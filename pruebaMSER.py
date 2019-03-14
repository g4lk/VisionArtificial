import numpy as np
import cv2 as cv
import sys
from os import listdir

def cogerImagen(name_img):
    try:
       img = cv.imread(name_img)
       return img 
    except Exception:
        print('No se puede cargar la imagen,saliendo')
        sys.exit(-1)

if __name__ == '__main__':
    for imagen in os.listdir('./train_10_ejemplos'):
        if 'ppm' in imagen:
            img = cogerImagen(imagen)

    mser = cv.MSER_create()

    while True:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        vis = img.copy()
        # Cogemos las regiones detectadas y sus arrays de coordenadas x,y
        # anchura y altura en ese orden
        regions, x  = mser.detectRegions(gray)
        for rectangle in x:
            # Por cada region encontrada, pintamos su rectangulo
            if (rectangle[2]/rectangle[3] >= 0.8) and (rectangle[2]/rectangle[3]
                                                      <= 1.2):
                cv.rectangle(vis, (rectangle[0],rectangle[1]),
                         (rectangle[0]+rectangle[2],rectangle[1]+rectangle[3]),
                         (0, 255, 0))

        cv.imshow('img', vis)
        if cv.waitKey(5) == 27:
            break
cv.destroyAllWindows()
