import math

"""
This is A star search algorithm to find a path that maximizes or minimizes
the elevation gain. The returned path has to be no longer than
(distance_shortest_path + 0.2*distance_shortest_path)

Input: graph, max_distance, origin, destination, type_of_elevation_optimization
Output: list of nodes
"""

'''Calculate f(n) and h(n) for each node in the graph
'''
float travel_dis = 0
#initialize open list: contains one node at a time, a parent node, remove that node,
#add node's neighbor with the least cost
open_list = Queue()
#initialize closed list: is a record of all locations which have been explored and evaluated by the algorithm.
close_list = {}
'''Function takes in a graph, and destination node to calculate cost
   destination is a node
'''
def calculate_cost(G, destination):
    if graph is None:
        raise InputError
    else:
        for edge in G.edges:
            node1 = G.node[edge['v']]
            node2 = G.node[edge['u']]
            f = math.sqrt((node1['x'] -  node2['x'])**2 - (node1['y'] -  node2['y'])**2)
            #f(n) is the distance between two nodes and is stored in edge
            G.add_edge(node1,node2, f_value = f )

            #h(n) is the Euclidean  distance between that node and the the destination
        for node in G.nodes:
            h = math.sqrt((node1['x'] -  destination['x'])**2 - (node1['y'] -  destination['y'])**2)
            #calculate g(n) = f(n) + h(n) for all nodes
            g.add_node(node,h_value=f)

    return



def find_path_minimize_elevation_gain(graph, origin, destination):

    return

#add origin to a list result_path
s
#At origin, find path with minimum elevation gain

#add origin to open_list

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
