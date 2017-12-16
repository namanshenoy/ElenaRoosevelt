from flask import Flask, jsonify, render_template
from elena_backend import ElenaBackend
from utils.setup_graph import SetupGraph
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
setup_graph = SetupGraph('amherst_bike.graphml')
graph = setup_graph.get_graph()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_route/<origin>/<destination>/<elevation_type>/<transportation_method>", methods=['GET'])
def get_data(origin, destination, elevation_type, transportation_method):
    """Function called when front-end makes an API request.
    Args:
        origin (string): User given origin
        destination (string): User given destination
        elevation_type(string): Type of elevation (minimize, uphills, downhills)
        transportation_method (string): This is not included in this version and is left for future implementation

    Returns:
        combined_information (json): This is sent to the front-end and includes the route and all the associated
        information
        """
    elena_backend_object = ElenaBackend(elevation_type, graph)
    actual_origin, actual_destination = elena_backend_object.find_actual_origin_and_destination(origin, destination)
    shortest_route_by_length = elena_backend_object.compute_route_by_criteria(actual_origin, actual_destination,
                                                                              criteria='length')
    shortest_route_by_impedance = elena_backend_object.compute_route_by_criteria(actual_origin, actual_destination,
                                                                                 criteria='impedance')

    shortest_route_information = elena_backend_object.compute_route_information(shortest_route_by_length)
    elevation_route_information = elena_backend_object.compute_route_information(shortest_route_by_impedance)
    combined_information = {'shortest_path_route_stats': shortest_route_information,
                            'elevation_route_stats': elevation_route_information}

    return jsonify(combined_information)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, use_reloader=False)
