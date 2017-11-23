# AutonomousSystems
## Introdução
O projeto tem como objetivo fazer um carro autônomo, capaz de andar e fazer curvas em uma pista sem que saia dela. Ele o carro é equipado com uma câmera, um microcontrolador e um sistema capaz de processar imagens e uma inteligência artificial como, no nosso caso, um computador. Quando o carro começar a andar, a câmera deverá capturar imagens da pista e manda-las para o sistema de processamento de imagens e da IA, onde no sistema ele irá, pela imagem, procurar o centro da pista e mandar um valor de acordo para o microcontrolador, que neste fará o controle de rodas e outros sensores (através de um controlador PID) para se manter no centro.

## Sistemas de Malha Fechadas

O principal conceito por traz do controlador PID é de ler um sensor, calcular a resposta de saída (esse cálculo é feito através do proporcional, integral e derivativo separados para depois somar-se, na qual os 3 componentes compõem o controlador PID), e então esse cálculo é colocado no atuador.

Para entender melhor o funcionamento do PID em um sistema de malha fechada (ou seja, que possui uma retroalimentação na saída) é necessário explicar brevemente como funciona um o sistema. Em um sistema de controle típico, a variável do processo é o parâmetro do sistema que precisa ser controlado como temperatura ou pressão, por exemplo. Um sensor é usado para medir a variável de processo e fornecer feedback (ou retroalimentação) para o sistema de controle. O set point é o valor desejado ou comando para a variável de processo, tais como 100ºC, no caso de um sistema de controle de temperatura. A qualquer momento, a diferença entre a variável de processo e o set point é usada pelo algoritmo do sistema de controle (controlador), para determinar a saída desejada do atuador, que por sua vez, irá acionar o sistema. Por exemplo, se a variável de processo “temperatura” medida é de 100 º C e o setpoint da temperatura desejada é de 120 º C, então a saída do atuador especificada pelo algoritmo de controle pode ser a unidade de um aquecedor. Controlar um atuador para ligar um aquecedor faz com que o sistema fique mais quente, e resulta em um aumento na variável de processo “temperatura”. Isto é chamado de um sistema de controle em malha fechada, porque o processo de leitura dos sensores para fornecer uma retroalimentação constante e o cálculo para definir a saída desejada do atuador se repete continuamente, como ilustrado a seguir.

## Controlador PID

No nosso caso, a câmera e o algoritmo de detecção de faixa fará o papel de setpoint. *Resumo do lane detection*

Após pegar o setpoint é necessário calcular o erro, para isso é utilizado o MPU6050, *Resumo MPU*.

Após o cálculo do erro, feita simplesmente subtraindo o ângulo do setpoint definido pelo algoritmo de detecção de faixa pelo o ângulo medida pelo sensor MPU, é necessário tratar este valor para que vire um comando para as rodas. Para isso é feito o controlador PID. Este controlador na verdade é um somatorio de 3 controladores que funcionam de maneira independentes, que são chamados de proporcional (o P do PID), integrativo (o I) e o derivativo (o D) e cada um tem sua função no controlador. *Falar o que é o controlador Proporcional*. *Falar o controlador Integrativo*. *Falar do controlador Derivativo*.
