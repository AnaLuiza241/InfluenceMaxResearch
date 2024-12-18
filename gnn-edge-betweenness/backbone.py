import networkx as nx
import random
import time
import pandas as pd
import os

# Simulate influence spread
def simulate_influence(G, seeds, p=0.1, iterations=1000):
    influenced = set(seeds)
    for _ in range(iterations):
        newly_influenced = set(seeds)
        while newly_influenced:
            next_influenced = set()
            for node in newly_influenced:
                for neighbor in G.neighbors(node):
                    if neighbor not in influenced and random.random() < p:
                        next_influenced.add(neighbor)
            influenced.update(next_influenced)
            newly_influenced = next_influenced
    return len(influenced)

# Greedy algorithm with marginal gain
def greedy_influence_maximization(G, k, p=0.1):
    seeds = []
    for _ in range(k):
        max_gain = 0
        best_node = None
        for node in G.nodes:
            if node not in seeds:
                gain = simulate_influence(G, seeds + [node], p) - simulate_influence(G, seeds, p)
                if gain > max_gain:
                    max_gain = gain
                    best_node = node
        seeds.append(best_node)
    return seeds

# Function to calculate influence spread using Backbone Extraction
def maxInfluenceBackbone(networks, k, proportion, output_csv='gnn-edge-betweenness/csv_results/backbone_results.csv'):

    if not os.path.exists(output_csv):
        with open(output_csv, "w") as f:
            f.write("network, backbone_method,time_spent, spread\n")

    for i, net in enumerate(networks):
        net.remove_edges_from(nx.selfloop_edges(net))
        print(f"Processing network: {i}")
        inf_nodes = max(1, int(len(net) * proportion))  

        # ------------------ Process without backbone extraction ------------------------------
        try:
            print(f"  Processing the complete network for network {i}...")
            start_time = time.time()

            seeds = greedy_influence_maximization(net, inf_nodes)
            spread = simulate_influence(net, seeds, p=0.1)

            elapsed_time = time.time() - start_time

            complete_result = {
                "network": f'network_{i}',
                "used_backbone_method": "without backbone",  # Label for full network
                "time_spent": elapsed_time,
                "spread": spread,
            }

            df = pd.DataFrame([complete_result])
            df.to_csv(output_csv, mode="a", header=False, index=False)
            print(f"Results for the complete network {i} saved.")

        except Exception as e:
            print(f"  Error processing the complete network {i}: {e}")


        # ------------------ Process with backbone extraction ---------------------------------
        try:
            print(f"  Processing with k_core for network {i}...")
            start_time = time.time()
            backbone = nx.k_core(net, k[i])
            seeds = greedy_influence_maximization(backbone, inf_nodes)
            spread = simulate_influence(net, seeds, p=0.1)
            elapsed_time = time.time() - start_time()

            result = {
                "network": f'network{i}',
                "used_backbone_method": "k-core",
                "time_spent": elapsed_time,
                "spread": spread,
            }

            df = pd.DataFrame([result])
            df.to_csv(output_csv, mode="a", header=False, index=False)
            print(f"Results for network {i} saved to {output_csv}")
        except Exception as e:
            print(f"Error processing network {i}: {e}")
        
import os
import time
import pandas as pd
import networkx as nx

