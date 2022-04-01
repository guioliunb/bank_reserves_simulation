# Modelo de Reservas Bancárias 

## Resumo

Um modelo altamente abstrato e simplificado de uma economia, com apenas um tipo de agente e um único banco representando todos os bancos de uma economia. As pessoas (representadas por círculos) se movem aleatoriamente dentro da grade. Se duas ou mais pessoas estiverem no mesmo local da grade, há 50% de chance de que elas negociem entre si. 

-Um saldo comercial positivo será depositado no banco como poupança. Se a negociação resultar em saldo negativo, o agente tentará sacar de suas economias para cobrir o saldo. 
Se não tiver poupança suficiente para cobrir o saldo negativo, fará um empréstimo junto ao banco para cobrir a diferença.


Hipóteses:
- Os valores de monetários agora possuem 4 chances de negociação entre os agentes. Com os valores atualizados para: $10, $20, $50, $10.
- Cada empréstimo feito pelo Agente terá parte do valor descontado por imposto requerido pelo Governo da simulação.
- Cada pagamento recebido terá parte do valor descontado por imposto requerido pelo Governo da simulação.
- O governo atua como um 3º agente no modelo. Assim sua contribuição será ponderada como hipóteses podendo ser positiva(auxílio de crédito) e/ou negativa(impostos).


Explicação 1: Dessa forma, com a maior diferenciação dos valores de negociação, em hipótese, juntamente com o fluxo de saída de imposto ocasionará maior desigualdade entre os agentes.

- Essa taxa de imposto considera valores individuais para cada agente entre o intervalo de 1% a 25%.

Explicação 2: O banco é obrigado a manter uma certa porcentagem dos depósitos como reservas. 

- Essa reserva entretanto pode ser reduzida até 1% com as hipóteses citadas promoverá maior transferência dos valores entre os agentes, contudo concentrando em maior quantidade de ricos/pobres e diminuição dos valores médios.

- O pensamento contrário também é válido. Assim a reserva do banco ajuda os agentes na manutenção dos seus valores, assim ajudando numa tendência média.

Explicação 3 (Colaboração do governo): No sentido contrário da arrecadação de impostos temos uma ação de manutenção financeira do sistema pelo governo.

- Quando o percentual de agentes na classificação pobre alcançar o valor definido de 20% então o governo auxiliará nos depósitos bancários em taxas de 15% até que a população de agentes se distribua melhor entre as outras duas classes (exceção da classe pobre).

- Assim, o governo atua como um 3º elemento com fator negativo: imposto e fator positivo: auxílio de crédito.

OBS: O repositório ainda possui 2 arquivos de modelo, pois uma melhora na ação de crédito do banco é funcional mas estava incompatível com os tipos de dados recebidos no batch_run (provavelmente por ser float).

Step 2:

Será analisada as influências da  "taxation"-imposto (variável de controle), e a influência dos "saved_taxes"-rendimentos(variável independente) do banco no sistema pelo faturamento ou perda das reservas provenientes das taxas.

O Banco começa com uma quantidade de dinheiro razoável ($1000) comparado com a variação de pessoas de 50-150.

O número de passos foi reduzido para 100 ou 200 steps pea quantidade de variações necessarias nas variaveis de controle para atingir os resultados estatísticos relevantes. Embora, o melhor resultado seria com mais steps e as mesmas variações não foi possível pela extensão dos arquivos e a sobrecarga computacional. Nas próximas entregas os processamentos mais longos serão tentados novamente.

A hipótese causal: A influência do banco afeta diretamente a quantidade das classes extremas foi tratada em 3 situações:
-Governo neutro
-Governo promotor
-Governo destrutor 

A forma de devolução implementada foi o retorno do capital de taxas para o capital de empréstimo assim que as reservas bancárias atingem um nível crítico.

A parte de tarifação destina as tarifas acumuladas apenas para o capital de reserva, ou seja, não retornando como capital disponível imediatamente  

Outras variações nas variáveis de controle foram feitas, porém os resultados não foram considerados satisfatórios. O que melhor descreveu as mudanças dentro das tentativas foi:

        "init_people":  [50, 100,150],
        "rich_threshold" :  [100 ,200],
        "reserve_percent" :  [10, 20, 30],
        "taxation" : [10, 20, 30]
        
Os arquivos csv gerados forma dividos entre as 3 situaões de Governo e foram realizados testes de correlação 

Execução:
Se run.py for usado para executar o modelo, a porcentagem de depósitos que o banco deve reter é um parâmetro configurável pelo usuário. O valor que o banco pode emprestar a qualquer momento é uma função do valor dos depósitos, suas reservas e o valor total do empréstimo atual.

Ferramentas Mesa :
 - MultiGrid para criar espaço compartilhável para agentes
 - DataCollector para coletar dados em execuções de modelos individuais
 - UserSettableParameters para ajustar os parâmetros iniciais do modelo
 - ModularServer para visualização da interação do agente
 - Herança de objeto do agente
 - Usando BatchRunner para coletar dados em várias combinações de parâmetros do modelo

## Instalação

Para instalar as dependências use o pip e o requirements.txt neste diretório. por exemplo.

```
    $ pip install -r requirements.txt
```

## Execução interativa do modelo

Para executar o modelo interativamente, use `mesa runserver` neste diretório:

```
    $ mesa runserver
```

Abra o navegador no urk [http://127.0.0.1:8521/](http://127.0.0.1:8521/), sslecione os parâmetros do modelo, pressione Reset, depois Start.

## Execução em lote

Para executar o modelo como uma execução em lote para coletar dados em várias combinações de parâmetros do modelo, execute "batch_run.py" nesse diretório.

```
    $ python batch_run.py
```
Uma barra de progresso aparecerá.

Para atualizar os parâmetros para testar outras varreduras de parâmetros, edite a lista de parâmetros no dicionário denominado "br_params" no "batch_run.py".

## Arquivos

* ``bank_reserves/random_walker.py``: Isso define uma classe que herda da classe Mesa Agent. O objetivo principal é fornecer um método para que os agentes se movam aleatoriamente uma célula por vez. 
* ``bank_reserves/agents.py``: Define a classe Pessoa e Banco.
* ``bank_reserves/model.py``: Define o modelo do Banco e as funções DataCollector.
* ``bank_reserves/server.py``: Configura o servidor de visualização interativa.
* ``run.py``: Inicia um servidor de visualização de modelo.
* ``batch_run.py``: Basicamente o mesmo que model.py, mas inclui um Mesa BatchRunner. O resultado da execução em lote será um arquivo .csv com os dados de cada etapa de cada execução.

## Referência em inglês:

This model is a Mesa implementation of the Bank Reserves model from NetLogo:

Wilensky, U. (1998). NetLogo Bank Reserves model. http://ccl.northwestern.edu/netlogo/models/BankReserves. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

"# bank_reserves_simulation" 
