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
        return heapq.heappop(self.elements)[1]

    def isContain(self, item):
        for (cost, node) in self.elements :
            if node == item:
                return True

        return False

    def display(self):
        print('priority queue',self.elements)

#class searcgAstar:
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
'''Function takes in a graph, and destination node to calculate cost
   destination is a node
'''
def calculate_cost(G, destination):
    #if G is None:
    #    raise InputError
    #else:
    for edge in G.edges:
        node1 = G.node[edge['v']]
        node2 = G.node[edge['u']]
        g = math.sqrt((node1['x'] -  node2['x'])**2 - (node1['y'] -  node2['y'])**2)
        #f(n) is the distance between two nodes and is stored in edge
        G.add_edge(node1,node2, g_value = g )

        #h(n) is the Euclidean  distance between that node and the the destination
    for node in G.nodes:
        h = math.sqrt((node1['x'] -  destination['x'])**2 - (node1['y'] -  destination['y'])**2)
        #calculate g(n) = f(n) + h(n) for all nodes
        G.add_node(node,h_value=h)

    return


def find_path_minimize_elevation_gain(G, origin, destination, max_distance):
    travel_length = 0
        #add origin to open_list
    open_list.put(origin, 0)
    cost_elevation = 0

    while not open_list.empty():
            #At origin, find path with minimum elevation gain => find node with least f on the open list
            #remove from the list
        current_node = open_list.get()
        if current_node == destination:
            return

        else:
            if current_node not in close_list:
                for next_node in G.neighbors(current_node):
                    if next_node not in close_list:
                        elevation = G[current_node][next_node]['elevation']
                        g = G[current_node][next_node]['g_value']
                        h = G.node[next_node]['h_value']
                        f = g+h
                        possible_travel_length = travel_length + f
                        if possible_travel_length<=max_distance:
                            if open_list.empty() or next_node not in open_list:
                                open_list.put(next_node, elevation)
                                travel_length = g
                                if current_node not in close_list:
                                    close_list.append(current_node)

    return close_list, travel_length


#if g(n) <= max_distance: go to node B

    #update travel_dis += f(n)
    #if B is the destination:
        #add B to result_path
        #return result_path
    #find all the routes that are not to nodes in result_path
        #repeat Step 3
        #if cannot find satisfying edge, go back to previous node in the result_path

#else: consider the next smallest elevation edge and so ond

#if no edge <= max_distance
    #throw exception error: cannot find path smaller <= max_distance
