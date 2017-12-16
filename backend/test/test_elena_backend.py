import unittest
from utils.setup_graph import SetupGraph
from elena_backend import ElenaBackend


class TestElenaBackend(unittest.TestCase):
    """For testing, use amherst_bike.graphml since pioneer valley data takes a lot of time to load resulting in slow
    testing."""

    def setUp(self):
        setup_graph = SetupGraph('amherst_bike.graphml')
        self.graph = setup_graph.get_graph()

    def test_origin_none(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        with self.assertRaises(Exception) as context:
            elena_backend_object.find_actual_origin_and_destination(None, "Mars")
        self.assertTrue("Empty String or None provided as origin" in str(context.exception))

    def test_destination_none(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        with self.assertRaises(Exception) as context:
            elena_backend_object.find_actual_origin_and_destination("Mars", None)
        self.assertTrue("Empty String or None provided as destination" in str(context.exception))

    def test_empty_string_origin(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        with self.assertRaises(Exception) as context:
            elena_backend_object.find_actual_origin_and_destination("", "Mars")
        self.assertTrue("Empty String or None provided as origin" in str(context.exception))

    def test_empty_string_destination(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        with self.assertRaises(Exception) as context:
            elena_backend_object.find_actual_origin_and_destination("Mars", "")
        self.assertTrue("Empty String or None provided as destination" in str(context.exception))

    def test_correct_origin_destination(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")
        self.assertIsNotNone(origin)
        self.assertIsNotNone(destination)

    def test_none_origin_compute_route(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")
        with self.assertRaises(Exception) as context:
            elena_backend_object.compute_route_by_criteria(None, destination, "length")
        self.assertTrue("Empty string or None provided as origin for computing route" in str(context.exception))

    def test_none_destination_compute_route(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")
        with self.assertRaises(Exception) as context:
            elena_backend_object.compute_route_by_criteria(origin, None, "length")
        self.assertTrue("Empty string or None provided as destination for computing route" in str(context.exception))

    def test_none_criteria_compute_route(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")

        with self.assertRaises(Exception) as context:
            elena_backend_object.compute_route_by_criteria(origin, destination, None)
        self.assertTrue("Empty string or None provided as criteria for computing route" in str(context.exception))

    def test_wrong_criteria_compute_route(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")
        with self.assertRaises(Exception) as context:
            elena_backend_object.compute_route_by_criteria(origin, destination, "size")
        self.assertTrue("Incorrect value of criteria provided" in str(context.exception))

    def test_correct_values_compute_route(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")

        self.assertIsNotNone(elena_backend_object.compute_route_by_criteria(origin, destination, "length"))
        self.assertIsNotNone(elena_backend_object.compute_route_by_criteria(origin, destination, "impedance"))

    def test_none_compute_route_information(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        with self.assertRaises(Exception) as context:
            elena_backend_object.compute_route_information(None)
        self.assertTrue("Route nor provided while computing route information" in str(context.exception))

    def test_correct_route_compute_route_information(self):
        elena_backend_object = ElenaBackend('minimize', self.graph)
        origin, destination = elena_backend_object.find_actual_origin_and_destination("Brandywine Amherst MA",
                                                                                      "UMass Amherst")
        shortest_route_by_length = elena_backend_object.compute_route_by_criteria(origin, destination,
                                                                                  criteria='length')

        self.assertIsNotNone(elena_backend_object.compute_route_information(shortest_route_by_length))


if __name__ == "__main__":
    unittest.main()
