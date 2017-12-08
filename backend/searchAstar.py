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
#close_list to store nodes without any options to go to destination

#add origin to a list result_path

#f(n) is the distance between two nodes and is stored in edge

#h(n) is the Euclidean  distance between that node and the the destination
#calculate g(n) = f(n) + h(n) for all nodes


# Step 3: At origin, find path with minimum elevation gain


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
