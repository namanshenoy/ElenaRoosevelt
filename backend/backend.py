import requests
import json
import osmnx as ox
import networkx as nx
from key import google_key
import sys
import numpy as np
import json


class Elena_backend:
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	user_given_origin = "Brandywine Amherst MA"
	user_given_destination = "UMass Amherst"
	elevation_type = "minimize"
	travel_mode = "bike"
	graph = None
	shortest_path_route_stats = dict()
	elevation_route_stats = dict()
	combined_route_stats = dict()
	ox.config(log_console=True)#, use_cache=True) # for logging, remove later

	def __init__(self):
		self.graph = self.load_graph('amherst_'+self.travel_mode+'.graphml')
		#self.graph = self.load_graph('pioneer_valley_'+self.travel_mode+'.graphml')

	def execute(self, user_given_origin, user_given_destination, elevation_type, travel_mode):
		self.user_given_origin = user_given_origin
		self.user_given_destination = user_given_destination
		self.elevation_type = elevation_type
		self.travel_mode = travel_mode

		self.add_impedance_to_graph_edges()
		actual_origin, actual_destination = self.find_actual_origin_and_destination()
		route_by_length = self.compute_route(actual_origin, actual_destination, criteria = 'length')
		route_by_impedance = self.compute_route(actual_origin, actual_destination, criteria = 'impedance')
		# self.plot_route(route_by_length)
		# self.plot_route(route_by_impedance)
		self.shortest_path_route_stats = self.get_route_stats(route_by_length)
		self.elevation_route_stats = self.get_route_stats(route_by_impedance)
		self.combined_route_stats = {'shortest_path_route_stats' : self.shortest_path_route_stats,
									'elevation_route_stats' : self.elevation_route_stats}

		# self.print_route_stats(self.shortest_path_route_stats, criteria = 'length')
		# self.print_route_stats(self.elevation_route_stats, criteria = 'impedance')
		# self.send_data_to_frontend()

	def add_impedance_to_graph_edges(self):
	    # add impedance and elevation rise values to each edge in the projected graph
	    # use absolute value of grade in impedance function if you want to avoid uphill and downhill
		for u, v, k, data in self.graph.edges(keys=True, data=True):
			length = float(data['length'])
			grade = float(data['grade'])
			grade_abs = float(data['grade_abs'])
			data['impedance'] = self.calc_impedance(length, grade)
			data['rise'] = length * grade


	# TODO handle x% shortest distance property and experiment with penalty values
	def calc_impedance(self, length, grade):
		#only go uphill if it has sqrt(length)
		if self.elevation_type == 'downhills':
			if grade <= 0:
				return length
			return length**2
		#only go dowhill if it has sqrt(length) problem is it goes too far sometimes
		elif self.elevation_type == 'uphills':
			if grade > 0:
				return length
			return length**2
		#cruising route (within length)
		elif self.elevation_type == 'minimize':
			#this also makes grade an absolute value
			penalty = grade**2
			return length * penalty
		#TODO this needs work.. suppose to maximize hills
		elif self.elevation_type == 'maximize':
			penalty = grade**2
			return 1/(length*penalty)
		#maximizes descent total
		elif self.elevation_type == 'lowest_grade_total':
			return (grade+1)
		#maximizes ascent total
		elif self.elevation_type == 'largest_grade_total':
			return (grade*-1)+1




	def find_actual_origin_and_destination(self):
		origin_coord = self.get_coords_of_location(self.user_given_origin)
		dest_coord = self.get_coords_of_location(self.user_given_destination)
		actual_origin = ox.get_nearest_node(self.graph, (origin_coord['lat'], origin_coord['lng']))
		actual_destination = ox.get_nearest_node(self.graph, (dest_coord['lat'], dest_coord['lng']))
		return actual_origin, actual_destination

	def get_coords_from_google(self, location):
		r = requests.get(self.url+location+'&key='+google_key)
		return r.json()

	# returns JSON coordinates [lat, long] for a location
	def get_coords_of_location(self, location):
		location_data_from_google = self.get_coords_from_google(location)
		location_coord = location_data_from_google['results'][0]['geometry']['location']
		return location_coord

	def compute_route(self, origin, destination, criteria):
		route = nx.shortest_path(self.graph, origin, destination, weight=criteria)
		return route

	def plot_route(self, route):
		ox.plot_graph_route(self.graph, route)

	def load_graph(self, filename):
		return ox.load_graphml(filename=filename)

	def get_route_stats(self, route):
		route_stats = dict()
		route_node_coords = self.get_route_node_coords(route)
		route_grades_stats = self.get_route_grade_stats(route)
		route_elevation_stats = self.get_route_elevation_stats(route)
		route_length, all_lengths = self.get_route_length(route)
		distances = self.transform_length_for_elevation_profile(all_lengths)
		route_node_elevations_with_distances = self.get_route_node_elevations_with_distances(route, distances)
		route_stats['route_node_coords'] = route_node_coords
		route_stats['route_elevations_with_distances'] = route_node_elevations_with_distances
		route_stats['route_grades_stats'] = route_grades_stats
		route_stats['route_elevation_stats'] = route_elevation_stats
		route_stats['route_length'] = route_length
		return route_stats

	def get_route_node_coords(self, route):
		nodes = list()
		for node in route:
			node_coords = dict()
			node_coords['lat'] = self.graph.node[node]['y'] # lat
			node_coords['lon'] = self.graph.node[node]['x'] # lon
			nodes.append(node_coords)
		return nodes

	def get_route_node_elevations_with_distances(self, route, distances):
		node_elevations_with_distances = list()
		for i in range(0, len(route)):
			node = route[i]
			node_elevation_with_distance = dict()
			node_elevation_with_distance['elevation'] = self.graph.node[node]['elevation']
			node_elevation_with_distance['distance'] = distances[i]
			node_elevations_with_distances.append(node_elevation_with_distance)
		return node_elevations_with_distances

	def get_route_grade_stats(self, route):
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

	def get_route_elevation_stats(self, route):
		route_elevation = dict()
		route_rises = ox.get_route_edge_attributes(self.graph, route, 'rise')
		ascent = np.sum([rise for rise in route_rises if rise >= 0])
		descent = np.sum([rise for rise in route_rises if rise < 0])
		route_elevation['rises'] = np.sum(route_rises)
		route_elevation['ascent'] = ascent
		route_elevation['descent'] = abs(descent)
		return route_elevation

	def get_route_length(self, route):
		all_lengths = ox.get_route_edge_attributes(self.graph, route, 'length')
		route_length = np.sum(all_lengths)
		return route_length, all_lengths

	def transform_length_for_elevation_profile(self, all_lengths):
		distances = list()
		distances.append(0)
		sum_ = 0
		for length in all_lengths:
			sum_ += length
			distances.append(sum_)
		return distances

	def print_route_stats(self, route, criteria):
		print("Route by %s stats" % criteria)
		msg = 'The average grade is {:.1f}% and the max is {:.1f}% and total sum is {:.1f}'
		print(msg.format(route['route_grades_stats']['grades_mean'], route['route_grades_stats']['grades_max'], route['route_grades_stats']['grades_total']))

		msg = 'Total elevation change is {:.0f} meters: a {:.0f} meter ascent and a {:.0f} meter descent'
		print(msg.format(route['route_elevation_stats']['rises'], route['route_elevation_stats']['ascent'],
		 					route['route_elevation_stats']['descent']))

		print('Total trip distance: {:,.0f} meters'.format(route['route_length']))
		print('\n')

	def send_data_to_frontend(self):
		# print(json.dumps(self.combined_route_stats, indent=2))
		return self.combined_route_stats


# Uncomment for command line testing
# def main(argv):
# 	elena_backend_object = Elena_backend(user_given_origin = argv[0], user_given_destination = argv[1],
# 										elevation_type = argv[2], travel_mode = argv[3])
# 	elena_backend_object.execute()
#
#
# if __name__ == "__main__":
#    main(sys.argv[1:])
