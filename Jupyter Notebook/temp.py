def find_shortest_path_gain(G, origin, destination):
    print('origin', origin)
    print('destination', destination)
    print('start')
    travel_length = 0
        #add origin to open_list
    open_list.put(origin, 0)
    cost_elevation = 0

    while not open_list.empty():
        print('close_list', close_list)
            #At origin, find path with minimum elevation gain => find node with least f on the open list
            #remove from the list
        current_node = open_list.get()
        print('Pop a node out of open list')
        print('current_node', current_node)

        open_list.display()
        has_path = True
      #  print('current node', current_node)
       # print(current_node == destination)
       # print('is empty', open_list.empty())
      #  print(type(current_node))
      #  print(type(destination))
        if current_node == destination:
            print(current_node == destination)
            close_list.append(current_node)
            return  close_list, travel_length

        else:
            if current_node not in close_list:
               # print(G.neighbors(current_node))
                for next_node in G.neighbors(current_node):
                    #if neightbor contain destination, go to destination
                    if next_node == destination:
                        close_list.append(current_node)
                        close_list.append(next_node)
                        return  close_list, travel_length
                  #  print('next node', next_node)





                     if next_node not in close_list:
                         elevation = G.get_edge_data(current_node,next_node).values()[0]['impedance']
                         g = G.get_edge_data(current_node,next_node).values()[0]['length']


                         h = G.node[next_node]['h_value']
                         f = g+h
                         print('next node', next_node)
                         print('g',g)
                         print('h', h)
                         print('f',f)

                         possible_travel_length = travel_length + f
                         print('in open list?', open_list.isContain(next_node))
                         if open_list.empty() or not open_list.isContain(next_node):
                                 open_list.put(next_node, f)
                                 travel_length += g                                        # print('close_list', close_list)

                      open_list.display()




        #check if there are node to move to from next_node that is not current_node:

        num_neighbor = 0

        for value in nx.neighbors(G,current_node ):
            num_neighbor +=1
            node_id = value

            print('value',value)
            print('node_id',num_neighbor)

        if (num_neighbor > 1 and current_node != origin) or (current_node == origin:

            if current_node not in close_list:
                close_list.append(current_node)
                print('travel length',travel_length )
                print('g to add',g)



    print('finish')

    return close_list, travel_length
