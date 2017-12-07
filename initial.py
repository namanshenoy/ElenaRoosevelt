import osmnx as ox
from key import google_key
import sys

def main(argv):
    location = argv[0]
    network_type = argv[1]
    filename = 'amherst_' + str(network_type) + '.graphml'
    # get graph from OSMaps
    graph = ox.graph_from_place(location, network_type=network_type)

    # add elevation to each of the nodes, using the google elevation API, then calculate edge grades
    graph = ox.add_node_elevations(graph, api_key=google_key)
    graph = ox.add_edge_grades(graph)

    # save graph to disk
    ox.save_graphml(graph, filename=filename)

if __name__ == "__main__":
   main(sys.argv[1:])

# python initial.py 'Amherst, Massachusetts' 'bike'
# python initial.py 'Amherst, Massachusetts' 'walk'
