import copy
import random


def get_input(problem_file_name):
    """
    :param problem_file_name: input file name .txt
    :return: node_name_list, path_list, prob_table_list, query_list
    """
    with open(problem_file_name) as f:
        lines = f.readlines()
    node_name_list = []
    path_list = []
    prob_tables_list = []
    query_list = []
    step = ''
    # read lines and store bayes net nodes
    # path list, probability table list
    # and query as a list as string values
    for i, line in enumerate(lines):
        if line == "[BayesNetNodes]\n":
            step = 'Nodes'
            continue
        if line == "[Paths]\n":
            step = 'Paths'
            continue
        if line == "[ProbabilityTable]\n":
            step = 'PTable'
            continue
        if line == "[Query]\n":
            step = 'Query'
            continue
        line = line.strip()
        if step == "Nodes":
            node_name_list.append(line)
        elif step == "Paths":
            path_list.append(eval(line))
        elif step == "PTable":
            prob_tables_list.append(eval(line))
        elif step == "Query":
            query_list.append(eval(line))
    return node_name_list, path_list, prob_tables_list, query_list


class Node():
    # A class that represents Bayes Network Node
    # holds, node name, parent and node's children
    def __init__(self, name):
        self.name = name
        self.parent = []
        self.children = []
        self.prob_table = []  # key = (node, parents' values-TRUE-FALSE), value = probability

    def add_parent(self, parent):
        # I gave parent argument as a list to this function accidentally, so node.parent holds [[parents]]
        self.parent.append(parent)

    def add_child(self, child):
        self.children.append(child)

    def add_prob_table(self, prob_table):
        # prob_table argument is a dict of probabilty values of the node given parent states
        self.prob_table.append(prob_table)

    def __str__(self):
        # function to print the node
        ret = "node:" + str(self.name) + " parent: " + str(
            self.parent if self.parent else "none"
            ) + " children:" + str(self.children) + " probtable:" + str(self.prob_table) + "\n"
        return ret


def get_negative_values(dict):
    # while constructing probability tables, in order to get the values of (1-proability)
    d = dict.copy()
    for elem in d:
        d[elem] = round(1 - d[elem], 3)
    return d


def prior_probability_tables(prob_list):
    """
    construct prior probability tables
    :param prob_list: list of probabilities given
    :return: dictionary including prior probabilities (key: name of the node-T/F, value: probability
    """
    prior_dict = {}
    for i in prob_list:
        if not i[1]:
            num = i[2].pop()
            prior_dict[(i[0], True)] = num
            prior_dict[(i[0], False)] = float(1 - num)
    return prior_dict


def conditional_probability_tables(prob_list):
    """
     construct conditional probability tables
    :param prob_list: list of probabilities given
    :return: dictionary including conditional probabilities (key: name of the node-T/F, value: parents' values and conditional prob values
    """
    conditional_dict = {}
    for i in prob_list:
        if i[1]:
            conditional_dict[(i[0], True)] = i[2]
            conditional_dict[(i[0], False)] = get_negative_values(i[2])

    return conditional_dict


def construct_network(node_name_list, path_list, prob_tables_list):
    """
     construct bayesnetwork
    :param node_name_list: name of the nodes given
    :param path_list: list of paths given
    :param prob_tables_list: prob tables list given
    :return: list including all the nodes
    """
    list_of_nodes = []
    prior_probabilities = prior_probability_tables(prob_tables_list)
    conditional_probabilities = conditional_probability_tables(prob_tables_list)

    for node in node_name_list:
        # add names
        e = Node(node)
        list_of_nodes.append(e)

    for path in path_list:
        # add parents
        for node in list_of_nodes:
            if path[1] == node.name:
                node.add_parent(path[0])

    for path in path_list:
        # add children
        temp = path[0]
        for elem in temp:
            for node in list_of_nodes:
                if elem == node.name:
                    node.add_child(path[1])

    for key in prior_probabilities:
        # add prior probabilities
        for node in list_of_nodes:
            if node.name == key[0]:
                node.add_prob_table({key: prior_probabilities[key]})

    for key in conditional_probabilities:
        # add conditional probabilities
        for node in list_of_nodes:
            if node.name == key[0]:
                node.add_prob_table({key: conditional_probabilities[key]})
    return list_of_nodes


