
# Algoritmo Genérico para o 8-puzzle

import random, time
from puzzle import apply_sequence, manhattan, MOVES, solvable

def fitness(ind, init): #funçao fitness,(individuo, estado inicial), quanto menor a nota melhor o individuo
    final, valid = apply_sequence(init, ind) #simula todos os movimentos 
    return manhattan(final) + (len(ind) - valid) * 0.3 #adiciona uma penalidade para movimentos inválidos(bater na parede)

def genetic_algorithm(init, pop_size=300, seq_len=120, max_gen=2000,#criando populaçao
                       pc=0.85, pm=0.03, elitism=10):
    if not solvable(init):
        print("Tabuleiro INSOLÚVEL!")
        return None, 0, float('inf')
    pop  = [[random.choice(MOVES) for _ in range(seq_len)] for _ in range(pop_size)]
    best, best_fit = None, float('inf')# a gente guarda o melhor individuo e a melhor nota, inicialmente é infinito pq queremos minimizar a nota

    for gen in range(max_gen):
        # 1. Calcula o fitness de toda a população UMA ÚNICA VEZ na geração
        fits = [fitness(ind, init) for ind in pop]
        
        # Encontra o melhor da geração atual
        idx = min(range(len(fits)), key=fits.__getitem__)
        if fits[idx] < best_fit:
            best_fit, best = fits[idx], pop[idx][:]
            
        # Se a distância de Manhattan for 0, encontramos a solução!
        if best_fit == 0:
            return best, gen, best_fit

        # Elitismo: passa os melhores direto para a próxima geração
        ranked = sorted(zip(fits, pop), key=lambda x: x[0])
        new_pop = [ind[:] for _, ind in ranked[:elitism]]

        # 2. Nova Seleção por Torneio (Muito mais rápida!)
        while len(new_pop) < pop_size:
            # Sorteamos os índices da população atual
            idx_p1 = random.sample(range(pop_size), 5)
            idx_p2 = random.sample(range(pop_size), 5)
            
            # O vencedor do torneio é quem tiver o MENOR fitness (já calculado em 'fits')
            p1_idx = min(idx_p1, key=lambda i: fits[i])
            p2_idx = min(idx_p2, key=lambda i: fits[i])
            
            p1 = pop[p1_idx]
            p2 = pop[p2_idx]

            # --- Crossover dois pontos ---
            a, b = sorted(random.sample(range(1, seq_len), 2))
            c1 = p1[:a] + p2[a:b] + p1[b:]
            c2 = p2[:a] + p1[a:b] + p2[b:]

            # --- Mutação ---
            for c in (c1, c2):
                for i in range(len(c)):
                    if random.random() < pm:
                        c[i] = random.choice(MOVES)
                if len(new_pop) < pop_size:
                    new_pop.append(c)

        pop = new_pop#orna a nova população para a próxima geração

    return best, max_gen, best_fit