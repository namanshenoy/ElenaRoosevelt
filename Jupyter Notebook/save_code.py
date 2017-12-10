def draw_bounding_box(origin_x, origin_y, destination_x, destination_y, graph):
    origin = ox.get_nearest_node(G, (origin_x, origin_y))
    destination = ox.get_nearest_node(G, (destination_x, destination_y))

    #Calculate midpoint between origin and destination
    lat1 = math.radians(origin_x)
   lon1 = math.radians(origin_y)
    lat2 = math.radians(destination_x)
    lon2 = math.radians(destination_y)
   print(lat1, lon1, lat2, lon2)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)

    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1)
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    lat3 = round(math.degrees(lat3), 2)
   lon3 = round(math.degrees(lon3), 2)
    print (lat3, lon3)

    #Calculate distance between origin and destination
    dlon = destination_y - origin_y
    dlat = destination_x - origin_x
    a = ((math.sin(dlat/2))**2) + math.cos(origin_x) * math.cos(destination_x) * ((math.sin(dlon/2))**2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    d = R * c
    print(d)

   #determine distance from midpoint to edge of bounding box
    distance =  d*20
    print (distance)


   bbox = ox.bbox_from_point((lat3, lon3), distance=distance, project_utm=True)

    return origin, destination, bbox

origin, destination,bbox = draw_bounding_box(42.350564, -72.527400, 42.391157, -72.526712,G)

# project the street network to UTM
G_proj = ox.project_graph(G)
route_by_length = nx.shortest_path(G_proj, source=origin, target=destination, weight='length')
fig, ax = ox.plot_graph_route(G_proj, route_by_length, bbox=bbox, node_size=0)
 #Given two nodes, calculate the shortest path between those nodes

 #Limit the final distance to 120% of the shortest path
