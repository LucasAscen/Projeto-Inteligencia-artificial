# Aplicação e Análise de Algoritmos Genéticos Computacionais no Jogo dos 8 Números (8-Puzzle).

## Integrantes

- **Jeane**
- **João**
- **Lucas**
- **Luiz**

## 1. Objetivo do Projeto

Descrição: Este trabalho apresenta o desenvolvimento e a análise de um sistema baseado em **Algoritmos Genéticos (AG)** para a resolução do tradicional quebra-cabeça
_8-puzzle_. Diante de um tabuleiro 3×3 em uma configuração inicial totalmente resolvivel,o sistema busca evoluir uma sequência de movimentos válidos que reorganize as peças numeradas de 1 a 8 até atingirem a configuração meta ordenada.

## 2. Conceitos-Chave e Componentes do AG

**O que sao Algoritmos geneticos?**
são meta-heurísticas de busca inspiradas na Teoria da Evolução Natural de Charles Darwin. Eles simulam uma população de soluções que competem entre si, onde os indivíduos mais aptos sobrevivem e transmitem suas características para as próximas gerações. No contexto do 8-puzzle, os componentes foram modelados da seguinte forma:

- **Cromossomo (representação do Indivíduo)** Cada cromossomo (ou indivíduo) representa uma proposta de solução para o problema. Ele é modelado como uma lista de tamanho fixo (_N=120 genes_), onde cada gene corresponde a um movimento elementar do espaço vazio no tabuleiro:
  - ' U ' (_UP-Cima_)
  - ' D ' (_Down-Baixo_)
  - ' L ' (_Left-Esquerda_)
  - ' R ' (_Right-Direita_)

  Como a população inicial é gerada de forma totalmente aleatória, muitos movimentos colidirão com as bordas do tabuleiro. A física do jogo (implementada em nosso módulo) apenas ignora os movimentos inválidos, permitindo que o indivíduo continue executando o restante de seu código genético

- **Função de Avaliação (Fitness)** A função de Fitness mede a qualidade (aptidão) de um indivíduo ao final da execução de sua sequência de movimentos. Para o 8-puzzle, adotamos uma abordagem de minimização, onde a nota ideal é 0 (zero). O cálculo baseia-se na Distância de Manhattan:
  $$\text{Fitness} = \sum |x_{\text{atual}} - x_{\text{alvo}}| + |y_{\text{atual}} - y_{\text{alvo}}|$$

  Para cada uma das 8 peças, calcula-se o número mínimo de passos verticais e horizontais necessários para sair de sua posição atual e chegar à sua posição correta no estado meta. O espaço vazio (zero) é ignorado nesse cálculo. Adicionalmente, aplica-se uma leve penalidade proporcional ao número de movimentos inválidos para guiar o algoritmo a preferir caminhos mais limpos.

## 2.1 Operadores Geneticos

Nesta sessão, iremos falar sobre os tipos de Seleção utilizada no desenvolvimento do projeto, bem como o crossOver e outros topicos importantes.

**A. Seleção (Torneio Estocástico)**

Para escolhermos quais indivíduos atuarão como pais na reprodução, aplicamos a seleção por **Torneio de tamanho 5**. O algoritmo escolhe 5 indivíduos aleatoriamente da população geral, compara suas notas de fitness e seleciona aquele com o menor valor (o mais apto). O processo é repetido para selecionar o segundo pai.

**B. Cruzamento (Crossover de Dois Pontos)**

O operador de cruzamento combina as características de dois pais para gerar dois novos filhos. Sorteiam-se dois pontos de corte ao longo dos 120 genes da sequência. O primeiro filho herda o início e o fim do primeiro pai, e o segmento do meio do segundo pai. O segundo filho recebe a combinação inversa. Isso permite que blocos de movimentos bem-sucedidos sejam transmitidos de forma íntegra.

**C. Mutação**

A mutação introduz variabilidade genética na população para evitar a convergência prematura (ficar preso em soluções locais ruins). Cada gene dos filhos gerados possui uma probabilidade fixa de 3% (pm=0.03) de sofrer mutação. Caso ocorra, o movimento original é substituído por uma nova direção sorteada ao acaso entre as quatro opções válidas.

**D. Elitismo**

Como garantia de convergência, os 10 melhores indivíduos de cada geração são copiados diretamente para a população da geração seguinte, sem sofrer modificações. Isso impede que o algoritmo perca a melhor rota encontrada até o momento devido ao acaso do cruzamento ou da mutação.

## 2.2 Criterio de Parada

O algoritmo interrompe seu ciclo evolutivo sob duas condições:

**1** - _Sucesso total_: Quando um indivíduo alcança uma Distância de Manhattan igual a zero, significando que o tabuleiro foi completamente ordenado.

**2** - _Limite de esforço_: Quando o contador atinge o limite máximo de 2000 gerações, interrompendo a busca e retornando a melhor aproximação encontrada.

## 3. Discussão: Vantagens e Limitações frente a Abordagens Clássicas

A aplicação do Algoritmo Genético ao 8-puzzle traz conclusões teóricas importantes que contrastam com algoritmos clássicos de busca em grafos, como a Busca em Largura (BFS) e o algoritmo A\*

- **A Limitação do Crossover no Puzzle**: O 8-puzzle é um problema altamente sensível à ordem e ao contexto dos estados. Quando realizamos o corte de crossover entre dois pais, a posição em que o espaço vazio (zero) termina na primeira metade do Pai 1 raramente coincide com a posição em que ele começaria no Pai 2. Isso faz com que a segunda metade dos movimentos herdada da pai2 seja aplicada em um cenário totalmente diferente, quebrando a lógica do caminho e transformando o que seriam movimentos bons em colisões ou direções caóticas.

- **Desempenho e Qualidade**: Enquanto o algoritmo clássico A\* utilizando a mesma heurística de Manhattan é ótimo e completo (sempre encontra a solução no menor número de passos possível e de forma extremamente rápida), o Algoritmo Genético depende fortemente de fatores estocásticos (sorte nos sorteios) e frequentemente falha em encontrar a solução perfeita para tabuleiros que exigem profundidades de busca muito grandes.

- **A Vantagem do AG**: A principal vantagem teórica do AG reside no consumo de memória constante. Algoritmos como o BFS sofrem com a explosão combinatória de estados, precisando armazenar milhões de nós visitados na memória do computador, o que pode travar o sistema. O AG trabalha sempre com um espaço de memória estrito e controlado, limitado apenas ao tamanho fixo da população (300 indivíduos).
