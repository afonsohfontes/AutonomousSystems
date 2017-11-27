import cv2
import pickle
import numpy as np
import scipy.misc as sci
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from skimage import io




from calibrate import undist
from threshold_helpers import *

'''
Carregar matriz de transformação da camera. 
'''
with open('test_dist_pickle.p', 'rb') as pick:
  dist_pickle = pickle.load(pick)

mtx = dist_pickle['mtx']
dist = dist_pickle['dist']

'''
deforma a pespectiva baseada em 4 pontos.
pontos ideais do webinar da Udacity no cálculo dos melhores pontos.
'''
def change_perspective(img):
  img_size = (img.shape[1], img.shape[0])
  bot_width = .76
  mid_width = 1
  height_pct = 1
  bottom_trim = 1
  offset = img_size[0]*0.1
  

  
  dst = np.float32([[0, 320], [240, 320], [240, 0], [0, 0]])
  src = np.float32([[0, 250], [240, 250], [240, 150], [0, 150]])
 
 
  plt.imshow(img)
  plt.title('lines')
  plt.show()

  
  M = cv2.getPerspectiveTransform(src, dst)

  warped = cv2.warpPerspective(img, M, (img_size[0], img_size[1]))
  return warped

'''
Obtenha os pixels para as pistas esquerda e direita e devolva-os.
a maior parte do código das palestras da Udacity sobre o cálculo da curvatura.
'''
def lr_curvature(binary_warped):
  
  histogram = np.sum(binary_warped[150:,:], axis=0)
  
  

  midpoint = np.int(histogram.shape[0]/2)
  leftx_base = np.argmax(histogram[:midpoint])
  rightx_base = np.argmax(histogram[midpoint:]) + midpoint

  # Escolha o número de janelas deslizantes.
  nwindows = 50
  # Definir altura das janelas.
  window_height = np.int(binary_warped.shape[0]/nwindows)
  # Identifique as posições x e y de todos os pixels não nítidos na imagem. 
  nonzero = binary_warped.nonzero()
  nonzeroy = np.array(nonzero[0])
  nonzerox = np.array(nonzero[1])
  # Posições atuais a serem atualizadas para cada janela.
  leftx_current = leftx_base
  rightx_current = rightx_base
  # Defina a largura da janela +/- margem.
  margin = 20
  # Defina o número mínimo de pixels encontrados na janela mais recente.
  minpix = 12
  # Crie listas vazias para receber índices de pixels da pista esquerda e direita.
  left_lane_inds = []
  right_lane_inds = []

  # Passar pelas janelas uma a uma.
  for window in range(nwindows):
      # Identifique os limites das janelas em x e y (e direita e esquerda).
      win_y_low = binary_warped.shape[0] - (window+1)*window_height
      win_y_high = binary_warped.shape[0] - window*window_height
      win_xleft_low = leftx_current - margin
      win_xleft_high = leftx_current + margin
      win_xright_low = rightx_current - margin
      win_xright_high = rightx_current + margin
      # Desenhe as janelas na imagem de visualização.
      good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
      good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
      # Anexe esses índices às listas.
      left_lane_inds.append(good_left_inds)
      right_lane_inds.append(good_right_inds)
      # Se você encontrou pixels maiores que o numero minimo de pixels, janela próxima mais recente na posição média.
      if len(good_left_inds) > minpix:
          leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
      if len(good_right_inds) > minpix:        
          rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

  # Concatenar os arrays de índices.
  left_lane_inds = np.concatenate(left_lane_inds)
  right_lane_inds = np.concatenate(right_lane_inds)

  # Extraia as posições de pixel da linha esquerda e direita.
  leftx = nonzerox[left_lane_inds]
  lefty = nonzeroy[left_lane_inds] 
  rightx = nonzerox[right_lane_inds]
  righty = nonzeroy[right_lane_inds] 

  # Ajustar um polinômio de segunda ordem a cada.
  left_fit = np.polyfit(lefty, leftx, 2)
  right_fit = np.polyfit(righty, rightx, 2)
  # Neste ponto, você está pronto! Mas aqui é como você também pode visualizar o resultado:
  # Gerar valores x e y para traçar.
  ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )
  left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
  right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]


  #converter pixels para metros.
  ym_per_pix = 30/720
  xm_per_pix = 3.7/700

  left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, 2)
  right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, 2)

  #calcular o raio da curvatura.
  left_eval = np.max(lefty)
  right_eval = np.max(righty)
  left_curverad = ((1 + (2*left_fit_cr[0]*left_eval + left_fit_cr[1])**2)**1.5)/np.absolute(2*left_fit_cr[0])
  right_curverad = ((1 + (2*right_fit_cr[0]*right_eval + right_fit_cr[1])**2)**1.5)/np.absolute(2*right_fit_cr[0])

  # calcule left_min ao encontrar o valor mínimo no primeiro índice de matriz.
  left_min = np.amin(leftx, axis=0)
  right_max = np.amax(rightx, axis=0)
  actual_center = (right_max + left_min)/2
  print("centro da faixa = ", actual_center)
  dist_from_center =  actual_center - (240/2)

  meters_from_center = xm_per_pix * dist_from_center
  string_meters = str(round(meters_from_center, 2))
  full_text = dist_from_center


  return full_text, actual_center
  

