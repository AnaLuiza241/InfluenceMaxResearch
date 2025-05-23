

def independent_cascade (graph, seed, p,):
    L = s.copy()



# Select some nodes as the initial actived nodes, which are Seeds;
# The propagation of an edge will be successfully cascaded with the probability q/in_degree_of_target, where q is a hyper parameter called threshold (we always set it to 0.2, 0.4, 0.6, 0.8, or 1.0);
# In each round, the propagation will be cascaded only once, and the active nodes in the round will be set to actived node, which would not cascade to other ndoes any more, even the nodes did not cascade to any other nodes.
# Keep cascading, until there is no nodes can active others. At this time, the number of actived nodes are the final incluence number.