def get_value(node, observed):
    # function to use inside enum_all in order to get probabilty value of a node
    # given observed states of its parents
    # there is 3 conditions to get the probabilty
    # The reason behind I need 3 if conditions to get probabilty of the node is
    # I'm storing the probabilities in different formats for no parent case, 1 parent case and more than 1 parent case
    if not node.parent:
        for elem in node.prob_table:
            if (node.name, True) in elem:
                prob = elem[(node.name, True)]
    else:
        parents = tuple(observed[par] for par in node.parent[0])
        if len(parents) == 1:
            for elem in node.prob_table:
                if (node.name, True) in elem:
                    prob = elem[(node.name, True)][parents[0]]
        if len(parents) >= 2:
            for elem in node.prob_table:
                if (node.name, True) in elem:
                    prob = elem[(node.name, True)][parents]
    #we get the True probability of given node, if its False in observed then we extract it from 1
    if not observed[node.name]:
        prob = round(1 - prob, 3)
    return prob


def enum_all(nodes, observed):
    # base condition
    if not nodes:
        return 1

    # if front element of bayesian network  is in observed
    # then we know its observed, we can call get_value and recursively call itself with rest of the variables(nodes)
    y = nodes[0]
    if y.name in observed:
        return get_value(y, observed) * enum_all(nodes[1:], observed)
    else:
        # we know that y is not observed so we are getting the sum of both True and False probabilty values
        # and return it
        probs = []
        for condition in [True, False]:
            new_observed = copy.deepcopy(observed)
            new_observed.setdefault(y.name, condition)
            probs.append(get_value(y, new_observed) * enum_all(nodes[1:], new_observed))
        return sum(probs)


def enum_ask(query, observed, nodes):
    """

    :param query: query variable that we need to calculate probability
    :param observed: observed states(evidence)
    :param nodes: list of nodes, bayes network
    :return:
    """
    q = []
    for condition in [True, False]:
        # calculate probabilty for both True and False values of query variable
        new_observed = copy.deepcopy(observed)
        new_observed.setdefault(query, condition)
        prob = enum_all(nodes, new_observed)
        q.append(prob)
    return normalize(q)


def normalize(q):
    """
    :param q: takes a tuple
    :return: a tuple
    """
    total = q[0] + q[1]
    q[0] = q[0] / total
    q[1] = q[1] / total
    return round(q[0], 3), round(q[1], 3)


def sample(X, e, bn):
    # X is just the variable name,
    # First I find the node from bayes net
    node = None
    for n in bn:
        if n.name == X:
            node = n

    Q = {} # probabilities
    # calculate both True and False probability for node with variable name = X
    for xi in [True, False]:
        ei = {**e, X:xi} # copy state and add node_name:True or node_name:False

        # calculate probabilty with new state
        prob = get_value(node, ei)
        for child in node.children:
            for n in bn:
                if n.name == child:
                    prob *= get_value(n, ei)
        # add calculated probabilty to Q
        Q[xi] = prob

    # Normalize
    total = Q[True] + Q[False]
    Q[True] /= total
    Q[False] /= total

    return random.random() < Q[True]

def gibbs(X, e, bn, N):

    """
    :param X: query variable
    :param e: observed
    :param bn: list of nodes
    :param N: iteration count
    :return:
    """
    random.seed(10)
    counts = {x: 0 for x in [True, False]} # True and False counts after sampling
    Z = [var.name for var in bn if var.name not in e] # non evidence variables
    state = copy.deepcopy(e)

    for Zi in Z:
        # randomly select state values for non evidence variables
        state.setdefault(Zi, random.choice([True, False]))

    for j in range(N):
        for Zi in Z:
            # change the state iteratively for every item in Z and continue sampling until hitting the N
            state[Zi] = sample(Zi, state, bn)
            counts[state[X]] += 1
    # returns True/Total, False/Total
    return counts[True]/(counts[True]+counts[False]), counts[False]/(counts[True]+counts[False])


def DoInference(method_name, problem_file_name, num_iteration):
    results = get_input(problem_file_name)
    node_name_list = results[0]
    path_list = results[1]
    prob_tables_list = results[2]
    query_list = results[3]
    list_of_nodes = construct_network(node_name_list, path_list, prob_tables_list)
    if method_name == "ENUMERATION":
        result = enum_ask(query_list[0][0], query_list[0][1], list_of_nodes)
    else:
        result = gibbs(query_list[0][0], query_list[0][1], list_of_nodes, num_iteration)
    return result
