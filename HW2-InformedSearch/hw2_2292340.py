def InformedSearch(method_name , problem_file_name) :
    # read file
    with open(problem_file_name) as file:
        lines = file.readlines()
        grid = []
        for line in lines:
            temp = line.replace('\t', '')
            temp2 = temp.replace('\n', '')
            # constructing a proper grid (2d)
            grid.append(temp2)

    obstacle = "#" # define obstacles (where we cannot go in the grid)
    width = len(grid[0]) # define width and height to specify edges of the grid
    height = len(grid)
    start = find_char(grid, "S")  # position of the start point in (y,x) format
    end = find_char(grid, "E") # position of the end point in (y,x) format
    if method_name == "UCS":
        path_ucs = UCS(grid, start, end, obstacle, width, height)
        return reverse_path(path_ucs)
    elif method_name == "AStar":
        path_astar = AStar(grid, start, end, obstacle, width, height)
        return reverse_path(path_astar)


def find_char(grid, char):
    """
    finds the position of a wanted char in the given grid.
    :param grid: 2d grid defined above
    :param char: wanted character
    :return: position of the char in (y,x) format.
    """
    for idx, i in enumerate(grid):
        for idx2, ltr in enumerate(i):
            if ltr == char:
                position = (idx, idx2)
    return position


def UCS(grid, start, end, obstacle, width, height):
    """
    UCS algorithm
    :param grid: 2d grid defined above
    :param start: position of the start point
    :param end: position of the end point
    :param obstacle: chars that we cannot go or move towards (defined above - in this problem it is #)
    :param width: width of the grid
    :param height: height of the grid
    :return: path
    """
    """
    I did not import priority queue, I implemented it. 
    priority queue consists of <cost(manhattan distance between two points), path>
    """
    priority_queue = []
    priority_queue = heappush(priority_queue, (0, [start])) # heappush function is defined below - first element of the queue is the start point
    explored = set() # a set to define points we already visited
    explored.add(start) # first element of the set is the start point
    while priority_queue:
        cost, path = heappop(priority_queue) # heappop is defined below (get cost and the path of the first element of the queue)
        y, x = path[len(path) - 1] # the position of the point that I am currently on (last element of the current path)
        if (y, x) == end: # stop condition
            return path
        for y_new, x_new in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]: # all neighbors of (y,x)
            if 0 <= x_new < width and 0 <= y_new < height and grid[y_new][x_new] != obstacle and (y_new, x_new) not in explored:
                # if condition checks for the neighbors if they are the points that we can go
                totalcost = cost + manhattan_distance(x, x_new, y, y_new) # calculates the total distance(cost) of the current path
                temp = path[:]
                temp.append((y_new, x_new))
                priority_queue = heappush(priority_queue, (totalcost, temp)) # pushing the new path to the priority queue with its cost
                explored.add((y_new, x_new)) # adds the new neighbor to explored since we visited it.
    return None


def AStar(grid, start, end, obstacle, width, height):
    """
        A* algorithm
        :param grid: 2d grid defined above
        :param start: position of the start point
        :param end: position of the end point
        :param obstacle: chars that we cannot go or move towards (defined above - in this problem it is #)
        :param width: width of the grid
        :param height: height of the grid
        :return: path
        """
    """
    priority queue consists of  <f cost (h cost + g cost), g cost (manhattan distance between two points), path>
    explored is dictionary consists of <position of the point as the key (y,x), f cost of that point as the value>
    """
    priority_queue = []
    priority_queue = heappush(priority_queue, (0, 0, [start]))  # priority queue sorting is made on the basis of f cost. heappush defined below.
    explored = {} # set to define points and their costs that we visited before
    explored.setdefault(start, 0)
    while priority_queue: # while the queue is not empty
        f_cost, g_cost, path = heappop(priority_queue) # heappop is defined below (getting the costs and the path of the first element of the queue)
        y, x = path[len(path) - 1] # the position of the point that I am currently on (last element of the current path)
        if (y, x) == end: # stop condition
            return path
        for y_new, x_new in [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]: # for each possible neighbor of (y,x)
            if 0 <= x_new < width and 0 <= y_new < height and grid[y_new][x_new] != obstacle: #controlling condition for the neighbors
                if grid[y_new][x_new] == "E":
                    path.append((y_new, x_new)) # if the neighbor is the end point, stop searching
                    return path
                if grid[y_new][x_new] == "S": # if the neighbor is the start point, continue
                    continue
                else:
                    h_cost = int(grid[y_new][x_new]) # calculating new h_cost which are the values on the grid itself
                    g_cost_new = int(g_cost) + manhattan_distance(x, x_new, y, y_new) # calculating the new total g_cost
                    f_cost_new = g_cost_new + h_cost # new f cost is defined here

                    has_lower_f_value = False # setting a boolean to search for a lower f valued path
                    for item in priority_queue:
                        # for each <fcost, gcost, path> pair, take the path's last element
                        # if it has the same value as my current neighbor with a lower f_cost, continue - do not push it to the priority queue.
                        # meaning: if there is a lower f valued path to that point, I would keep it (not changing).
                        if item[2][-1] == (y_new, x_new) and item[0] < f_cost_new:
                            has_lower_f_value = True # if we found a lower f valued path, this turns true.
                    if has_lower_f_value:
                        continue
                    if (y_new, x_new) in explored and explored[(y_new, x_new)] < f_cost_new:
                        # checking if the current neighbor in explored set with a lower f cost
                        # if it does have, I will keep it too.
                        continue
                    # if no lower f valued path found in priority queue or explored, push it to the priority queue with new costs and new path.
                    temp = path[:]
                    temp.append((y_new, x_new))
                    priority_queue = heappush(priority_queue, (f_cost_new, g_cost_new, temp))
                    # if the key already exists, change its value. Or add new key-value pair.
                    if (y_new, x_new) in explored:
                        explored[(y_new, x_new)] = f_cost_new
                    else:
                        explored.setdefault((y_new, x_new), f_cost_new)
    return None


def manhattan_distance(x, x_new, y, y_new):
    # defined function for calculating manhattan_distance
    distance_y = abs(y_new - y)
    distance_x = abs(x_new - x)
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


def reverse_path(list):
    # takes the final path as a list and reverse it.
    list.reverse()
    # since I keep my tuples as (y,x) format, below returns it to (x,y) format as in the output files. 
    reversed_tuples = [] 
    for i in list:
        new_element = tuple(reversed(i))
        reversed_tuples.append(new_element)
    return reversed_tuples

