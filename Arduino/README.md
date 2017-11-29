# Arduino

Este são os cordigos utilizados no carro para arduino. Ele é dividido em 3 partes, que são: "Autonomous_Car_Final"; "Functions"; "MPU6050_Setup_Loop".

## Codigos

### Autonomous_Car_Final

Esta aba é a principal parte do codigo, onde o "void setup" e o "void loop" estão. Os "include" e os "defines" são de maioria para o MPU6050 consiga rodar, com exeção do ultimo (softwareSeria.h) na qual colocamos apenas para monitoramento de variaveis atravez do terminal. Dividimos as variaveis em 2 para uma fazer ajustes mais faceis, as primeiras são variaveis do MPU6050 e as demais são para o controlador PID, todas comentadas.
No "void setup" começamos a comunicação serial e então chamamos um função "MPU6050_setup()" na qual fica na terceira aba (MPU6050_Setup_Loop) e será explicada lá. Apos isso definimos alguns pinos para o controle das rodas até chegamos no comando "while" que roda uma função "MPU6050_loop()" na qual é preciso rodar por alguns segundos afim de estabilizar os sensores antes do carro começar a andar.
O "void loop" é somente o controlador PID com a função de loop do MPU.

### Functions

Nesta aba é para tabelas e funções do MPU e de controle PID na qual são explicadas melhor nas suas respectivas pastas.

### MPU6050_Setup_Loop

Aqui são colocadas o setup e o loop necessario para que o MPU6050 rode corretamente. No setup é feita uma comunicação basica para iniciar o sensor. No loop é somente necessario o saber se a comunicação pode ser feita (fifoReady) e assim executar as funcções nela.
