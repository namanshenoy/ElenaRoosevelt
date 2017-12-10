import math

import heapq

class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)

    def isContain(self, item):
        for (cost, node) in self.elements :
            if node == item:
                return True

        return False
    def check_priority(self, item):
        for (cost, node) in self.elements :
            if node == item:
                return cost

        return -1

    def display(self):
        print('priority queue',self.elements[:5])

    def peek(self):
        priority, item = heapq.heappop(self.elements)

        heapq.heappush(self.elements, (priority, item))
        return (priority, item)

    def replace(self, priority, item):
        i=0
        for (cost, node) in self.elements :
            if node == item:
                self.elements[i] = (priority, item)
            i+=1


import osmnx as ox
import osmnx as ox, networkx as nx, numpy as np
ox.config(log_console=True, use_cache=True)
city = ox.gdf_from_place('Amherst, MA')
G = ox.graph_from_place('Amherst, MA', network_type='bike')
google_elevation_api_key = 'AIzaSyDEOzFyx1050FqVa2fg-IhAdP6Bn8qq2Xw' #replace this with your own API key

# add elevation to each of the nodes, using the google elevation API, then calculate edge grades
G = ox.add_node_elevations(G, api_key=google_elevation_api_key)
G = ox.add_edge_grades(G)


"""
This is A star search algorithm to find a path that maximizes or minimizes
the elevation gain. The returned path has to be no longer than
(distance_shortest_path + 0.2*distance_shortest_path)

Input: graph, max_distance, origin, destination, type_of_elevation_optimization
Output: list of nodes
"""

'''Calculate f(n) and h(n) for each node in the graph
'''
travel_dis = 0
    #initialize open list: contains one node at a time, a parent node, remove that node,
    #add node's neighbor with the least cost
open_list = PriorityQueue()
    #initialize closed list: is a record of all locations which have been explored and evaluated by the algorithm.
close_list = []
path = []
'''Function takes in a graph, and destination node to calculate cost
   destination is a node
'''
import math
#MARGIN: distance between the bounding box and the furthest node among origin and destination away from center point
MARGIN = 1000
#Earth's radius (miles)
R =3959

def calculate_midpoint(origin_x, origin_y, destination_x, destination_y):

    #Calculate midpoint between origin and destination
    lat1 = math.radians(origin_x)
    lon1 = math.radians(origin_y)
    lat2 = math.radians(destination_x)
    lon2 = math.radians(destination_y)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)

    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    lat3 = round(math.degrees(lat3), 2)
    lon3 = round(math.degrees(lon3), 2)
   # print (lat3, lon3)
    return lat3, lon3

