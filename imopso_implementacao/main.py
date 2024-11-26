from funcoes import *
import networkx as nx
import numpy as np

# Definir funções de múltiplos objetivos
def objective1(xid):
    # Exemplo: Função que minimiza a soma dos elementos do vetor xid
    return sum(xid)

def objective2(xid):
    # Exemplo: Função que maximiza a quantidade de elementos "1" em xid
    return len(xid) - sum(xid)

# Criar um grafo de exemplo
G = nx.erdos_renyi_graph(10, 0.5)  # Grafo aleatório com 10 nós e probabilidade de conexão 0.5
N = 5  # Número de partículas no enxame
MaxIt = 10  # Número máximo de iterações
w = 0.5  # Inércia
c1, c2 = 1.5, 1.5  # Fatores de aprendizado
mult_funcs = [objective1, objective2]  # Lista das funções de múltiplos objetivos

# Executar o algoritmo
non_dominated_solutions = imopso_for_lcim(G, N, MaxIt, w, c1, c2, mult_funcs)

# Exibir as soluções não-dominadas
print("Soluções não-dominadas encontradas:")
for solution in non_dominated_solutions:
    print(solution)