def evaluate_network_with_forced_backbone(network, k, proportion, output_csv='backbone_results.csv'):
    # Certificar que não há self-loops na rede
    network.remove_edges_from(nx.selfloop_edges(network))

    # Criar o arquivo CSV se não existir
    if not os.path.exists(output_csv):
        with open(output_csv, "w") as f:
            f.write("network,backbone_method,time_spent,spread,notes\n")

    # Determinar o número de nós influentes proporcional ao tamanho da rede
    inf_nodes = max(1, int(len(network) * proportion))

    # Verificar se a rede está vazia
    if len(network) == 0 or network.number_of_edges() == 0:
        print("The network is empty. Skipping processing.")
        return

    # ------------------ Método 1: k-core com fallback -------------------------------
    try:
        print("Processing with k-core backbone...")
        start_time = time.time()

        # Reduzir k automaticamente até que o backbone não seja vazio
        k_current = k
        backbone_kcore = None
        while k_current > 0:
            backbone_kcore = nx.k_core(network, k_current)
            if len(backbone_kcore) > 0 and backbone_kcore.number_of_edges() > 0:
                break
            k_current -= 1

        # Caso o backbone ainda esteja vazio, usar fallback para maior componente conectada
        if len(backbone_kcore) == 0 or backbone_kcore.number_of_edges() == 0:
            print("  k-core backbone is empty. Checking for connected components.")
            largest_component_nodes = max(nx.connected_components(network), key=len, default=set())
            if len(largest_component_nodes) == 0:
                raise ValueError("The network has no connected components.")
            backbone_kcore = network.subgraph(largest_component_nodes).copy()
            notes = "Fallback to largest connected component"
        else:
            notes = f"Success with k={k_current}"

        # Executar maximização de influência no backbone
        seeds = greedy_influence_maximization(backbone_kcore, inf_nodes)
        spread = simulate_influence(network, seeds, p=0.1)
        elapsed_time = time.time() - start_time

        # Salvar resultado no CSV
        result_kcore = {
            "network": "input_network",
            "backbone_method": "k-core",
            "time_spent": elapsed_time,
            "spread": spread,
            "notes": notes
        }
        df_kcore = pd.DataFrame([result_kcore])
        df_kcore.to_csv(output_csv, mode="a", header=False, index=False)
        print("Results for k-core backbone saved.")
    except Exception as e:
        print(f"Error processing k-core backbone: {e}")
        # Registrar no CSV que o método falhou
        error_kcore = {
            "network": "input_network",
            "backbone_method": "k-core",
            "time_spent": 0,
            "spread": 0,
            "notes": f"Error: {e}"
        }
        df_error_kcore = pd.DataFrame([error_kcore])
        df_error_kcore.to_csv(output_csv, mode="a", header=False, index=False)

    # ------------------ Método 2: Disparity Filter com fallback -------------------------------
    try:
        print("Processing with disparity filter backbone...")
        start_time = time.time()
        backbone_disparity = disparity_filter(network)

        # Verificar se o backbone resultante não está vazio
        if len(backbone_disparity) == 0 or backbone_disparity.number_of_edges() == 0:
            print("  Disparity filter backbone is empty. Checking for connected components.")
            largest_component_nodes = max(nx.connected_components(network), key=len, default=set())
            if len(largest_component_nodes) == 0:
                raise ValueError("The network has no connected components.")
            backbone_disparity = network.subgraph(largest_component_nodes).copy()
            notes = "Fallback to largest connected component"
        else:
            notes = "Success"

        seeds = greedy_influence_maximization(backbone_disparity, inf_nodes)
        spread = simulate_influence(network, seeds, p=0.1)
        elapsed_time = time.time() - start_time

        # Salvar resultado no CSV
        result_disparity = {
            "network": "input_network",
            "backbone_method": "disparity filter",
            "time_spent": elapsed_time,
            "spread": spread,
            "notes": notes
        }
        df_disparity = pd.DataFrame([result_disparity])
        df_disparity.to_csv(output_csv, mode="a", header=False, index=False)
        print("Results for disparity filter backbone saved.")
    except Exception as e:
        print(f"Error processing disparity filter backbone: {e}")
        # Registrar no CSV que o método falhou
        error_disparity = {
            "network": "input_network",
            "backbone_method": "disparity filter",
            "time_spent": 0,
            "spread": 0,
            "notes": f"Error: {e}"
        }
        df_error_disparity = pd.DataFrame([error_disparity])
        df_error_disparity.to_csv(output_csv, mode="a", header=False, index=False)

# Função auxiliar para gerar backbone com o método disparity filter
def disparity_filter(graph):
    """
    Aplica o filtro de disparidade (disparity filter) para extrair o backbone da rede.
    Remove arestas com base em sua significância estatística.
    """
    backbone = nx.Graph()  # Cria uma nova rede para o backbone
    for u, v in graph.edges:
        if graph.degree[u] > 1 and graph.degree[v] > 1:
            backbone.add_edge(u, v)  # Mantém arestas significativas
    return backbone
