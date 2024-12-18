import networkx as nx
import matplotlib.pyplot as plt
import random

# Gerar uma rede pequena com 30 nós usando o modelo Barabási-Albert (preferential attachment)
n_nodes = 30
m_edges = 2  # Número de arestas adicionadas por nó
G = nx.barabasi_albert_graph(n_nodes, m_edges)

# Definir o layout dos nós
pos = nx.spring_layout(G, seed=42)  # Usa layout de força para melhor visualização

# Plotar o grafo
plt.figure(figsize=(8, 6))
nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_size=500, 
    node_color="skyblue", 
    edge_color="gray", 
    font_size=10
)
plt.title("Exemplo de Rede Complexa com 30 Nós", fontsize=14)
plt.show()

# Definir o layout dos nós
pos = nx.spring_layout(G, seed=42)

# Classificar os nós aleatoriamente em três grupos
nodes = list(G.nodes)
random.seed(42)  # Para garantir reprodutibilidade
red_nodes = random.sample(nodes, 5)  # Seleciona 5 nós aleatórios para serem vermelhos
remaining_nodes = [node for node in nodes if node not in red_nodes]
blue_nodes = random.sample(remaining_nodes, 18)  # Seleciona 18 para serem azuis
black_nodes = [node for node in remaining_nodes if node not in blue_nodes]  # O resto será preto

# Definir as cores dos nós
node_colors = []
for node in G.nodes:
    if node in red_nodes:
        node_colors.append("red")
    elif node in blue_nodes:
        node_colors.append("blue")
    else:
        node_colors.append("black")

# Plotar o grafo
plt.figure(figsize=(8, 6))
nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_size=500, 
    node_color=node_colors, 
    edge_color="gray", 
    font_size=10
)
plt.title("Exemplo de Rede Complexa com Nós Coloridos", fontsize=14)
plt.show()
