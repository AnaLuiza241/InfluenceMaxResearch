from funcoes import *

if __name__ == '__main__':
    
    # Leitura das redes
    nome_redes = ["gnn-edge-betweenness/redes/fb-pages-food.edges"]
    redes = read_networks(nome_redes)
    #print(redes)

    # Calculo do edge betweenness para as redes
    real_edge_bc, real_time_taken = edge_betweenness_networks(redes)
    print(real_time_taken)

    s_edge_bc, s_time_taken = propose_model(redes[0])
    print(s_time_taken)

