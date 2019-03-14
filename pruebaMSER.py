
import numpy as np
import cv2 as cv
import sys

def cogerImagen(name_img):
    try:
       img = cv.imread(name_img)
       return img
    except Exception:
        print('No se puede cargar la imagen,saliendo')
        sys.exit(-1)

def hazmeCuadrado(rectangulo):
    x = rectangulo[0] - 15
    y = rectangulo[1] - 15
    return np.array([x,y,50,50])

if __name__ == '__main__':
    img = cogerImagen('./train_10_ejemplos/00006.ppm')
    mser = cv.MSER_create()

    while True:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        vis = img.copy()
        # Cogemos las regiones detectadas y sus arrays de coordenadas x,y
        # anchura y altura en ese orden
        regions, x  = mser.detectRegions(gray)
        for rectangle in x:
            # Por cada region encontrada, pintamos su rectangulo
     #       if (rectangle[2]/rectangle[3] >= 0.65) and (rectangle[2]/rectangle[3] <= 1.35):
                cuadrado = hazmeCuadrado(rectangle)
                cv.rectangle(vis,(cuadrado[0],cuadrado[1]),
                             (cuadrado[0] + cuadrado[2],cuadrado[1] +
                              cuadrado[3]),(0,255,0))

        cv.imshow('img', vis)
        if cv.waitKey(5) == 27:
            break
cv.destroyAllWindows()
