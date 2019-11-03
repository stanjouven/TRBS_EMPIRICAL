import numpy as np
import networkx as nx
import operator
import random

import TRBS.source_estimation as se

'''
Enables to call functions to find the source estimation of the algorithm
PARAMETERS:
    graph: the nx graph used
    obs_time: dictionnary node -> time of the infection
    distribution: distribution used
'''
def trbs(graph, obs_time_filt, distribution):

    #print('obs time', obs_time_filt)

    #largest_graph_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
    #obs_time_filt = observer_filtering(obs_time, largest_graph_cc)
    obs_filt = np.array(list(obs_time_filt.keys()))
    path_lengths = {}
    #nodes = len(list(graph.nodes()))
    #random.sample(range(0, nodes-1), len(obs_filt))

    graph = preprocess(o, graph, distribution)

    for o in obs_filt:
        ### Computation of the shortest paths from every observer to all other nodes
        path_lengths[o] = nx.single_source_dijkstra_path_length(graph, o)


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
def preprocess(observer, graph, distr):
    for o in obs_filt:
        ### Initialization of the edge delay
        edges = graph.edges()
        for (u, v) in edges:
            graph[u][v]['weight'] = graph[u][v]['weight'] + abs(distr.rvs())
    return graph
