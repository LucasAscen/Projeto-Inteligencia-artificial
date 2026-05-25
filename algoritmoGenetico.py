import random

def inicializar_populaçao(tamanho_populacao, tamanho_individuo):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = [random.randint(0, 1) for _ in range(tamanho_individuo)]
        populacao.append(individuo)
    return populacao

def avaliar_fitness(individuo):
    return sum(individuo)#quanto mais 1s, melhor

def selecionar_pais(populacao):
    populacaoOrdenada = sorted(populacao, key=avaliar_fitness, reverse=True)
    return populacaoOrdenada[:2]#seleciona os 2 melhores