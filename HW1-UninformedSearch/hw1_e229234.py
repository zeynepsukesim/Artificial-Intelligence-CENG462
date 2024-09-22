def UnInformedSearch (method_name, problem_file_name):
    # read file
    with open(problem_file_name) as file:
        my_dict = eval(file.read().replace('\n', ' '))
    min_value = my_dict["min"] # extract min
    env_list = my_dict["env"] # extract env
    final_point = find_char(env_list, "F")
    start_point = find_char(env_list, "S")
    customers_points = find_char(env_list, "C")

    # construct graph(adj. list) as said in the HW document
    my_graph = {start_point[0]: customers_points + final_point}
    for key in customers_points:
        connection_list = []
        for customer in customers_points:
            if key != customer:
                connection_list.append(customer)
                my_graph[key] = connection_list + final_point
    # added final point as key to the graph, empty list on value means it has no outgoing edge
    my_graph.setdefault((final_point[0]), [])
    if method_name == "DFS":
        return dfs(my_graph, start_point[0], final_point[0], min_value)
    elif method_name == "BFS":
        return bfs(my_graph, start_point[0], final_point[0], min_value)
    elif method_name == "UCS":
        return ucs(my_graph, start_point[0], final_point[0], min_value)



#find wanted char in the env part
def find_char(lst, chr):  # lst=env_list, chr=wanted char
    char_index_list = []  # list to append indexes
    for idx, i in enumerate(lst):
        for idx2, ltr in enumerate(i):
            if ltr == chr:
                tpl = (idx, idx2)
                char_index_list.append(tpl)
    return char_index_list

#function for DFS
def dfs(graph, start, target, min_value):
    """
    :param graph: dictionary(adj. list)
    :param start: coordinates of our starting point
    :param target: destination point
    :param min_value: min customer count to visit
    :return final path
    """
    """
    stack will consist of <coordinates, stop count(which is the visited customer count),  path> 
    """
    stack = [(start, 0, [start])]
    while stack:
        current_node, current_stops, current_path = stack.pop() # pop current root element
        """
        if we come to the target point and reached required customer point count, we can return our path
        """
        if current_node == target and min_value <= current_stops:
            return convert_list(current_path) # convert_list is defined below. Used to convert list of tuples to list of list

        if current_stops <= min_value: # no need to traverse after stop_count reaches a certain point
            for neighbor in graph[current_node]:
                temp = current_path.copy() # we needed to make a copy of current_path as we will append every neighbor to current_path seperately
                temp.append(neighbor)
                if neighbor not in current_path:# if already in the path, then dont continue
                    if neighbor == target:
                        stack.append((neighbor, current_stops, temp)) # no need to increment current stop as its not a customer
                    else:
                        stack.append((neighbor, current_stops + 1, temp)) # increment current stop as we have visited a customer

    return None # path not found


#function for BFS
def bfs(graph, start, target, min_value):
    """

    :param graph: dictionary(adj. list)
    :param start: coordinates of the starting point
    :param target: coordinates of the final point
    :param min_value: min customer count to visit
    :return final path
    """
    """
    queue is consist of <coordinates, path>
    """
    queue = []
    visited = set()
    queue.append((start, [start]))
    visited.add(start)
    while queue:
        current_node, current_path = queue.pop(0) # popping the first element of our queue (list)
        visited.add(current_node)
        if current_node == target and len(current_path) == min_value + 2: # point to stop--if we reach the final point and the min customer count
            return convert_list(current_path)  # return current path
        neighbors = graph[current_node]
        for neighbor in neighbors:
            if neighbor not in current_path:
                temp = current_path[:] # we needed to make a copy of current_path as we will append every neighbor to current_path seperately
                temp.append(neighbor)
                queue.append((neighbor,temp)) # append to our original queue
    return None


def ucs(graph, start, target, min_value):
    """

    :param graph: dictionary(adj. list)
    :param start: coordinates of the starting point
    :param target: coordinates of the final point
    :param min_value: min customer count to visit
    :return: final path
    """
    """
    priority queue is consist of <cost(manhattan distance between two points), path, stop_point(min customer count)>
    """
    priority_queue = []
    priority_queue = heappush(priority_queue, (0, [start], 0)) #heappush function is defined below
    while priority_queue:
        distance, path, stop_count = heappop(priority_queue) #heappop function is defined below
        point = path[len(path) - 1]
        if point == target and stop_count == min_value + 1: #stop condition is defined here
            return convert_list(path)
        neighbors = graph[point]
        if stop_count <= min_value:
            for neighbor in neighbors:
                if neighbor not in path: #if already in the path, do not continue
                    totaldistance = distance + int(manhattan_distance(point, neighbor)) #calculate the total distanc(cost) of the current path
                    temp = path[:]
                    temp.append(neighbor)
                    priority_queue = heappush(priority_queue,(totaldistance, temp, stop_count + 1))
    return None


def manhattan_distance(start, final):
    # defined function for calculating manhattan_distance
    distance_y = abs(start[0] - final[0])
    distance_x = abs(start[1] - final[1])
    distance = distance_x + distance_y
    return distance


def heappush(priority_queue, tuple):
    # priority_queue should be a list.
    priority_queue.append(tuple) # given tuple is add to the list.
    return sorted(priority_queue, key=lambda x: x[0]) # sort the list and return


def heappop(priority_queue):
    # priority queue is a list.
    value = priority_queue.pop(0) # popping the first element of the list
    return value


def convert_list(lst):
# converting list of tuples to list of lists
    new_list = []
    for i in lst:
        new_list.append(list(i))
    return new_list






