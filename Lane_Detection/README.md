Autores: 
<a href="https://github.com/AndreVTavares">AndreTavares</a>
<a href="https://github.com/nunesian">IaN.</a>

# Procedimentos

Utilizando o Anaconda Navigator(https://anaconda.org/anaconda/anaconda-navigator) para rodar o programa em python, seguindo os seguintes passos:

![image](https://user-images.githubusercontent.com/31252029/33347808-e866fef4-d472-11e7-8353-5c982476c267.png)

Nesta imagem já possui o environment utilizado por nós (carroIA). Quando iniciado um novo projeto será necessario criar um novo environment clique em create, depois de criado o environment e inicializado o prompt de comandos do python, clicando em open terminal.

![image](https://user-images.githubusercontent.com/31252029/33348059-a78a1064-d473-11e7-9138-fe16bf9f50e2.png)

Em seguida é realizado o comando a seguir: cd <diretório onde se encontra o programa em python>.

![image](https://user-images.githubusercontent.com/31252029/33348195-26530e82-d474-11e7-8b0e-31b082ffba80.png)

Em seguida é realizado o codigo acima: python nome do programa.py 

# Tratamento de Imagem

O algoritmo de tratamento de imagem tem o objetivo de identificar duas linhas (contínuas ou não) ao longo da pista que serão limitantes do espaço por onde o carro pode trafegar uma vez que ele deve permanecer em uma mesma faixa da via durante o trajeto.

Após a aquisição da imagem o primeiro passo é corrigir a distorção gerada pela câmera, isso se faz necessário para que tenhamos uma imagem mais fiel à realidade para identificar com precisão a distância entre as linhas de uma faixa.

Uma vez que a imagem foi corrigida estamos aptos a iniciar a identificação das linhas; para isso aplicamos filtros (thresholders) que colorem todos os pixels da foto em preto ou branco, isso nos ajudará a diferenciar as linhas da pista de quaisquer outros obstáculos existentes. Combinamos os resultados da aplicação destes filtros para obter uma imagem mais limpa, isto é, com quantidade reduzida de ruídos que possam confundir o robô. Os filtros utilizados estão descritos na tabela abaixo e podem ser encontrados em "thresholders.py" (créditos-<a href="https://github.com/BillZito">BillZito</a>)

![image](https://github.com/afonsohfontes/AutonomousSystems/blob/master/Lane_Detection/tabela.png) 

Então utilizamos uma matriz de transformação para mudar a perspectiva da imagem, para tanto são definidos quatro pontos na foto original que serão transformados. A escolha desses pontos deve ser feita dentro da região de interesse na imagem, isto é, apenas a pista deve estar contida neste retângulo. Após a transformação, em vez da visão ao nível da via simularemos uma visão aérea que torna as linhas aproximadamente paralelas e com curvatura semelhante.

A função lr_curvature() identifica os pixels brancos (nonzero pixels) na imagem e desenha janelas de tamanho fixo enquadrando esses pixels. A partir das coordenadas das regiões com maior densidade de pixels válidos são geradas duas funções polinomiais que descrevem linhas semelhantes às linhas à direita e esquerda de uma faixa. A partir do vetor de coordenadas horizontais dos pixels válidos selecionamos o pixel extremo da direita e da esquerda e calculamos a média simples dessas extermidades para obter o ponto médio entre elas, ou seja, o centro da faixa. Por fim obtemos a medida do desvio do carro em relação ao centro da faixa subtraindo o valor do centro da imagem (largura da imagem dividida por 2) do valor do centro da faixa.

Estes cálculos fornecem o resultado em pixels; opcionalmente é possível fazer uma conversão de pixels para metros desde que se conheça a largura e o comprimento (em metros) de uma faixa da via dentro da região de interesse.







