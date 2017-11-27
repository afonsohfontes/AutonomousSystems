*O que é o MPU6050?
O módulo MPU6050 nada mais é do que um acelerômetro, giroscópio e sensor de temperatura embutidos em uma placa eletrônica e processados através de um CI, que facilita o processamento de dados e a comunicação desses à CPU através da rede I2C.

*Como, de fato, ele funciona?
Segundo o datasheet (anexo) do mesmo, os ranges do equipamento são os seguintes:

GIROSCÓPIO
SETTING  | SCALE  | VALUE  | UNIT
-------- | ------ | ------ | -----
FS_SEL=0 | ±250	  | 131		 | LSB(º/s)
FS_SEL=1 | ±500 	| 65.5	 | LSB(º/s)
FS_SEL=2 | ±1000	| 32.8	 | LSB(º/s)
FS_SEL=3 | ±2000	| 16.4   | LSB(º/s)

->Se o valor de FS_SEL escolhido for 0, o valor máximo da velocidade angular que o sensor vai conseguir detectar é de +-250º/s, onde o valor bruto (raw value) que será enviado à CPU será de 131. Então, deve-se saber qual a velocidade angular máxima que se espera que o projeto alcance e determinar o range adequado.

ACELERÔMETRO
SETTING  | SCALE  | VALUE  | UNIT
-------- | ------ | ------ | -----
AFS_SEL=0|	 ±2	  | 16384	 | LSB(g)
AFS_SEL=1|	 ±4	  | 8192   | LSB(g)
AFS_SEL=2|	 ±8	  | 4096	 | LSB(g)
AFS_SEL=3|	 ±16	| 2048	 | LSB(g)

->Se o valor de AFS_SEL escolhido for 0, o valor máximo da aceleração que o sensor vai conseguir detectar é de +-2g (onde g é a aceleração gravitacional de aproximadamente 9,8 m/s²), onde o valor bruto (raw value) que será enviado à CPU será de 16384. Então, deve-se saber qual a aceleração máxima que se espera que o projeto alcance e determinar o range adequado.

TEMPERATURA
     RANGE | VALUE | UNIT
     ----- | ----- | ----	
-40 to +85 | 340   | °C

Segundo o mapa de registros (anexo) do mesmo, FS e AFS são as seleções de fundo de escala do sensor. Então, já se sabe quais os ranges e os valores brutos que cada um fornecem.
Se buscar no GitHub de Noah Zerkin (https://github.com/bzerk), poderá encontrar o arquivo que disponibilizo como "MPU6050_Original" (anexo), que foi a base do nosso estudo para entender e aplicar o sensor no carro autônomo. Lá, poderá encontrar mais informações sobre cada registro, a matriz 3D de inicialização, os valores que são convertidos em anglos de Euler para exibição no programa Processing, etc.
