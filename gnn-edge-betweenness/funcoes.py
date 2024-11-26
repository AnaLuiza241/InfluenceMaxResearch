import networkx as nx
import time


def read_networks (networks):
    n = []
    i = 0
    for net in networks:
        g = nx.read_edgelist(net, delimiter=',')
        n.append(g)
        print(f'Rede {i}:')
        print(f'Número de Vértices: {g.number_of_nodes()}  Número de arestas: {g.number_of_edges()}')
        i += 1
    
    return n 

def betweenness_redes (networks):
    times  = []
    betweenness = []
    for net in networks:
        start_time = time.time()
        bc = nx.edge_betweenness_centrality(net)
        betweenness.append(bc)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return betweenness, times