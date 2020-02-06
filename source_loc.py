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
    obs_time: dictionnary {node: time of the infection}
    distribution: distribution used
RETURN:
    s_est: estimation of the true source
    ranked: sorted(in decreasing order) list of tuple (node, value in which we do the estimation)
'''
def trbs_empirical(graph, obs_time_filt, distribution):

    nb_diffusions = int(np.sqrt(len(list(graph.nodes()))))
    obs_filt = np.array(list(obs_time_filt.keys()))

    path_lengths = preprocess(obs_filt, graph, distribution, nb_diffusions)
    path_lengths = compute_mean_shortest_path(path_lengths)

    ### Run the estimation
    s_est, scores = se.source_estimate(graph, obs_time_filt, path_lengths)

    return (s_est, scores)

'''
Apply the given distribution to the edge of the graph and then create a dataframe to store
shortest path from every observer to every nodes in the graph
PARAMETERS:
    observer: the observer node
    graph: the nx graph used
    distr: the distribution used
    nb_diffusions: (int) number of time we do the diffusion
Return pandas.DataFrame
'''
def preprocess(observer, graph, distr, nb_diffusions):
    path_lengths = pd.DataFrame()
    for diff in range(nb_diffusions):
        path_lengths_temp = pd.DataFrame()
        ### edge delay
        edges = graph.edges()
        for (u, v) in edges:
            graph[u][v]['weight'] = abs(distr.rvs())
        for o in observer:
            ### Computation of the shortest paths from every observer to all other nodes
            path_lengths_temp[str(o)] = pd.Series(nx.single_source_dijkstra_path_length(graph, o))
        path_lengths = path_lengths.append(path_lengths_temp)
    return path_lengths


'''
Compute the mean shortest path of every diffusion
PARAMETERS:
    path_lengths:(pandas.DataFrame) containing all shortest path from every diffusion
RETURN: dictionnary of dictionnary: {obs: {node: mean length}}
'''
def compute_mean_shortest_path(path_lengths):
    path_lengths.reset_index(inplace = True)
    path_lengths = path_lengths.rename({'index': 'node'}, axis = 1).set_index('node')
    return path_lengths.groupby(['node']).mean().to_dict()
