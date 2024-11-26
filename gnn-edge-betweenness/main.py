from funcoes import *

if __name__ == '__main__':
    
    # Leitura das redes
    nome_redes = [r'gnn-edge-betweenness\redes\fb-pages-food.edges']
    redes = read_networks(nome_redes)
    #print(redes)

    # Calculo do edge betweenness para as redes
    edge_bc, time_taken = betweenness_redes(redes)
    print(time_taken)

