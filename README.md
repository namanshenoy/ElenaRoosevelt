# ElenaRoosevelt
**Elevation-based Navigation**

Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain.
Let's say you are hiking or biking from one location to another. You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are looking for an intense yet time-constrained workout.

**Contributors**
```
Naman Shenoy, Corey Collins, Jaeseong Lee, Akash Mantry, Ly Harriet Bui
```
## Requirements to run
Requires at least Python 2.7.
Setup:
1. If you have virtualenv installed, set up a new virtual environment:
  `python virtualenv venv`
2. Enter the created venv folder and clone the repository using:
  `git clone https://github.com/namanshenoy/ElenaRoosevelt.git`
3. Activate the virtual environment:
  Linux: `source bin/activate`
  Windows: `Scripts/activate.bat`
4. Install the requirements:
  `pip install -r requirements`
5. This should install all the requirements, if later on, a dependency is missing, you can install it using:
  `pip install requirement`
6. At this point, you have two options:
  1. Local server, you can run the following command to run a server for debug/test usage:
    python backend/server.py`
    This will run a server at URL 0.0.0.0:7000:
  2. For a higher scale server:
    `gunicorn wsgi -b 0.0.0.0:7000  --workers 3 --timeout 60`
    This will also run a server at URL 0.0.0.0:7000, but will be able to handle a much larger load


## Technology stack
* Flask backend - We use flask as a backend server to host our Frontend and our API. We used Flask as most of our backend code was Python and flask is a lightweight Python framework

* Gunicorn for HTTP server
* Javascript/JQuery Frontend
* Materialize CSS and JS - materializecss.com



## Algorithm
**Description**

FRONTEND FEATURES:
* Search for a route within Pioneer valley,
* Autocomplete Places
* Display navigation details per route change or direction change
* Display direction between each step in the route
* Get a route with the ‘get route’ button or pressing enter key on the input fields
* Continue a step in the route with the ‘next pin’ button
* Go back a step in the route with the ‘go back’ button
* Clear all steps in the route (return to the 1st step)
* Navigate a map of the world (functions are currently within pioneer valley)


BACKEND:
* Dijkstra’s algorithm from Osmx allows us to keep track of cost of the move for the past nodes and the current move being considered. We manipulated the weight function taking in length (distance between two nodes) and grade (slopes between two node’s elevation) in order to minize the elevation within certain length. 

* Astar search was implemented to reduce the cost of searching for the shortest past from O(E log(V)) to O(E).


API FEATURES:



## API Model:
```
www.elenaroosevelt.world:7000/get_route/[origin string]/[destination string]/[elevation type]/[transportation method]
```

It will return:
```json
{
  "elevation_route_stats": {
    "route_elevation_stats": {
      "ascent": "Total Ascent Distance, Type: Float",
      "descent": "Total Descent Distance, Type: Float",
      "rises": "Net height gain, Type: Float"
    },
    "route_elevations_with_distances": [
        {
            "distance": "Distance from this node to next, Type: Float",
            "elevation": "Height of node, Type: Float"
        }
    ],
    "route_grades_stats":{
        "grades_list":[
        "List of grade per edge, Type: Float"
        ],
        "grades_max": "Maximum grade, Type: Float",
        "grades_mean": "Mean grade, Type: Float",
        "grades_total": "Sum of grades, Type: Float"
    },
    "route_length": "Route length, Type: Float",
    "route_node_coords":[
         {
           "lat": "Latitude of Node, Type: Float",
            "lon": "Longitude of Node, Type: Float"
        }
    ]
  },
  "shortest_path_route_stats": {
    "route_elevation_stats": {
      "ascent": "Total Ascent Distance, Type: Float",
      "descent": "Total Descent Distance, Type: Float",
      "rises": "Net height gain, Type: Float"
    },
    "route_elevations_with_distances": [
        {
            "distance": "Distance from this node to next, Type: Float",
            "elevation": "Height of node, Type: Float"
        }
    ],
    "route_grades_stats":{
        "grades_list":[
        "List of grade per edge, Type: Float"
        ],
        "grades_max": "Maximum grade, Type: Float",
        "grades_mean": "Mean grade, Type: Float",
        "grades_total": "Sum of grades, Type: Float"
    },
    "route_length": "Route length, Type: Float",
    "route_node_coords":[
         {
           "lat": "Latitude of Node, Type: Float",
            "lon": "Longitude of Node, Type: Float"
        }
    ]
  },

}
```


##### The following are valid entries for the api fields:

* Origin String: This is any string value for for the address you’re starting your route from. Google GeoLocation API will attempt to resolve this string value into Latitude/Longitude points to be placed onto our graph. Some examples of this include “Amity Place, Amherst MA 01002”, “UMass Amherst”, “Bridge St, Amherst”, “Amherst MA”.

* Destination String: The format is the same as origin string. However, this value will be used as the destination of the route.

### Elevation Type:
There are 3 current supported elevation types you can enter into this field. Each one results in a different model for the impedance function in our backend. This function determines how to calculate the edge weights in our graph prior to performing dijkstra's algorithm. It takes in two parameters for each edge (grade, length) and returns the weight value for that edge, where grade is a value within [-1, 1] to represent the slope of the edge and length represents the distance of the edge.


* minimize: This method attempts to avoid slopes throughout the route, whether it’s uphill or   downhill. It will try to maintain the flattest route possible within reasonable distance     from the shortest route. Model is as follows:
  ```
  penalty = grade^2
  impedance = penalty * length
  ```
  Traditionally for calculating the shortest path the length is used for each edge weight. By using grade as a penalty on the length, the amount of grade will affect the size of the length. Grade is squared for two reasons: to make the grade absolute so negative grades become positive, and to amplify the penalty on length.
  This option is best for those seeking to find the best route for a cruising bike ride.
* downhills: This method attempts to maximize the amount of length going downhill. If you are a longboarder or biker seeking to find the most downhill slopes throughout their route, this is the option to pick. The impedance model is as follows:
  ```
  if grade <= 0:
  	impedance = length
  else:
  	impedance = length^2
  ```
  This model will square the length of any uphill edge. In other words, the shortest route algorithm will only favor an uphill slope over a straight/downhill if its length is at least the square root of the others.

*  uphills: Contrary to downhills, this method attempts to maximize the amount of length going uphill. If you are a runner or biker trying to strengthen their calves with a workout utilizing the most hills, this is definitely for you. The model for impedance is as follows:
    ```
    if grade > 0:
        impedance = length
    else:
        impedance = length^2
    ```
    As you’ll notice this model is the opposite of the downhills method. This method will only favor a downhill/straight slope if the square root of its length is less than the uphill options.


### Transportation Method:
There is only 1 option currently supported for this, which is “bike”. The graph we have active in the backend is optimized for biking, and may easily be expanded in the future for other methods such as “walking” or “driving”. However the biking option works well with walking or running as well.


### Testing:
Run command from backend folder to test backend.
```
 python -m unittest discover -v
```
