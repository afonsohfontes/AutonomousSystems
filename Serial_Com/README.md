# INSTALAÇÃO DO PYTHON 3.0 E OPENCV

Nessa parte do projeto seguiremos com um passo a passo para a instalção do Python v 3.0 e do OpenCV, o Python 3.0 é essencial para conseguirmos rodar os programas desse projeto e o OpenCV é o ambiente em que os programas serão rodados.

# 1) Instalações Básicas

O primeiro passo é instalar os updates e upgrades existentes para seu raspbian:

$ sudo apt-get update
$ sudo apt-get upgrade

Agora iremos instalar algumas ferramentas como o CMake, que ajuda na configuração do OpenCV

$ sudo apt-get install build-essential cmake pkg-config

Em seguida, iremos instalar pacotes I/O de leitura de imagens (JPEG, PNG, TIFF, etc)

$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

E agora faremos o mesmo para pacotes I/O de leitura de vídeos.

$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidecore-dev libx264-dev


