# INTRODUÇÃO
Este texo foi elaborado por: Mauro César

Neste trabalho irei apresentar uma forma de detecção de parada de sinal.
Este código leva um sinal de parada "protótipo" (stopPrototype.png) e cria uma pirâmide para fora por meio do downsampling

![image](https://user-images.githubusercontent.com/32276018/33354042-9735a860-d48f-11e7-8193-4ba4c08ab322.png)

# DOWNSAMPLING
Pyramid, ou representação de pirâmide, é um tipo de representação de sinal de escala múltipla desenvolvida pelas comunidades de processamento de imagem, processamento de imagem e processamento de sinal, em que um sinal ou uma imagem está sujeita a suavização repetida e subamostragem. A representação da pirâmide é uma antecessora da representação da escala espacial e da análise de multi-resolução.
"No dataset deste projeto se encontra algumas amostras de imagens!"

Existem dois tipos principais de pirâmides: passagem baixa e passagem de banda.

PASSAGEM BAIXA: Uma pirâmide de passagem baixa é feita suavizando a imagem com um filtro de suavização apropriado e depois submetendo-se a imagem suavizada, geralmente por um fator de 2 ao longo de cada direção de coordenada. A imagem resultante é então submetida ao mesmo procedimento, e o ciclo é repetido várias vezes. Cada ciclo deste processo resulta em uma imagem menor com suavização aumentada, mas com diminuição da densidade de amostragem espacial (ou seja, redução da resolução da imagem). Se ilustrado graficamente, toda a representação em escala múltipla parecerá uma pirâmide, com a imagem original na parte inferior e a imagem menor resultante de cada ciclo empilhada uma sobre a outra.

PASSAGEM DE BANDA: Uma pirâmide de passagem de banda é feita formando a diferença entre imagens em níveis adjacentes na pirâmide e executando algum tipo de interpolação de imagem entre níveis adjacentes de resolução, para permitir a computação de diferenças de pixel. 
![image](https://user-images.githubusercontent.com/32276018/33355113-d60eec36-d494-11e7-8a2b-d9b62f85eb45.png)

# DESCRIÇÃO DO CÓDIGO

 
Calcula o erro quadrático médio entre duas matrizes n-d. Baixa = mais semelhante.

     def meanSquareError(img1, img2):
     assert img1.shape == img2.shape, "Images must be the same shape."
     error = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
     error = error/float(img1.shape[0] * img1.shape[1] * img1.shape[2])
     return error

    def compareImages(img1, img2):
    return 1/meanSquareError(img1, img2)



 Calcula pirâmides de imagens (começa com as amostras original e descendente).
 Adaptado de:
 http://www.pyimagesearch.com/2015/03/16/image-pyramids-with-python-and-opencv/

     def pyramid(image, scale = 1.5, minSize = 30, maxSize = 1000):
     yield image
     while True:
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width = w)
        if(image.shape[0] < minSize or image.shape[1] < minSize):
            break
        if (image.shape[0] > maxSize or image.shape[1] > maxSize):
            continue
        yield image


 "Desliza"uma janela sobre a imagem. Veja para este url para animação legal:
 http://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/
 
 A funçâo range utilizada faz com que o código fique um pouco mais lento pois ela irá imediatamente gerar uma lista  e alocar essa lista na memória.
 
 Já a função xrange irá ter um melhor desempenho devido ela gerar todos de uma só vez economizando espaço na memória e tempo.

     def sliding_window(image, stepSize, windowSize):
        for y in range(0, image.shape[0], stepSize):
           for x in range(0, image.shape[1], stepSize):
               yield (x, y, image[y:y+windowSize[1], x:x+windowSize[1]])

 Pega o o prototipo e a as imagens a qual você colocou para realizar a leitura.
 
     ap = argparse.ArgumentParser()
     ap.add_argument("-i", "--image", required=True, help="Path to the target image")
     ap.add_argument("-p", "--prototype", required=True, help="Path to the prototype object")
     args = vars(ap.parse_args())

     targetImage = cv2.imread(args["image"])
     targetImage = cv2.GaussianBlur(targetImage, (15, 15), 0)
 
 Em uma pirâmide gaussiana, as imagens subsequentes são ponderadas usando uma média gaussiana (borrão gaussiano) e reduzidas. Cada pixel contendo uma média local que corresponde a um bairro de pixels em um nível mais baixo da pirâmide. Esta técnica é usada especialmente na síntese de textura.

     targetImage = imutils.resize(targetImage, width=500)
     prototypeImg = cv2.imread(args["prototype"])

     maxSim = -1
     maxBox = (0,0,0,0)

     t0 = time.time()

Possível erro pode ocorrer pela formatação de espaço por tab.

      for p in pyramid(prototypeImg, minSize = 50, maxSize = targetImage.shape[0]):
      for (x, y, window) in sliding_window(targetImage, stepSize = 2, windowSize = p.shape):
        if window.shape[0] != p.shape[0] or window.shape[1] != p.shape[1]:
            continue

        tempSim = compareImages(p, window)
        if(tempSim > maxSim):
           maxSim = tempSim
           maxBox = (x, y, p.shape[0], p.shape[1])

    t1 = time.time()

    print("Execution time: " + str(t1 - t0))
    print(maxSim)
    print(maxBox)
    buff1 = 10
    (x, y, w, h) = maxBox
 
 Possível erro pode ocorrer devido a tranformação para inteiro fazendo com que baixe assim a resolução.No caso de pegar uma imagem grande ele tera dificuldade de realizar a leitura de toda extensão da mesma, fazendo com que print somente uma área padrão ja definida anteriormente.

     cv2.rectangle(targetImage,(int(x-buff1/2),int(y-buff1/2)),(int(x+w+buff1/2),int(y+h+buff1/2)),(0,255,0),2)
     cv2.imshow('image', targetImage)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
![image](https://user-images.githubusercontent.com/32276018/33354906-e3cd6268-d493-11e7-889c-c98dd0b6a6e3.png)


# PASSOS PARA REALIZAR

Primeiro passo é instalar os updates
sudo apt-get update

INSTALANDO O ANACONDA

cd /tmp

curl -O https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh

sha256sum Anaconda3-4.2.0-Linux-x86_64.sh

bash Anaconda3-4.2.0-Linux-x86_64.sh

#CASO ERRE:
export PATH="/home/<user>/anaconda3/bin:$PATH" #Replace <user> with the actual path name
source ~/.bashrc
#Install Conda
 
 
SELECIONAR O COMPARTIMENTO NO QUAL IRA BAIXAR OS GIT NECESÁRIOS 
cd ~

git clone https://github.com/afonsohfontes/car-behavioral-cloning.git

cd ~

CRIANDO O AMBIENTE DE CRIAÇÃO
cd car-behavioral-cloning
conda env create -f environment.yml

ATIVANDO O AMBIENTE
source activate car

INSTALANDO ALGUNS PIPs ESSENCIAIS PARA O PROJETO
sudo pip install opencv-python
conda install -c menpo opencv 
sudo apt-get install python-pip python-dev ipython
sudo apt-get install bluetooth libbluetooth-dev
sudo pip install pybluez
pip install -i https://pypi.anaconda.org/pypi/simple pybluez
sudo apt-get install python-pygame
 
 ENTRANDO NA PASTA NO QUAL IRA BAIXAR O GITHUB
cd ~

git clone https://github.com/Barros92/detec-o-de-parada-de-sinal.git
cd ~
source active car
 python detectStopSigns.py -p stopPrototype.png -i Stop\ Sign\ Dataset/3.jpg

ATUALIZAÇÃO DOS UPGRADES E UPDATES
sudo apt-get dist-upgrade
sudo apt-get update
 



