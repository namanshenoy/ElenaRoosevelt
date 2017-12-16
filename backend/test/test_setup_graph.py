import unittest
from utils.setup_graph import SetupGraph


class TestSetupGraph(unittest.TestCase):
    """For testing, use amherst_bike.graphml since pioneer valley data takes a lot of time to load resulting in slow
    testing."""

    def test_get_graph(self):
        setup_graph = SetupGraph('amherst_bike.graphml')
        graph = setup_graph.get_graph()
        self.assertIsNotNone(graph)


if __name__ == "__main__":
    unittest.main()





