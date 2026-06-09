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
São meta-heurísticas de busca inspiradas na Teoria da Evolução Natural de Charles Darwin. Eles simulam uma população de soluções que competem entre si, onde os indivíduos mais aptos sobrevivem e transmitem suas características para as próximas gerações. No contexto do 8-puzzle, os componentes foram modelados da seguinte forma:

- **Cromossomo (representação do Indivíduo)** Cada cromossomo (ou indivíduo) representa uma proposta de solução para o problema. Ele é modelado como uma lista de tamanho fixo (_N=120 genes_), onde cada gene corresponde a um movimento elementar do espaço vazio no tabuleiro:
  - ' U ' (_UP-Cima_)
  - ' D ' (_Down-Baixo_)
  - ' L ' (_Left-Esquerda_)
  - ' R ' (_Right-Direita_)

  Como a população inicial é gerada de forma totalmente aleatória, muitos movimentos colidirão com as bordas do tabuleiro. A física do jogo apenas ignora os movimentos inválidos, permitindo que o indivíduo continue executando.

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

## 4. Testes e Análise de Resultados

Para avaliar a eficácia do Algoritmo Genético desenvolvido, o sistema foi testado utilizando a interface gráfica com os 4 cenários pré-definidos (_Presets_). Os dados obtidos no painel de estatísticas foram consolidados na tabela abaixo:

| Cenário de Teste  | Dist. Manhattan Inicial | Solúvel? | Status Final             | Gerações de Parada | Tamanho da Solução (Movimentos) | Tempo de Execução |
| :---------------- | :---------------------: | :------: | :----------------------- | :----------------: | :-----------------------------: | :---------------: |
| **Fácil**         |            1            |   Sim    | Solução encontrada!      |        500         |                3                |       8.92s       |
| **Médio**         |            2            |   Sim    | Solução encontrada!      |        800         |               52                |      33.52s       |
| **Médio-Difícil** |            9            |   Não    | Parcial! limite atingido |        2000        |               117               |      277.9s       |
| **Difícil**       |           10            |   Sim    | Solução encontrada!      |        3000        |               82                |      581.35s      |

### Análise dos Resultados do primeiro teste

- **Cenário Fácil:** O algoritmo demonstra uma eficiência espetacular, encontrando a solução em menos de 9 segundos. Como o tabuleiro inicial estava a pouquíssimos movimentos do objetivo (Distância de Manhattan = 1), a própria população inicial aleatória gerou indivíduos capazes de resolver o problema quase de imediato. O algoritmo convergiu rapidamente na geração 500 porque o espaço de busca era extremamente pequeno, gerando uma solução limpa de apenas 3 movimentos.
- **Cenário Médio:** Este caso é o melhor exemplo do "equilíbrio" do Algoritmo Genético. O tabuleiro estava moderadamente embaralhado (Distância de Manhattan = 2). O algoritmo precisou de 800 gerações e cerca de 33 segundos para evoluir a solução. Repare que a solução final teve 52 movimentos: isso reflete a característica estocástica do AG, que foca em encontrar _uma_ solução válida que zere a distância de Manhattan, mesmo que o caminho encontrado não seja o mais curto possível (diferente de uma busca clássica como o A\*, que prioriza o caminho mínimo).
- **Cenários Fácil e Médio:** No cenário Médio-Difícil, a função de validação matemática identificou que o tabuleiro inicial era Insolúvel, Como esperado teoricamente, o Algoritmo Genético esgotou o limite máximo de 2000 gerações sem conseguir zerar a Distância de Manhattan, comprovando a eficácia do nosso módulo de checagem de inversões em prever estados impossíveis de resolver.
- **Cenário Difícil:** No cenário Difícil, o algoritmo genético obteve sucesso absoluto, encontrando a solução na geração 3000. O tempo de execução elevado (581.35s) deve-se ao custo computacional de avaliar uma população maior (400 indivíduos) ao longo de sequências longas (150 genes). Este caso valida o comportamento estocástico do AG: mesmo diante da degradação de sequências provocada pelo crossover em caminhos complexos, a manutenção de uma alta variabilidade genética (mutação) e o elitismo permitiram alcançar o objetivo no limite do esforço programado.

## 4.1 Testes e Analise de resultados 2

No **Primeiro teste** notou-se alguns pontos em que poderiamos melhorar a eficiência do algoritmo e obter melhores resultadados.

As principais mudanças ocorreram nos testes: médio-dificil e dificil.

**Primeira Mudança**: Na tabela 1, o cenario médio-dificil é marcado como insolúvel, ou seja não existe solução (Distância de Manhattan = 0). Mesmo assim, o algoritmo calcula 2000 gerações, o que nos leva a um despedicio de processamento, pois o objetivo é impossivel.
O problema foi resolvido com uma "Trava de Segurança", que verifica se existe solução antes de iniciar o algoritmo genetico, e é encerrado imediatamente pelo _Return_ retornando valores que indicam que nenhuma solução foi encontrada, nenhuma geração foi executada e que o custo é infinito.
Abaixo o trecho do código onde a adaptaçao ocorreu:

