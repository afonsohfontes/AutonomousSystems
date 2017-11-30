# INSTALAÇAO DO RASPIBIAN NO RASPBERRY PI 3
Este texto foi elaborado por: Rafael Bezerra Melo Sousa Lemos

O Raspbian é um sistema operacional desenvolvido inicialmente para ser usado em conjunto com o Raspberry Pi Zero, mas desde então foram feitas várias atualizações no software.

![image](https://user-images.githubusercontent.com/32318386/33293477-1333352c-d3b4-11e7-9a9f-13e9f4da7098.png)

Para a instalação do software é necessário um cartão de memória SD de pelo menos 8GB de espaço, e recomendado um SD com 16GB de memória, o cartão precisa estar completamente livre, de preferência formatado para uma instalação mais segura do SO.

Foi usado um segundo programa chamado Etcher para a instalação do Raspibian no cartão de memória. O passo a passo da instalação foi a seguinte:

1 – Download do Software Etcher e Raspibian, ambos se encontram no site dos seus fornecedores;

2 – Em seguida abrimos o programa Etcher e selecionamos a imagem que será instalada no cartão SD;

3 – O software irá reconhecer e escolher automaticamente o cartão de memória no qual será instalado o RaspibiaN;

4 – Por fim é necessário selecionar a opção “Flash!” e o Raspibian é instalado no cartão de memória SD.

Seguem as imagens do passo-a-passo.

![image](https://user-images.githubusercontent.com/32318386/33293596-7fdb65e6-d3b4-11e7-9ddf-81f3131c556e.png)

![image](https://user-images.githubusercontent.com/32318386/33293626-98acb4bc-d3b4-11e7-8a48-29e00ea51b6d.png)

![image](https://user-images.githubusercontent.com/32318386/33293649-a9e91fa4-d3b4-11e7-8f00-c374046b2232.png)

# INSTALAÇÃO DO PYTHON 3.0 E OPENCV

Nessa parte do projeto seguiremos com um passo a passo para a instalção do Python v 3.0 e do OpenCV, o Python 3.0 é essencial para conseguirmos rodar os programas desse projeto e o OpenCV é o ambiente em que os programas serão rodados.

# 1) Instalações Básicas

O primeiro passo é instalar os updates e upgrades existentes para seu raspbian:
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
Agora iremos instalar algumas ferramentas como o CMake, que ajuda na configuração do OpenCV
```
$ sudo apt-get install build-essential cmake pkg-config
```
Em seguida, iremos instalar pacotes I/O de leitura de imagens (JPEG, PNG, TIFF, etc)
```
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```
E agora faremos o mesmo para pacotes I/O de leitura de vídeos.
```
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidecore-dev libx264-dev
```
A biblioteca OpenCV possui um sub-módulo chamado highhui que é usado para mostrar imagens básicas na sua interface. A linha de codigo seguinte serve para a instalação dessa biblioteca.
```
$ sudo apt-get install libgtk2.0-dev

$ sudo apt-get install libatlas-base-dev gfortran
```
E por fim iremos instalar tanto o python 2.7 e o 3.0
```
$ sudo apt-get install python2.7-dev python3-dev
```
# 2) Download do código fonte OpenCV

Agora que temos as instalações básicas necessárias iremos baixar o OpenCV do repositório oficial OpenCV. Se houver uma versão nova do Open CV se substitui o número da versão na linha de código.
```
$ cd ~
$ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
$ unzip opencv.zip
```
Agora iremos instalar completamente o OpenCV 3 e para isso também precisaremos requerer o opencv_contrib do repositório.
```
$ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
$ unzip opencv_contrib.zip
```
# 3) Ambiente Virtual Python 3.0

Antes de compilar o OpenCV no Raspberry Pi 3, primeiramente iremos instalar o "pip", um módulo Python essencial.
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
$ sudo pip install virtualenv virtualenvwrapper
$ sudo rm -rf ~/.cache/pip
```
Agora será necessário a atualização do "~/.profile" com as seguintes linhas de código:
```
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

$ echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
$ echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
```
Já que temos o nosso profile atualizado necessitamos resetar o ~/.profile.
```
$ source ~/.profile
```
Finalmente poderemos criar o nosso ambiente virtual python, para a criação de um abiente 2.7 usamos a seguitne linha de código.
```
$ mkvirtualenv cv -p python2
```
E para um Python 3.0 usamos, fique atento pois para usarmos nesse projeto é essencial que usemos o Python 3.0.
```
$ mkvirtualenv cv -p python3
```
# Checando se o CV está instalado

Usaremos as seguintes linhas de código para confirmarmos a instação do ambiente virtual.
```
$ cd~
$ source ~/.profile
$ workon cv
```
Enfim falta apenas instalar a dependencia usada para processamentos numericos, NumPy.
```
$ pip install numpy
```
# 4) Compilar OpenCV

Primeiramente temos que ter certeza que estamos de fato dentro do ambiente virtual, verifique se há uma identificação "cv" na sua linha de diretório.
``` 
$ workon cv
```
Agora vamos instalar nosso CMake
```
$ cd ~/opencv-3.1.0/
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE 
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D BUILD_EXAMPLES=ON ..
```   
Estamos prontos para compilar o OpenCV
```
$ make -j4
$ make clean
$ make
```
E agora precisamos apenas terminar a instalação.
```
$ sudo make install
$ sudo ldconfig
```
# 5) Testando a Instalação

Finalmente se tudo ocorreu como o desejado poderemos ver se o OpenCV está funcionando corretamente.
```
$ source ~/.profile 
$ workon cv
$ python
```