'''
execute uma máscara com certos índices.
'''
def region_of_interest(img, vertices):
    """
    Aplica uma máscara de imagem.
    
    Apenas mantém a região da imagem definida pelo polígono
    formado a partir de "vértices". O resto da imagem está definido para preto.
    """
    #definindo uma máscara em branco para começar.
    mask = np.zeros_like(img)   
    
    #definindo uma cor de 3 canais ou 1 canal para preencher a máscara dependendo da imagem de entrada.
    if len(img.shape) > 2:
        channel_count = img.shape[2]  
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #preenchendo pixels dentro do polígono definido por "vértices" com a cor de preenchimento.
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero.
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

'''
Dado valores das linhas esquerda e direita, adicione à imagem original.
'''
def draw_on_road(img, warped, left_fitx, left_yvals, right_fitx, right_yvals, ploty):
  #crie uma imagem para desenhar as linhas.
  warp_zero = np.zeros_like(warped).astype(np.uint8)
  color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

  #reformule x e y no formato utilizável para cv2.fillPoly.
  pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
  pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
  #print('pts left', pts_left.shape, 'pts right', pts_right.shape)
  pts = np.hstack((pts_left, pts_right))

  #dtrace a linha na imagem em branco deformada.
  cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))

  img_size = (img.shape[1], img.shape[0])

  bot_width = .76
  mid_width = .08
  height_pct = .62
  bottom_trim = .935
  offset = img_size[0]*.25

  dst = np.float32([[img.shape[1]*(.5 - mid_width/2), img.shape[0]*height_pct], [img.shape[1]*(.5 + mid_width/2), img.shape[0]*height_pct],\
   [img.shape[1]*(.5 + bot_width/2), img.shape[0]*bottom_trim], [img.shape[1]*(.5 - bot_width/2), img.shape[0]*bottom_trim]])
  src = np.float32([[offset, 0], [img_size[0] - offset, 0], [img_size[0] - offset, img_size[1]], [offset, img_size[1]]])

  cv2.fillConvexPoly(image, src, 1)
  Minv = cv2.getPerspectiveTransform(src, dst)

  #warp the blank back oto the original image using inverse perspective matrix.
  newwarp = cv2.warpPerspective(color_warp, Minv, (img.shape[1], img.shape[0]))

  #combine o resultado com o original
  result = cv2.addWeighted(img, 1, newwarp, 0.3, 0)
  return result

'''
Executa todos os passos para processo da imagem. 
0. Undistort a imagem.
1. Criação dos limites binários.
2. Mudar pespectiva para birds-eye-view.
3. Calcula a curvatura das linhas da esquerda e direita.
4. Mapeia de volta para a pista.
'''
def process_image(img):

  undist_img = undist(img, mtx, dist)

  combo_image = combo_thresh(img)

  warped_image = change_perspective(combo_image)
  
  result, actual_center = lr_curvature(warped_image)
  linha = np.array([[actual_center, 0], [actual_center, 320]], np.int32);
  masked_image = region_of_interest(img, [linha])#aqui era undist_img
  BlendImage = cv2.addWeighted(img, 1, masked_image, 0.3, 0)
  plt.imshow(BlendImage, cmap='gray') 
  plt.title('masked_image')
  plt.show()

  return result


'''
crie uma classe de linha para acompanhar informações importantes sobre cada linha
'''
class Lane():
  def __init__(self):
    #Se a lane foi detectada na última iteração
    self.curve = {'full_text': ''}

if __name__ == '__main__':
  
 
  lane = Lane()
  
  while(True):
   try: 
     start_time = time.time()
     #image = io.imread("http://192.168.43.1:8080/photo.jpg")
     image = io.imread("test2.jpg")
     src = np.float32([[0, 480], [640, 480], [640, 0], [0,0]])
     dst = np.float32([[0, 320], [240, 320], [240, 0], [0,0]])
     #M = cv2.getRotationMatrix2D((image.shape[1]/2,image.shape[0]/2),270,1)
     #image1 = cv2.warpAffine(image,M,(image.shape[1],image.shape[0]))
     S = cv2.getPerspectiveTransform(src, dst)
     warped = cv2.warpPerspective(image, S, (240,320))
     colored_image = process_image(warped)
     #print("--- %s seconds ---" % (time.time() - start_time))
     print("distancia para o centro = ", colored_image)
    #plt.imshow(colored_image, cmap='gray')
    #plt.title('colored_image')
    #plt.show()
   except: 
    print("erro")
    pass
     

