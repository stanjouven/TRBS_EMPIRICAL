import networkx as nx
import numpy as np
import collections

'''
Estimation of the true source according to the paper
PARAMETERS:
    graph: graph containing mean weights
    obs_time: dictionnary: node -> time
    path_lengths: dictionnary of dictionnary: {obs: {node: length}}
RETURN:
    source_candidates: source(s) estimation
    var_T: dictionnary: {node: var} for every node
'''
def source_estimate(graph, obs_time, path_lengths):
    T = collections.defaultdict(list)
    var_T = {}
    for node in list(graph.nodes()):
        for obs in np.array(list(obs_time.keys())):
            T[node].append(obs_time[obs] - path_lengths[str(obs)][node])
        var_T[node] = np.var(T[node])

    scores = sorted(var_T.items(), key=operator.itemgetter(1), reverse=False)
    source_candidate = scores[0][0]

    return source_candidate, scores
