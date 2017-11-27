# SERIAL COMMUNICATION

# Instalação

A linha de comando: [ pip install pyserial ] deve funcionar para a maioria dos usuários.
```
$ pip install pyserial
```
No caso de que você queira instalar com o anaconda use a linha: [ conda install ~c conda-forge pyserial ]
```
$ conda install ~c conda-forge pyserial
```
# Comunicação com o Arduino

Agora para o recebimento dos dados por parte do arduino iremos fazer uma breve explicação do que as linhas fazem de forma geral.
```
#include <SoftwareSerial.h> //Linha que introduz a biblioteca SoftwareSerial.h no código;

SoftwareSerial serial1(10, 11); // Indica os pinos serial RX, TX;
```

A seguide no void setup iremos configurar o necessário para a leitura serial.
```
void setup(){
  
  Serial.begin(9600); //Bauldrate
  //serial1.setTimeout(10); //se for usado a função serial.parseFloat o valor a ser setado deve ser 1000ms, se não a leitura será muito lenta;
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
  while(first <= 400){ // Opcional, caso o carro possua uma tela, ela irá disponibilizar uma barra de loading para a inicialização da serial;
    MPU6050_loop();
  }
  Serial.println("Valendo");
} // Fim do Setup
```
Agora dentro do laço de repetição:

```
if (serial1.available()) { //Verifica se a comunicação está funcionando
    //sp = serial1.parseFloat();
    sp = ((float) serial1.read()) - 100;
    Serial.print("Setpoint: "); Serial.println(sp);
    ok_coord = true;
    }
```
