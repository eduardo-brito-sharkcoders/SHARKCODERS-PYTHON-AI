import cv2
import random

img = cv2.imread('assets/imagem1.jpg', -1)
img = cv2.resize(img, (400, 400))

bocadinho = img[60:90, 245:275] # -- selecionamos o nosso "bocadinho" a copiar (linhas de pixeis 60 a 90, colunas 245 a 275) -- #
img[360:390, 360:390] = bocadinho # -- atribuímos às linhas e colunas 360 a 390 o "bocadinho" que copiámos -- #

for i in range(100): # -- numero de linhas a alterar -- #
    for j in range(img.shape[1]): # -- numero de colunas a alterar -- #
        img[i][j] = [random.randint(0, 0),
                     random.randint(0, 0),
                     random.randint(0, 255)]

cv2.imshow('Janela da imagem', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