```python
if not solvable(init):
    print("Tabuleiro INSOLÚVEL!")
    return None, 0, float('inf')
```

**Segunda Mudança:Otimização de Performance** A segunda mudança se deu, por nos atentarmos ao fato de que a função _Fitness_, calculava o mesmo elemento centenas de vezes, com isso resolvemos que calcular a função 1(uma) única vez no início de cada geração e salvarmos esses valores na lista **_fits_** , espera-se que essa mudança diminua drasticamente o tempo de execução, especialmente nos cenários Difíceis (que demoravam 581 segundos).
A mudança ocorre logo na primeira parte do laço:

```python
for gen in range(max_gen):
   fits = [fitness(ind, init) for ind in pop]
```

Os dados obtidos no painel de estatísticas do segundo teste foram consolidados na tabela abaixo:

Para avaliar a eficácia e a evolução do Algoritmo Genético desenvolvido, submetemos o sistema a uma bateria de testes utilizando a interface gráfica com os cenários pré-definidos (_Presets_).

## 4.2 Testes e Análise de Resultados (Otimizados)

Após a identificação de redundâncias críticas na seleção por torneio e da ausência de travas para matrizes impossíveis, o motor do Algoritmo Genético foi refatorado. Abaixo apresenta-se a tabela com os novos dados empíricos recolhidos na interface gráfica:

| Cenário de Teste  | Dist. Manhattan Inicial | Solúvel? | Status Final             | Gerações de Parada | Tamanho da Solução (Movimentos) | Tempo de Execução |
| :---------------- | :---------------------: | :------: | :----------------------- | :----------------: | :-----------------------------: | :---------------: |
| **Fácil**         |            1            |   Sim    | Solução encontrada!      |        500         |               13                |       2.02s       |
| **Médio**         |            2            |   Sim    | Solução encontrada!      |        800         |               58                |       6.98s       |
| **Médio-Difícil** |            9            |   Não    | Parcial! limite atingido |         0          |                0                |        0s         |
| **Difícil**       |           10            |   Sim    | Solução encontrada!      |        3000        |               144               |      112.81s      |

### 4.3 Análise Comparativa do Impacto das Otimizações

A reestruturação do código trouxe melhorias nos indicadores de eficiência do sistema:

1. **Ganho de Velocidade por Vetorização de Fitness:** Ao calcular o _fitness_ da população uma única vez por geração (armazenando-o na memória para consulta rápida no torneio), eliminou-se o gargalo de recalcular caminhos repetidamente. Isso resultou numa **redução média de ~78% no tempo de execução** nos cenários solúveis (_Fácil_, _Médio_ e _Difícil_). O caso mais complexo (_Difícil_) passou de **9.6 minutos** para uma execução de apenas **1.8 minutos**.
2. **Eliminação do Desperdício Computacional:** No cenário _Médio-Difícil_, o algoritmo original executava loops redundantes por 277.9 segundos. A inclusão da validação de inversões matemática eliminou este procedimento, encerrando a execução em **0 segundos** ao detectar que o puzzle pertencia à metade insolúvel.

## 6. Conclusão

Com esse projeto, conseguimos entender na prática como um Algoritmo Genético funciona para resolver o jogo do 8-puzzle, e chegamos a algumas conclusões importantes:

- **A matemática ajuda o algoritmo:** Não adianta só soltar o algoritmo genético para procurar a solução se o tabuleiro for impossível de resolver. Metade dos tabuleiros desse jogo não têm solução. Colocar a função `solvable()` logo no começo foi essencial para o sistema não ficar rodando para sempre em um problema sem saída.
- **Código mal otimizado trava tudo:** A função de calcular a nota (_fitness_) é a parte mais pesada do sistema, porque ela mexe nas peças e calcula as distâncias. Fazer o código calcular isso uma vez só e guardar o valor na memória foi o que salvou o desempenho do projeto. Se não fizesse isso, o programa continuaria lento demais para usar na interface.
- **A Distância de Manhattan funciona bem:** Usar a distância de Manhattan (contar quantas casas faltam para cada peça chegar no lugar certo) junto com a penalidade para movimentos inválidos se mostrou uma ótima escolha. Ela guiou a população de um jeito que, mesmo no caso Difícil, o algoritmo conseguiu achar o caminho certo.

No geral, o projeto funcionou muito bem. O algoritmo saiu de uma versão travada e pesada para uma versão rápida, inteligente e que não quebra se o usuário colocar um tabuleiro impossível.
