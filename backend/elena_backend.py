import requests
import osmnx as ox
import networkx as nx
from key import google_key
import numpy as np
from utils.elevation import Elevation


class ElenaBackend(object):
    """
        This class forms the backend and is responsible for getting the routes and computing all the information
        to be sent to front-end.
    """

    def __init__(self, elevation_type, graph):
        self.graph = graph
        self.elevation_type = Elevation[elevation_type].value
        self._add_impedance_to_graph_edges()

    def _add_impedance_to_graph_edges(self):
        """Add impedance to graph data depending on elevation type"""
        for u, v, k, data in self.graph.edges(keys=True, data=True):
            length = float(data['length'])
            grade = float(data['grade'])
            data['impedance'] = ElenaBackend._calc_impedance(length, grade, self.elevation_type)

    @staticmethod
    def _calc_impedance(length, grade, elevation_type):
        """Calculate impedance value depending on elevation type
        Args:
            length (float): length of edge
            grade (float): grade of edge
            elevation_type (enum) : kind of elevation

        Returns:
            impedance (float)
        """
        impedance = length

        # only go uphill if it has sqrt(length)
        if elevation_type == Elevation.uphills.value:
            if grade > 0:
                impedance = length**2

        # only go downhill if it has sqrt(length) problem is it goes too far sometimes
        elif elevation_type == Elevation.downhills.value:
            if grade <= 0:
                impedance = length**2

        # cruising route (within length)
        elif elevation_type == Elevation.minimize.value:
            # this also makes grade an absolute value
            penalty = grade**2
            impedance = length * penalty

        return impedance

    def find_actual_origin_and_destination(self, origin, destination):
        """Find the nearest origin and destination to user defined origin and destination
        Args:
            origin (list): coordinates of origin
            destination (list): coordinates of destination

        Returns:
            actual_origin (list)
            actual_destination (list)

        Raises:
            Exception: If empty string or None is provided as input
        """
        if not origin:
            raise Exception("Empty String or None provided as origin")
        if not destination:
            raise Exception("Empty String or None provided as destination")

        origin_coordinates = ElenaBackend._get_coordinates_of_location(origin)
        destination_coordinates = ElenaBackend._get_coordinates_of_location(destination)
        actual_origin = self._find_nearest_node(origin_coordinates)
        actual_destination = self._find_nearest_node(destination_coordinates)
        return actual_origin, actual_destination

    def _find_nearest_node(self, node):
        """Returns nearest node to the given node in the graph
        Args:
            node (list): coordinates of node

        Returns:
            nearest_node list : coordinates of nearest node
        """
        return ox.get_nearest_node(self.graph, (node['lat'], node['lng']))

    @staticmethod
    def _get_coordinates_from_google(location):
        """Get location data from Google's API
        Args:
            location (string): location name

        Returns:
            location (json): location data
        """
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
        r = requests.get(url+location+'&key='+google_key)
        return r.json()

    @staticmethod
    def _get_coordinates_of_location(location):
        """Get coordinates of location
        Args:
            location (string): location name

        Returns:
            location_coord (list): coordinates
        """
        location_data_from_google = ElenaBackend._get_coordinates_from_google(location)
        location_coord = location_data_from_google['results'][0]['geometry']['location']
        return location_coord

    def compute_route_by_criteria(self, origin, destination, criteria):
        """Compute the shortest route between source and destination based on criteria
        Args:
            origin (list): coordinates of origin
            destination (list): coordinates of destination
            criteria (string): 'length' or 'impedance'

        Returns:
            route (list): route data

        Raises:
            Exception: If empty string or None is provided as input
        """
        if not origin:
            raise Exception("Empty string or None provided as origin for computing route")
        if not destination:
            raise Exception("Empty string or None provided as destination for computing route")
        if not criteria:
            raise Exception("Empty string or None provided as criteria for computing route")

        if criteria not in ("length", "impedance"):
            raise Exception("Incorrect value of criteria provided")

        route = nx.shortest_path(self.graph, origin, destination, weight=criteria)
        return route

    def plot_route(self, route):
        """Auxillary function to plot the route for local testing
        Args:
            route (list): Route data
        """
        ox.plot_graph_route(self.graph, route)

    def compute_route_information(self, route):
        """Get all route information. This includes:
        1. Coordinates of nodes.
        2. Elevation and distance data for elevation chart.
        3. Grades of all the nodes.
        4. Elevations of all nodes.
        5. Total route length.
        This information is sent to front-end.
        Args:
            route (dict): Route data

        Returns:
            route_information (dict): all route information

        Raises:
            Exception: If empty string or None is provided as route
        """
        if not route:
            raise Exception("Route nor provided while computing route information")

        route_information = dict()

        route_coordinate_information = self._add_nodes_coordinate_information(route)
        route_grades_information = self._get_route_grade_information(route)
        route_elevation_information = self._get_route_elevation_information(route)
        all_leg_lengths = self._get_all_leg_lengths(route)
        route_elevations_with_distances = self._get_route_elevations_with_distances(route, all_leg_lengths)

        route_information['route_node_coords'] = route_coordinate_information
        route_information['route_elevations_with_distances'] = route_elevations_with_distances
        route_information['route_grades_stats'] = route_grades_information
        route_information['route_elevation_stats'] = route_elevation_information
        route_information['route_length'] = np.sum(all_leg_lengths)

        return route_information

    def _add_nodes_coordinate_information(self, route):
        """This function gets the coordinate information of all the nodes in the route
        Args:
            route (dict): Route data

        Returns:
            nodes (list): Coordinates of all the nodes
        """
        nodes = list()
        for node in route:
            node_coordinates = self._get_coordinates_of_node(node)
            nodes.append(node_coordinates)
        return nodes

    def _get_coordinates_of_node(self, node):
        """This function gets the coordinate information of a single node in the route
        Args:
            node (dict): Data of node

        Returns:
            coordinates_dict (dict): Coordinate data of node
        """
        coordinates_dict = dict()
        coordinates_dict['lat'] = self.graph.node[node]['y']  # latitude
        coordinates_dict['lon'] = self.graph.node[node]['x']  # longitude
        return coordinates_dict

    def _get_route_grade_information(self, route):
        """This function gets the grade information of the route
        Args:
            route (dict): Data of route

        Returns:
            route_grades (dict): Grades of the route
        """
        route_grades = dict()
        grades = ox.get_route_edge_attributes(self.graph, route, 'grade')
        grades = [float(i) for i in grades]
        grades_mean = np.mean(grades)*100
        grades_max = np.max(grades)*100
        grades_total = np.sum(grades)
        route_grades['grades_list'] = grades
        route_grades['grades_mean'] = grades_mean
        route_grades['grades_max'] = grades_max
        route_grades['grades_total'] = grades_total
        return route_grades

    def _get_route_elevation_information(self, route):
        """This function gets the elevation information (rise, ascent, descent) of the route
        Args:
            route (dict): Data of route

        Returns:
            route_elevation (dict): Elevation of the route
        """
        route_elevation = dict()
        route_rises = ox.get_route_edge_attributes(self.graph, route, 'rise')
        ascent = np.sum([rise for rise in route_rises if rise >= 0])
        descent = np.sum([rise for rise in route_rises if rise < 0])
        route_elevation['rises'] = np.sum(route_rises)
        route_elevation['ascent'] = ascent
        route_elevation['descent'] = abs(descent)
        return route_elevation

    def _get_all_leg_lengths(self, route):
        """This function all the individual leg lengths of the route
        Args:
            route (dict): Data of route

        Returns:
            all_leg_lengths (list): Lengths of the legs of the route
        """
        all_leg_lengths = ox.get_route_edge_attributes(self.graph, route, 'length')
        return all_leg_lengths

    def _get_route_elevations_with_distances(self, route, all_leg_lengths):
        """This function makes the points to be plotted by the elevation chart in the UI.
        Args:
            route (dict): Data of route
            all_leg_lengths (list): All leg lengths of the route
        Returns:
            route_elevations_with_distances (dict): Points of the chart for UI
        """
        route_elevations_with_distances = list()
        distance = 0
        for i in range(0, len(route)):
            node = route[i]
            node_elevation_with_distance = dict()
            node_elevation_with_distance['elevation'] = float(self.graph.node[node]['elevation'])
            node_elevation_with_distance['distance'] = distance
            route_elevations_with_distances.append(node_elevation_with_distance)
            distance += all_leg_lengths[i-1]
        return route_elevations_with_distances

    @staticmethod
    def print_route_information(route, criteria):
        """Auxillary function to print the route information for local testing.
        Args:
            route (dict): Data of route
            criteria (string): Criteria for the route
        """
        print("Route by %s stats" % criteria)
        msg = 'The average grade is {:.1f}% and the max is {:.1f}% and total sum is {:.1f}'
        print(msg.format(route['route_grades_stats']['grades_mean'], route['route_grades_stats']['grades_max'],
                         route['route_grades_stats']['grades_total']))

        msg = 'Total elevation change is {:.0f} meters: a {:.0f} meter ascent and a {:.0f} meter descent'
        print(msg.format(route['route_elevation_stats']['rises'], route['route_elevation_stats']['ascent'],
                         route['route_elevation_stats']['descent']))

        print('Total trip distance: {:,.0f} meters'.format(route['route_length']))
        print('\n')

