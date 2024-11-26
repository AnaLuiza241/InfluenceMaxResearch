import random
import numpy as np
from scipy.stats import levy

# Equação 11 do artigo
def convert_position(xid, vid):
    if vid > random.random():
        return 1 if xid == 0 else 0  
    else:
        return xid  

def initialization(G, N):
    V, E = G[0], G[1]
    v, x, pbest = np.zeros((N,len(V))), np.zeros((N,len(V))), np.zeros((N,len(V)))
    
    # Ordenação dos nós pelo grau
    degrees = [len(list(G.neighbors(node))) for node in G.nodes()]
    listA = sorted(range(len(degrees)), key=lambda k: degrees[k])
    listB = sorted(range(len(degrees)), key=lambda k: degrees[k], reverse=True)
    
    for i in range(N):
        for d in range(len(V)):
            # Inicialização aleatória dos vetores de velocidade, posição e melhor posição pessoal
            v[i][d] = random.random() # velocity vector
            x[i][d] = random.randint(0,1) # position vector
            pbest[i][d] = random.randint(0,1)
            
            # Levy flight para atualização da posição usando a função scipy.stats.levy
            x[i][d] += levy.rvs()
            pbest[i][d] += levy.rvs()

            # Discretização conforme a Equação 11
            x[i][d] = convert_position(x[i][d], v[i][d])
            pbest[i][d] = convert_position(pbest[i][d], v[i][d])

    return v, x, pbest

def fitness(xid, mult_funcs):
    # Avalia o fitness de xid de acordo com as funções mult_objetivo
    return [f(xid) for f in mult_funcs]

def update_velocity(vid, xid, pbest, gbest, w, c1, c2):
    # Equação 2: Atualização de velocidade vid
    r1, r2 = random.random(), random.random()
    new_vid = (w * vid) + (c1 * r1 * (pbest - xid)) + (c2 * r2 * (gbest - xid))
    return new_vid

# G: Grafo; N: Tamanho do Particle Swarm; MaxIt: Número máximo de Iterações; w: Inertia Weight; c1 e c2: Learning Factors; mult_funcs: Multi-objective functions.
def imopso_for_lcim (G, N, MaxIt, w,  c1, c2, mult_funcs):
    iter = 0

    # Inicialização dos vetores de posição, velocidade e pbest
    v, x, pbest = initialization(G, N)

    # Avalia o fitness inicial para cada xid
    pbest_fitness = [fitness(x_i, mult_funcs) for x_i in x]
    gbest = pbest[np.argmin([sum(f) for f in pbest_fitness])]  # Melhor posição global inicial

    # according to the fitness of objective functions
    while iter < MaxIt:
        for i  in range(N):
            for d in range(len(G[0])):  # Percorre os nós do grafo
                # Atualiza a velocidade com Eq.(2)
                v[i][d] = update_velocity(v[i][d], x[i][d], pbest[i][d], gbest[d], w, c1, c2)
                
                # Converte a posição de xid com base na Eq.(11)
                x[i][d] = convert_position(x[i][d], v[i][d])
        
            # Avalia o fitness para o xid atualizado
            current_fitness = fitness(x[i], mult_funcs)

            # Atualiza o pbest e gbest com base na busca local
            if sum(current_fitness) < sum(pbest_fitness[i]):
                pbest[i] = x[i]
                pbest_fitness[i] = current_fitness
                # Se o fitness do pbest[i] for melhor que o gbest, atualiza gbest
                if sum(current_fitness) < sum(fitness(gbest, mult_funcs)):
                    gbest = x[i]
        # Atualiza as soluções não-dominadas
        non_dominated_solutions = [p for p, f in zip(pbest, pbest_fitness) if all(f <= fi for fi in f)]
        iter += 1
    return non_dominated_solutions  # Retorna as soluções não-dominadas ao final
    
