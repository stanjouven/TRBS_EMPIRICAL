import numpy as np
import networkx as nx
import pandas as pd
import operator
import random


import TRBS_EMPIRICAL.source_estimation as se

'''
Enables to call functions to find the source estimation of the algorithm
PARAMETERS:
    graph: the nx graph used
    obs_time: dictionnary node -> time of the infection
    distribution: distribution used
'''
def trbs_empirical(graph, obs_time_filt, distribution):

    nb_diffusions = int(np.sqrt(len(list(graph.nodes()))))
    obs_filt = np.array(list(obs_time_filt.keys()))

    path_lengths = preprocess(obs_filt, graph, distribution, nb_diffusions)
    print('final path ', path_lengths)

    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time_filt, path_lengths)
    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=False)

    return (s_est, ranked)

'''
Apply the given distribution to the edge of the graph.
PARAMETERS:
    observer: the observer node
    graph: the nx graph used
    distr: the distribution used
Return dictionnary: node -> time to go from that node to the given observer
'''
def preprocess(observer, graph, distr, nb_diffusions):
    path_lengths = initialize_dataframe(observer)
    i = 0
    for diff in range(nb_diffusions):
        ### Initialization of the edge delay
        edges = graph.edges()
        for (u, v) in edges:
            graph[u][v]['weight'] = graph[u][v]['weight'] + abs(distr.rvs())
        for o in observer:
            ### Computation of the shortest paths from every observer to all other nodes
            path_lengths[str(o)] += pd.Series(nx.single_source_dijkstra_path_length(graph, o))
        if i == 0:
            print('path 1 ',path_lengths.to_dict())
        i = i + 1
    path_lengths = path_lengths / len(observer)
    return path_lengths.to_dict()



def initialize_dataframe(observer):
    path_lengths = pd.DataFrame()
    for o in observer:
        path_lengths[str(o)] = 0
    return path_lengths
