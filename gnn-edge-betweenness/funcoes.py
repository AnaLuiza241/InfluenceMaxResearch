import networkx as nx
import time
import random


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

def edge_betweenness_networks (networks):
    times  = []
    betweenness = []
    for net in networks:
        start_time = time.time()
        bc = nx.edge_betweenness_centrality(net)
        betweenness.append(bc)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return betweenness, times


def edge_select (network, tx=0.4):
    if not (0 <= tx <= 1):
        raise ValueError('A porcentagem deve estar entre 0 e 1')
    
    edges = list(network.edges)
    print(len(edges))
    n = max(1, int(tx * len(edges)))
    print(n)
    selected_edges = random.sample(edges, n)
    
    return selected_edges

def edge_selected_betweenness (network, selected_edges):
    bet = {edge: 0.0 for edge in selected_edges}

    return bet

def propose_model(network):
    start_time = time.time()
    selected_edges = edge_select(network)
    bet = edge_selected_betweenness(network, selected_edges)
    t = time.time() - start_time 
    return bet, t