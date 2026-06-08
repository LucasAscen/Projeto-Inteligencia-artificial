
# Algoritmo Genérico para o 8-puzzle

import random, time
from puzzle import apply_sequence, manhattan, MOVES

def fitness(ind, init): #funçao fitness,(individuo, estado inicial), quanto menor a nota melhor o individuo
    final, valid = apply_sequence(init, ind) #simula todos os movimentos 
    return manhattan(final) + (len(ind) - valid) * 0.3 #adiciona uma penalidade para movimentos inválidos(bater na parede)

def genetic_algorithm(init, pop_size=300, seq_len=120, max_gen=2000,#criando populaçao
                       pc=0.85, pm=0.03, elitism=10):
    pop  = [[random.choice(MOVES) for _ in range(seq_len)] for _ in range(pop_size)]
    best, best_fit = None, float('inf')# a gente guarda o melhor individuo e a melhor nota, inicialmente é infinito pq queremos minimizar a nota

    for gen in range(max_gen):
        fits = [fitness(ind, init) for ind in pop]
        idx  = min(range(len(fits)), key=fits.__getitem__)

        if fits[idx] < best_fit:
            best_fit, best = fits[idx], pop[idx][:]
        if best_fit == 0:#distancia de manhattan é 0, ou seja, o estado final foi alcançado
            return best, gen, best_fit

        ranked  = sorted(zip(fits, pop), key=lambda x: x[0])#passa os melhores para a proxima geração
        new_pop = [ind[:] for _, ind in ranked[:elitism]]

        while len(new_pop) < pop_size:
            # Seleção por torneio
            p1 = min(random.sample(pop, 5), key=lambda x: fitness(x, init))
            p2 = min(random.sample(pop, 5), key=lambda x: fitness(x, init))
            # Crossover dois pontos
            a, b = sorted(random.sample(range(1, seq_len), 2))
            c1 = p1[:a] + p2[a:b] + p1[b:]
            c2 = p2[:a] + p1[a:b] + p2[b:]
            # Mutação
            for c in (c1, c2):#com pm de 3% cada movimento tem chance de ser mutado, ou seja, ser substituido por um movimento aleatorio
                for i in range(len(c)):
                    if random.random() < pm:
                        c[i] = random.choice(MOVES)
                if len(new_pop) < pop_size:
                    new_pop.append(c)

        pop = new_pop #retorna a nova população para a próxima geração

    return best, max_gen, best_fit