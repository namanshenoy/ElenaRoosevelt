import osmnx as ox


class SetupGraph(object):
    """
        This class loads the already saved graph from data folder.
    """

    def __init__(self, filename):
        self.graph = self._load_graph(filename)
        self._add_attributes_to_graph_edges()

    @staticmethod
    def _load_graph(filename):
        return ox.load_graphml(filename=filename)

    def _add_attributes_to_graph_edges(self):
        """Add rise value to the graph"""
        for u, v, k, data in self.graph.edges(keys=True, data=True):
            length = float(data['length'])
            grade = float(data['grade'])
            data['rise'] = length * grade

    def get_graph(self):
        return self.graph
