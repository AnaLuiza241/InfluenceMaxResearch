from funcoes import *
from backbone import *

if __name__ == '__main__':
    
    # Leitura das redes
    nome_redes = ['gnn-edge-betweenness/redes/fb-pages-food.edges',
                  'gnn-edge-betweenness/redes/fb-pages-politician.edges',
                  'gnn-edge-betweenness/redes/fb-pages-artist.edges']
    #redes = read_networks(nome_redes)
    #print(redes)

    # Calculo do edge betweenness para as redes
    #real_edge_bc, real_time_taken = node_betweenness_networks(redes)
    #print(real_time_taken)
    #update_node_metrics(redes)
    k = [15, 15, 20]
    proportion = 0.1
    #maxInfluenceBackbone(redes, k, proportion)

    g = nx.read_edgelist(nome_redes[1], delimiter=',')
    print()

    evaluate_network_with_forced_backbone(g, k[1], proportion)

    # s_edge_bc, s_time_taken = propose_model(redes[0])
    #print(s_time_taken)

