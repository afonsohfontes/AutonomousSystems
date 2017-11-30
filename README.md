# AutonomousSystems

Este texto foi elaborado por: [Ramon Bernardes](https://github.com/RamonRBF)

## Introdução
O projeto tem como objetivo fazer um carro autônomo, capaz de andar e fazer curvas em uma pista sem que saia dela. Ele o carro é equipado com uma câmera, um microcontrolador e um sistema capaz de processar imagens e uma inteligência artificial como, no nosso caso, um computador. Quando o carro começar a andar, a câmera deverá capturar imagens da pista e manda-las para o sistema de processamento de imagens e da IA, onde no sistema ele irá, pela imagem, procurar o centro da pista e mandar um valor de acordo para o microcontrolador, que neste fará o controle de rodas e outros sensores (através de um controlador PID) para se manter no centro.

## Sistemas de Malha Fechadas

O principal conceito por traz do controlador PID é de ler um sensor, calcular a resposta de saída (esse cálculo é feito através do proporcional, integral e derivativo separados para depois somar-se, na qual os 3 componentes compõem o controlador PID), e então esse cálculo é colocado no atuador.

Para entender melhor o funcionamento do PID em um sistema de malha fechada (ou seja, que possui uma retroalimentação na saída) é necessário explicar brevemente como funciona um o sistema. Em um sistema de controle típico, a variável do processo é o parâmetro do sistema que precisa ser controlado como temperatura ou pressão, por exemplo. Um sensor é usado para medir a variável de processo e fornecer feedback (ou retroalimentação) para o sistema de controle. O set point é o valor desejado ou comando para a variável de processo, tais como 100ºC, no caso de um sistema de controle de temperatura. A qualquer momento, a diferença entre a variável de processo e o set point é usada pelo algoritmo do sistema de controle (controlador), para determinar a saída desejada do atuador, que por sua vez, irá acionar o sistema. Por exemplo, se a variável de processo “temperatura” medida é de 100 º C e o setpoint da temperatura desejada é de 120 º C, então a saída do atuador especificada pelo algoritmo de controle pode ser a unidade de um aquecedor. Controlar um atuador para ligar um aquecedor faz com que o sistema fique mais quente, e resulta em um aumento na variável de processo “temperatura”. Isto é chamado de um sistema de controle em malha fechada, porque o processo de leitura dos sensores para fornecer uma retroalimentação constante e o cálculo para definir a saída desejada do atuador se repete continuamente, como ilustrado a seguir.

## Controlador PID

No nosso caso, a câmera e o algoritmo de detecção de faixa fará o papel de setpoint. *Resumo do lane detection*

Após pegar o setpoint é necessário calcular o erro, para isso é necessário o MPU6050. "O módulo MPU6050 nada mais é do que um acelerômetro, giroscópio e sensor de temperatura embutidos em uma placa eletrônica e processados através de um CI, que facilita o processamento de dados e a comunicação desses à CPU através da rede I2C", ou seja, ele nos fornecerá o angulo na qual o carro está em relação a que ele foi configurado (ao iniciar ele define o angulo em que está iqual a zero). O Código do arduino é explicado mais à frente.
	
Após o cálculo do erro, feita simplesmente subtraindo o ângulo do setpoint definido pelo algoritmo de detecção de faixa pelo o ângulo medida pelo sensor MPU, é necessário tratar este valor para que vire um comando para as rodas. Para isso é feito o controlador PID. Este controlador na verdade é um somatório de 3 controladores que funcionam de maneira independentes, que são chamados de proporcional (o P do PID), integrativo (o I) e o derivativo (o D) e cada um tem sua função no controlador. 
No nosso projeto o PID foi ajusto com o método de "guess and check", ou seja, foi estimado um número para as constantes(Kp, Ki e Kd) de cada componente do controlador e então testamos esses valores e ajustamos à medida que achávamos que o controle oscilava muito ou demorava demais para a estabilizar.

O controlador proporcional é o mais básico dos 3, a ideia por traz dele é fazer com que a resposta seja proporcional ao erro em relação ao setpoint, ou seja, quanto maior o erro, maior será a resposta e vice-versa. O seu cálculo faz com que ele pegue o erro e o multiplique por uma constante "Kp", sendo assim, caso o KP seja iqual a 5 e o erro seja 10 a resposta que chegará no sistema é 50. O ideal é que, quando se está começando o ajuste, comece apenas com o controlador proporcional até que esteja regulado tendo em mente também que neste controlador o erro estacionário não chega a ser zerado, deve-se apenas observar se o tempo de resposta está adequado.

A componente integral soma o termo de erro ao longo do tempo. O resultado é que mesmo um pequeno erro fará com que a componente integral aumente lentamente. A resposta integral irá aumentando ao longo do tempo a menos que o erro seja zero, portanto, o efeito é o de conduzir o erro de estado estacionário para zero. Após o ajuste do proporcional, acrescenta-se o integral (fazendo assim um controlador PI) e comece novamente o ajuste, podendo mudar o valor de Kp.

A componente derivada faz com que a saída diminua se a variável de processo está aumentando rapidamente. A derivada de resposta é proporcional à taxa de variação da variável de processo. Aumentar o parâmetro do tempo derivativo (dt) fará com que o sistema de controle reaja mais fortemente às mudanças no parâmetro de erro aumentando a velocidade da resposta global de controle do sistema. Agora com o controlador completo (Proporcional, integrativo e derivativo) ajuste novamente os valores das constantes até que a resposta da mudança de setpoint ou de distúrbios esteja rápida e sem erros no final.

No nosso carro, utilizamos o primeiramente o controlador P, definimos o setpoint iqual a zero (ângulo zero em relação a frente do carro, ou seja, o carro deve andar em linha reta) e no meio do percurso batíamos levemente nas rodas traseiras para que ele perdesse a direção o observávamos se ele respondia bem ao distúrbio, caso não, ajustávamos para mais ou para menos a constante Kp. Seguimos assim para o controlador PI e aplicávamos o mesmo teste até que Kp e Ki estejam regulados da mesma maneira e da mesma maneira colocamos o componente derivativo (PID). Após os três estarem regulados, colocamos um dispositivo bluetooth para mudar o valor do setpoint e verificar se o mesmo conseguia fazer ter a mesma resposta.

## Carro Autônomo

Antes de falar do código do carro é preciso falar dos componentes na qual utilizamos, que foram: 1 arduino, 1 modulo bluetooth HC-06, 1 MPU6050, 1 driver de ponte H L298N, 1 chassi de carro para arduino, 2 rodas com controladores servomotos e 1 roda de apoio.
	
Agora explicando o código do arduino. A lógica do programa começa no "void Setup", na qual ele define alguns pinos como "output" a fim de transformá-los em pinos de controle na qual serão utilizados na ponte H e assim controlar as rodas. Após isso é implementado uma lógica de "while" na qual inicializa o senso MPU, afim de estabiliza-lo. 
	
Código do Arduino:

```
void setup(){
  
Serial.begin(9600);
//serial1.setTimeout(10); //When using serial.parseFloat, the default value of this function is 1000ms, wich makes the arduino takes too long to read the data from the bluetooth.
	  serial1.begin(9600);
	  MPU6050_setup();
	  pinOutMode(ENA);
	  pinOutMode(ENB);
	  pinOutMode(IN1);
	  pinOutMode(IN2);
	  pinOutMode(IN3);
	  pinOutMode(IN4);
	  pinOutMode(EN_BT);
	  digitalWrite(EN_BT, HIGH);
	  while(first <= 400){ // If the car has a display screen, it is possible insert a bar from 0 to 100% showing the car initialization using this value
	    MPU6050_loop();
	  }
	  Serial.println("Valendo");
	} // End of the setup
```
	
Após as configurações iniciais, começa o loop no qual o carro ficará até ser desligado. No "void loop" começa com o controle PID, na qual primeiramente ele precisa pegar o tempo na qual já foi decorrido e atualizar, isso é preciso para o cálculo do componente derivativo do controlador.
	
```
	void loop(){
	  last_time = actual_time;
	  actual_time = millis();
	
```
	
Seguindo assim para uma requisição do ângulo do carro feita pela linha `MPU6050_loop();` na qual fica na aba de "MPU6050_Setup_Loop". Com o valor do ângulo do carro é preciso pegar o setpoint estabelecido pelo algoritmo de detecção de lane através de uma comunicação serial do bluetooth. Caso não, o setpoint continua o que foi estabelecido (lembrando que o setpoint é inicializado com zero, caso não tenha ocorrido nenhuma leitura nova de valor).
	
```
	  if (serial1.available()) { //Check the serial communication working
	    //sp = serial1.parseFloat();
	    sp = ((float) serial1.read()) - 100;
	    Serial.print("Setpoint: "); Serial.println(sp);
	    ok_coord = true;
	    }
```
	
Com estes valores já é possível calcular o erro, na qual será utilizado no controlador. Caso o erro seja zero e houve alguma mudança de setpoint anteriormente, é preciso zerar e reconfigurar o MPU6050 para que esse novo setpoint seja a nova frente do carro, na qual as duas variáveis booleanas (reset_coord e ok_coord) fazem esse controle.
	
```
	  last_ang = actual_ang;
	  actual_ang = deg[0];
	  error = sp - actual_ang;  
	  if(error == 0 && ok_coord){
	    sp = 0;
	    reset_coord = true;
	    ok_coord = false;
	    }
```
	
Com o erro já é possível para o controlador calcular sua resposta PID e aplica-lo no sistema, na qual é exatamente isso que as próximas duas linhas fazem. A linha  `wheel_controller();` chama uma função que fica na aba "Function", lá ele faz todo o cálculo do controlador. Assim que a função é chamada ela calcula os valores individuais de P, de I e de D e logo após são somados. Importante dizer também que, pelo componente integrador ser um somatório é preciso definir um limite na qual ele não cresça para uma escala muito grande, na qual no nosso caso foi determinado como 50, para positivo e para negativo.
	
```
	void wheel_controller(){
	  dt = actual_time - last_time;
	  p = kp * error;
	  i += ki * error * dt;
	  if(i > 50 || i < -50)
	    if (i > 50) i =  50;
	    if (i < -50) i = -50;
	  d = (kd * (actual_ang - last_ang)) / dt;
	  pid = p + i + d;
```
	
Com o PID completo basta aplica-lo as variáveis que fazem o controle do carro, que são X e Y. Ambas devem ter um valor de uma constante para caso o PID seja 0 o carro continuar há andar, neste caso, para frente. Estas duas variáveis vão as que serão aplicadas nas rodas (uma em cada roda) fazendo assim o controle de velocidade das rodas por PWM (pulse-width-mudulation), e como ele só aceita valores de 0 a 255 deve-se ter certeza que essas variáveis não passem disso. OBS: No caso do nosso X foi preciso dá uma pequena compensada de +45 devido a uma das rodas andar mais devagar.
	
```
	  x = (cons + 45) + pid;
	  y = cons - pid;
	  
	  if(x < 0 || y < 0){
	    if(x < 0) x = 0;
	    if(y < 0) y = 0;}
	    
	  if (x > 255 || y > 255){
	    if(x > 255) x = 255 ;
	    if(y > 255) y = 255;}
	}
```
	
E por último é aplicado os valores calculados de X em uma das rodas e o de Y em outra pela função `mov_front`.
	
```
	void mov_front(int a, int b){
	  digitalWrite(IN1, HIGH);
	  digitalWrite(IN2, LOW);
	  digitalWrite(IN3, HIGH);
	  digitalWrite(IN4, LOW);
	  analogWrite(ENA, a);
	  analogWrite(ENB, b);
	}
```
	
E assim terminando o loop de controle. As demais linhas são feitas para ver os valores de algumas variáveis quando ainda está configurando via terminal do IDE do Arduino. Pelo o mesmo usar as portas 0 e 1 para estabelecer a comunicação da USB foi preciso criar um software serial para que pudéssemos ler o valor do bluetooth e monitorarmos as variáveis.
	
```
	  //Serial.print("Angle: "); Serial.println(deg[0]);
	  //Serial.print("Setpoint: "); Serial.println(sp);
	  /*Serial.print("Error: "); Serial.println(error);
	  Serial.print("PID: "); Serial.println(pid);*/
	  //Serial.print(x); Serial.print(" :X e Y: "); Serial.println(y); //Serial.println(y);
	  //Serial.print("Angle: "); Serial.print(deg[0]);  Serial.print("  Setpoint: "); Serial.print(sp);  Serial.print("  Error: "); Serial.print(error);  Serial.print("  PID: "); Serial.print(pid);   Serial.print("  X:  "); Serial.print(x); Serial.print("  Y: "); Serial.println(y); //Serial.println(y);
	
	}//End of the loop
```
