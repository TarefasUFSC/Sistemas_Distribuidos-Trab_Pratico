# Comunicação de Grupo Baseada em Ack

A comunicação entre o cliente e o receiver é feita com sockets

Existem 3 serviços que são executados:

- Servidor de Descobrimento: Um servidor em Flask que registra os processos do Grupo que estão aptos a receberem comunicações do cliente e executarem os processamentos
- Receiver, ou Nó de processamento: É um processo que executa uma instancia do processamento e fica aguardando uma requisição do cliente e responde com um ack depois do processamento. (Artificialmente foi colocado uma chance de 50% do processo crashar e simplesmente não responder o ack só para podermos ver o caso de erro)
- Cliente: Uma instancia que chama o servidor de descobrimento para pegar as informações de quais nós estão disponiveius para receberem processamentos e então envia uma mensagem para um dos nós e aguarda um Timout de 5s para receber um ack. Caso n receba nesse meio tempo ele tenta de novo infinitamente até receber um ack dentro do tempo

Tanto o cliente quanto o receiver podem ter infinitas copias.

Para executar o programa siga os passos abaixo:

## Servidor de descobrimento

Antes de tudo suba o servidor, pois ele é essencial para aplicação (caso vc esqueça e suba outra coisa antes eu ja fiz um logica para fixcarem aguardando esse cara subir antes de fazer qualquer coisa)

`docker-compose -f docker-compose.discovery.yml up -d`

## Receivers

Suba uma quantidade N de receivers com o seguinte comando:
`docker-compose -f docker-compose.receiver.yml up --scale receiver=<QTD>`

Cada um vai se conectar com o servidor de descobrimento e ganhar um id

## Cliente

Voce tb pode criar varios clientes, mas para questão de teste nesta disciplina e na apresentação do trabalho isso não faz muitro sentido entção eu vou subir só um, mas vc pode faze usando o mesmo parametro de scale do receiver

- `docker-compose -f docker-compose.client.yml up -d --scale client=<QTD>`
- `docker ps` -> isso vai listar todos os containers que vc tem
- escolhe qual cliente vc quer entrar no terminal e pega o id e joga nesse comando: `docker exec -it <ID>> "/bin/bash"`
- Já dentro do bash do cliente inicie o programa com `python client.py`
- ele vai listar os processos ativos e vai perguntar pra quem vc quer mandar uma msg. escreva o id correspondente da lista e de enter
