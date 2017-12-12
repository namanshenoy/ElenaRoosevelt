from flask import Flask, jsonify, render_template
from backend import Elena_backend
from flask_cors import CORS

app = Flask(__name__)
elena_backend_object = Elena_backend()

CORS(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_route/<origin>/<destination>/<elevation_type>/<travel_mode>", methods=['GET'])
def get_data(origin, destination, elevation_type, travel_mode):
    elena_backend_object.execute(user_given_origin = origin, user_given_destination = destination,
    									elevation_type = elevation_type, travel_mode = travel_mode)
    data_to_send = elena_backend_object.send_data_to_frontend()
    return jsonify(data_to_send)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug = True, use_reloader=False) # remove debug later
