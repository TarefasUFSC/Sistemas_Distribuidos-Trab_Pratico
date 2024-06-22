# Comunicação de Grupo Baseada em Ack
A comunicação entre o cliente e o receiver é feita com sockets

Existem 3 serviços que são executados:
- Servidor de Descobrimento: Um servidor em Flask que registra os processos do Grupo que estão aptos a receberem comunicações do cliente e executarem os processamentos
- Receiver, ou Nó de processamento: É um processo que executa uma instancia do processamento e fica aguardando uma requisição do cliente e responde com um ack depois do processamento. (Artificialmente foi colocado uma chance de 50% do processo crashar e simplesmente não responder o ack só para podermos ver o caso de erro)
- Cliente: Uma instancia que chama o servidor de descobrimento para pegar as informações de quais nós estão disponiveius para receberem processamentos e então envia uma mensagem para um dos nós e aguarda um Timout de 5s para receber um ack. Caso n receba nesse meio tempo ele tenta de novo infinitamente até receber um ack dentro do tempo

Tanto o cliente quanto o receiver podem ter infinitas copias. 

Para executar o programa siga os passos abaixo:

## Servidor de descobrimento