class TreeNode:
    """
    class for nodes of the tree.
    """
    def __init__(self, value, parent, utility, level):
        """
        :param value: list, the state of the piles. Ex: [1,3,5] is the value of the root node according to the first input file.
        :param parent: TreeNode, parent node of the current node
        :param utility: 1 or -1. The utilities that a node can be assigned.
        :param level: the depth of the node in the tree. Ex: root node's level is 1 (depth 1) while its children's level is 2 (depth 2)
        """
        self.children = []
        self.parent = parent
        self.value = value
        self.utility = utility
        self.level = level

    def __str__(self, level=0):
        #function to print the tree
        ret = level * "\t" + str(self.value)  + " parent: " + str(self.parent.value if self.parent else "none") + \
              " utility:" + str(self.utility) + " level:" + str(self.level) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def construct_tree(node):
    """
    Given the root node, this function constructs the tree while finding the root nodes and assigning them their utilities based on
    which player's turn it is.
    :param node: root node: node that in which construction begins.
    """
    value = node.value  # store the value of the node meaning the state of the piles
    if value is None: # check if value is None
        return None
    else:  # if the value is not None, continue constructing
        for i in range(len(value)): # constructing the tree in the order as written in the pdf.
            temp = value.copy()
            counter = 0
            limit = temp[i]
            while counter < limit:
                new_value = temp.copy()
                new_value[i] = counter
                tree = TreeNode(new_value, node, None, node.level+1)
                counter = counter + 1
                node.children.append(tree)
        for child in node.children:
            # while recursively calling the construct_tree function for each child of the given node, function finds terminal nodes of the tree
            # if maximizer the terminal nodes are + 1
            # if minimizer the terminal nodes are -1
            if sum(child.value) == 0: # terminal nodes
                # since we know that the game will be started with MAX player, we can decide which level is minimizer while the other one is maximizer.
                # since the we know root is the MAX player, we can say that the even levels are MIN while the odd levels are MAX. Because they will play one by one.
                if child.level % 2 == 0: # if minimizer (even levels -depth-), the terminal nodes are -1.
                    child.utility = -1
                else:   # if child.level % 2 != 0: if maximizer (odd levels -depth-), the terminal nodes are 1. -
                    child.utility = 1
            else:
                construct_tree(child)
    return node


def minimax(node):
    """
    :param node: tree that we constructed
    :return: find_utility(node) function
    """
    if node.level == 0:
        return node.value, None

    def find_utility(node):
        """
        minimax algorithm applied here:
        :return: best possible node to move after (root's best child in this case) and its utility pair
        """
        if not node.children: #if terminal nodes, return that node's state(value) and its utility (-1 or 1)
            return node.value, node.utility
        possible_nodes =[]
        for child in node.children:
            v=find_utility(child)
            possible_nodes.append((child, v[1])) #adds to the list with child node and its utility

        if node.level % 2 != 0: #max condition (same reason as in the construct_tree function)
            start = float("-inf")
            max_node = max(possible_nodes, key=lambda item:item[1]) # finds the node with the max utility (while comparing utilities).
            if max(start, max_node[1]) == max_node[1]:
                return max_node #node itself and its utility pair
        if node.level % 2 == 0: #min condition (same reason as in the construct_tree function)
            start = float("inf")
            min_node = min(possible_nodes, key=lambda item:item[1]) # finds the node with the min utility (while comparing utilities).
            if min(start, min_node[1]) == min_node[1]:
                return min_node #node itself and its utility pair
    return find_utility(node)


visited = [] # global variable to keep the nodes that we visited in the alpha beta
def alpha_beta(node):
    """
    :param node: tree that we constructed
    :return: find_utility(node) function
    """
    if node.level == 0:
        return node.value, 1

    def find_utility(node, alpha = -1, beta = 1):
        """
        alphabeta algorithm applied here
        :param alpha: alpha represents the minimum score that the maximizing player is ensured.
        Since in this game, we know that the min possible value is -1, we can give it directly.
        :param beta: beta will represent the maximum score that the minimizing player is ensured.
         Since in this game, we know that the max possible value is 1, we can give it directly.
        :return: best possible node to move after (root's best child in this case) and its utility pair
        """
        global visited
        if not node.children: # if terminal nodes, return that node's state(value) and its utility (-1 or 1)
            visited.append(node) #append the nodes that we visited
            return node.value, node.utility
        possible_nodes =[]
        visited.append(node) #append the nodes that we visited
        for child in node.children:
            v=find_utility(child, alpha, beta)
            possible_nodes.append((child, v[1]))
            if node.level % 2 != 0: # maximizer
                alpha = max(alpha, v[1]) # compare with alpha, and take the max value
            else: # minimizer
                beta = min(v[1], beta) # compare with beta, and take the min value
            if beta <= alpha: # break condition - if we break, we do not continue exploring that node's children.
                break
        if node.level % 2 != 0: #max condition
            max_node = max(possible_nodes, key=lambda item:item[1]) #based on utility, maximizer
            return max_node
        if node.level % 2 == 0: #min condition
            min_node = min(possible_nodes, key=lambda item:item[1]) #minimizer, based on utility
            return min_node
    return find_utility(node)


def find_node_count_minimax(node):
    """
    to count the nodes that we expanded in minimax. (we give the node coming from the result of minimax function, in this case)
    :param node: tree
    :return: count of the nodes
    """
    if node is None:
        return None
    if not node.children:
        return 1
    else:
        queue = [] # a basic BFS algorithm to count the nodes in the given tree
        queue.append(node)
        count = 0
        while queue:
            value = queue.pop(0)
            for child in value.children:
                count += 1
                queue.append(child)
    return count


def find_node_count_alphabeta(node):
    """
    to count the nodes that we expanded in the alphabeta. (we give the node coming from the result of minimax function, in this case)
    :param node: tree
    :return: count of nodes
    """
    global visited # list that we append all the nodes that we expanded while running the alphabeta algorithm (above)
    if node is None:
        return None
    else:
        queue = []
        queue.append(node)
        count = 0
        while queue:
            value = queue.pop(0)
            for child in value.children:
                if child in visited: # if that node is visited in the alphabeta, we count. Else, we skip.
                    count += 1
                queue.append(child)
    return count


def SolveGame(method_name, problem_file_name, player_type):
    """
    :param method_name: "Minimax" or "AlphaBeta"
    :param problem_file_name: input file .txt
    :param player_type: "MAX" or "MIN"; however, in this game we know that only MAX player will be given.
    :return: ([((best possible node to move after the root), count of the expanded nodes]) EX: ([(1, 3, 2), 446]) for the root [1 ,3 ,5].
    """
    f = open(problem_file_name, "r") #read input file
    root = eval(f.readline())
    tree = TreeNode(root, None, None, 1) #define root
    construct_tree(tree) #construct the tree
    if method_name == "Minimax" and player_type == "MAX": # for minimax, call the minimax function
        result_minimax = minimax(tree)[0] # keep the results first element which is the best possible node to move after
        node_count = find_node_count_minimax(result_minimax) # count the expanded nodes coming from the result of the minimax
        res = '(' + str([tuple(result_minimax.value), node_count]) + ')' # just to keep the format as given in the pdf
        return res
    if method_name == "AlphaBeta" and player_type == "MAX": # same as above
        result_alphabeta = alpha_beta(tree)[0]
        node_count = find_node_count_alphabeta(result_alphabeta)
        res = '(' + str([tuple(result_alphabeta.value), node_count]) + ')'
        return res


