import networkx as nx
import time
import random
import pandas as pd
import os

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

def edge_betweenness_networks (networks, output_dir='gnn-edge-betweenness/csv_results'):
    times  = []
    betweenness = []

    execution_times_csv = f'{output_dir}/execution_times.csv'

    pd.DataFrame(columns=["network", "time"]).to_csv(execution_times_csv, index=False)
    

    for i, net in enumerate(networks):
        start_time = time.time()

        bc = nx.edge_betweenness_centrality(net)
        betweenness.append(bc)

        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        
        execution_times_df = pd.DataFrame([{'network': f'network_{i+1}', 'time': elapsed_time}])
        execution_times_df.to_csv(execution_times_csv, mode='a',header=False, index=False)

        bet_df = pd.DataFrame(
            [(u, v, value) for (u, v), value in bc.items()],
            columns=['no_saida', 'no_entrada', 'betweenness']
        )
        bet_csv = f'{output_dir}/network_{i+1}_betweenness.csv'
        bet_df.to_csv(bet_csv, index=False)

        print(f'Fim execução {i}')

    return betweenness, times

def node_betweenness_networks(networks, output_dir='gnn-edge-betweenness/csv_results'):
    times = []
    betweenness = []
    
    execution_times_csv = f"{output_dir}/execution_times.csv"
    
    pd.DataFrame(columns=["network", "time"]).to_csv(execution_times_csv, index=False)
    
    for i, net in enumerate(networks):
        start_time = time.time()
        
        # Calcula a centralidade de intermediação dos nós
        bc = nx.betweenness_centrality(net)
        betweenness.append(bc)
        
        # Calcula o tempo de execução
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        
        # Atualiza o arquivo de tempos de execução
        execution_times_df = pd.DataFrame([{"network": f"network_{i+1}", "time": elapsed_time}])
        execution_times_df.to_csv(execution_times_csv, mode='a', header=False, index=False)
        
        # Salva os dados de centralidade em um CSV usando pandas
        betweenness_df = pd.DataFrame(
            [(node, value) for node, value in bc.items()],
            columns=["nó", "betweenness"]
        )
        betweenness_csv = f"{output_dir}/network_{i+1}_betweenness.csv"
        betweenness_df.to_csv(betweenness_csv, index=False)
    
    return betweenness, times


def update_node_metrics(networks, output_dir='gnn-edge-betweenness/csv_results'):
    for i, net in enumerate(networks):
        # Caminho do CSV existente para a rede atual
        betweenness_csv = f"{output_dir}/network_{i+1}_betweenness.csv"
        
        if not os.path.exists(betweenness_csv):
            print(f"Arquivo {betweenness_csv} não encontrado. Pulando...")
            continue
        
        # Lê o CSV existente
        betweenness_df = pd.read_csv(betweenness_csv)
        
        # Certifica-se de que a coluna "nó" está no mesmo tipo usado no grafo
        if betweenness_df["nó"].dtype != type(list(net.nodes())[0]):
            betweenness_df["nó"] = betweenness_df["nó"].astype(str if isinstance(list(net.nodes())[0], str) else int)
        
        # Calcula as métricas adicionais
        degrees = dict(net.degree())  # Grau de cada nó
        clustering = nx.clustering(net)  # Coeficiente de aglomeração
        
        # Adiciona novas colunas ao DataFrame
        betweenness_df["degree"] = betweenness_df["nó"].map(degrees)
        betweenness_df["clustering"] = betweenness_df["nó"].map(clustering)
        
        # Salva o CSV atualizado
        betweenness_df.to_csv(betweenness_csv, index=False)
        print(f"Métricas atualizadas no arquivo: {betweenness_csv}")


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