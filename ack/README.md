# Comunicação de Grupo Baseada em Ack

A comunicação entre o cliente e o receiver é feita com sockets.

Existem 3 serviços que são executados:

- **Servidor de Descobrimento**: Um servidor em Flask que registra os processos do Grupo que estão aptos a receberem comunicações do cliente e executarem os processamentos.
- **Receiver, ou Nó de Processamento**: Um processo que executa uma instância do processamento, fica aguardando uma requisição do cliente e responde com um ack depois do processamento. (Artificialmente foi colocada uma chance de 50% do processo falhar e não responder com o ack para simular casos de erro).
- **Cliente**: Uma instância que chama o servidor de descobrimento para obter informações sobre quais nós estão disponíveis para receber processamentos. Em seguida, envia uma mensagem para um dos nós e aguarda um timeout de 5 segundos para receber um ack. Caso não receba dentro desse tempo, tenta novamente infinitamente até receber um ack.

Tanto o cliente quanto o receiver podem ter cópias infinitas.

Para executar o programa siga os passos abaixo:

## Servidor de Descobrimento

Antes de tudo, suba o servidor, pois ele é essencial para a aplicação (caso você esqueça e suba outra coisa antes, já fiz uma lógica para que os outros componentes aguardem esse servidor subir antes de fazer qualquer coisa).

`docker-compose -f docker-compose.discovery.yml up -d`

## Receivers

Suba uma quantidade N de receivers com o seguinte comando:

`docker-compose -f docker-compose.receiver.yml up --scale receiver=<QTD>`

Cada um vai se conectar com o servidor de descobrimento e ganhar um ID.

## Cliente

Você também pode criar vários clientes, mas para fins de teste nesta disciplina e na apresentação do trabalho, não faz muito sentido subir vários. Portanto, vamos subir apenas um cliente, mas você pode usar o mesmo parâmetro de scale do receiver.

`docker-compose -f docker-compose.client.yml up -d --scale client=<QTD>`

`docker ps` -> isso vai listar todos os containers que você tem

Escolha qual cliente você quer entrar no terminal, pegue o ID e execute o comando:

`docker exec -it <ID> "/bin/bash"`

Já dentro do bash do cliente, inicie o programa com:

`python client.py`

Ele vai listar os processos ativos e perguntar para quem você quer mandar uma mensagem. Escreva o ID correspondente da lista e pressione Enter.

## Descrição do Funcionamento da Aplicação

### Fase de Registro

Durante esta fase, os nós de processamento registram-se no Servidor de Descobrimento. O cliente então usa essas informações para determinar quais nós estão disponíveis para processar mensagens.

![Fase de Registro](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_registro.png)

### Fase de Descobrimento

Nesta fase, o cliente faz uma requisição POST ao Servidor de Descobrimento para obter uma lista de receivers disponíveis. O servidor responde com um JSON contendo a lista. O cliente então pergunta aos receivers quem está disponível para processar a mensagem.

![Fase de Descobrimento](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_descobrimento.png)

### Fase de Mensagem (Sucesso)

Quando o cliente finalmente recebe o ACK, a mensagem foi processada com sucesso pelo nó.

![Fase de Mensagem (Sucesso)](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_mensagem_sucesso.png)

### Fase de Mensagem (Erro 1)

O cliente envia uma mensagem a um nó de processamento e espera um ACK. Se o nó falhar (não responde), o cliente não recebe o ACK.

![Fase de Mensagem (Erro 1)](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_mensagem_erro_1.png)

### Fase de Mensagem (Erro 2)

O cliente, ao não receber o ACK, tenta novamente enviar a mensagem.

![Fase de Mensagem (Erro 2)](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_mensagem_erro_2.png)

### Fase de Mensagem (Erro 3)

O cliente continua tentando até receber um ACK. A ilustração mostra o cliente finalmente recebendo o ACK após várias tentativas.

![Fase de Mensagem (Erro 3)](https://raw.githubusercontent.com/TarefasUFSC/Sistemas_Distribuidos-Trab_Pratico/main/docs/ack-fase_de_mensagem_erro_3.png)

Essas fases demonstram como a aplicação lida com a descoberta de nós disponíveis, envio de mensagens, tratamento de erros e registro de nós.