def calculate_distance_between_two_nodes(origin_x, origin_y, destination_x, destination_y):
     #Calculate distance between origin and destination
    dlon = destination_y - origin_y
    dlat = destination_x - origin_x
    a = ((math.sin(dlat/2))**2) + math.cos(origin_x) * math.cos(destination_x) * ((math.sin(dlon/2))**2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    d = R * c
    #determine distance from midpoint to edge of bounding box
    distance =  d*20
    print (distance)

    return distance

# select an origin and destination node and a bounding box around them
def draw_bounding_box(origin_x, origin_y, destination_x, destination_y, graph):
    origin = ox.get_nearest_node(G, (origin_x, origin_y))
    destination = ox.get_nearest_node(G, (destination_x, destination_y))

    lat3, lon3 = calculate_midpoint(origin_x, origin_y, destination_x, destination_y)
    print(lat3, lon3)
    #Calculate distance between origin and destination
    #determine distance from midpoint to edge of bounding box
    distance = calculate_distance_between_two_nodes(origin_x, origin_y, destination_x, destination_y)
    print (distance)


    bbox = ox.bbox_from_point((lat3, lon3), distance=distance, project_utm=True)

    return origin, destination, bbox



def heurisic_with_Eulicidian(origin_x, origin_y, destination_x, destination_y):
    h = math.sqrt((origin_x -  destination_x)**2 + (origin_y -  destination_y)**2)
    return h

def heurisic_networkx(origin_x, origin_y, destination_x, destination_y):
    h = ((origin_x -  destination_x)**2 + (origin_y -  destination_y)**2) ** 0.5
    return h

# define some edge impedance function here
def impedance(length, grade):
    penalty = grade ** 2
    return length * penalty

def has_edge(node1, node2, G):
    for node in G.neighbors(node1):
        if node == node2:
            return True
    return False
'''
Algorithm does not account for terrain or mainroad
'''
def find_shortest_path_gain(G, origin, destination):
    print('origin', origin)
    print('destination', destination)
    parent = None
        #add origin to open_list
    open_list.put(origin, 0)

    past_cost = 0

    while not open_list.empty():
        print('close_list', close_list)
            #At origin, find path with minimum elevation gain => find node with least f on the open list
            #remove from the list
        top_node =  open_list.get()
        current_node = top_node[1]
        cost_for_node = top_node[0]

        print('POP A NODE OUT OF OPEN LIST: CURRENT NODE')
        print('current_node', current_node)

        open_list.display()
      #  print('current node', current_node)
       # print(current_node == destination)
       # print('is empty', open_list.empty())
      #  print(type(current_node))
      #  print(type(destination))
        if current_node == destination:
            print(current_node == destination)
            path.append(current_node)
            while G.node[current_node]['parent'] >0:
                path.append(G.node[current_node]['parent'])
                current_node = G.node[current_node]['parent']
            print('finish')
            return path, past_cost
        #check if current_node connected to previous node:

      #  print('next node', next_node)
        if current_node == origin:
            G.node[current_node]['h_value'] = 0
            past_cost += cost_for_node - G.node[current_node]['h_value']
           # print(G.neighbors(current_node))
        for next_node in G.neighbors(current_node):
            print('NEXT NODE', next_node)


            if next_node in close_list:
                continue

            num_neighbor = 0
            for neighbor in G.neighbors(next_node):
                num_neighbor +=1
                if (num_neighbor <=1) and (next_node != destination):
                    continue

            h = G.node[next_node]['h_value']
            elevation = G.get_edge_data(current_node,next_node).values()[0]['impedance']
            edge_length = G.get_edge_data(current_node,next_node).values()[0]['length']
            f = past_cost + edge_length +h
            print('past_cost', past_cost)
            print('edge_length', edge_length)
            print('h', h)
            print('f',f)

            if open_list.isContain(next_node):
                if open_list.check_priority(next_node) > f:
                    open_list.replace(f, next_node)
                    G.node[next_node]['parent'] = current_node

            else:

                open_list.put(next_node, f)
                G.node[next_node]['parent'] = current_node

            open_list.display()
    #check if there are node to move to from next_node that is not current_node:



        if current_node not in close_list:
            close_list.append(current_node)


    raise ValueError('No Path Found')
'''
Dubois - Franklin
42.389813, -72.52825000000001, 42.3892436, -72.52251669999998
Boulder - Umass
'''
origin, destination,bbox = draw_bounding_box(42.35056399999999, -72.5274, 42.3911569, -72.5267121, G)
# project the street network to UTM
G_proj = ox.project_graph(G)

for edge in G_proj.edges.items():
    node1 = edge[0][0]
    node2 = edge[0][1]
    g = edge[1]['length']
        #f(n) is the distance between two nodes and is stored in edge
    edge[1]['g_value'] = g
   # G_proj.add_edge(node1,node2, g_value = g )

        #h(n) is the Euclidean  distance between that node and the the destination
for node in G_proj.nodes:
    origin_x = G_proj.node[node]['x']
    origin_y = G_proj.node[node]['y']
    destination_x = G_proj.node[destination]['x']
    destination_y = G_proj.node[destination]['y']
    h = heurisic_networkx(origin_x, origin_y, destination_x, destination_y)
        #calculate g(n) = f(n) + h(n) for all nodes
    G_proj.add_node(node,h_value=h)
    G_proj.add_node(node, parent = 0)

# add impedance and elevation rise values to each edge in the projected graph
# use absolute value of grade in impedance function if you want to avoid uphill and downhill
for u, v, k, data in G_proj.edges(keys=True, data=True):
    data['impedance'] = impedance(data['length'], data['grade_abs'])
    data['rise'] = data['length'] * data['grade']

shortest_path , length= find_shortest_path_gain(G_proj, origin, destination)
print('origin', origin)
print('destination',destination)
print('shortest path', shortest_path, len(shortest_path))
print('length', length )

def length_of_path(path, G):
     distance = 0
     for i in range(0, len(path)-2):
         print('i', i)
         print('distance', distance)
         distance += G.get_edge_data(path[i],path[i+1]).values()[0]['length']
     return distance

print('shortest distance', length_of_path(shortest_path,G_proj ))
