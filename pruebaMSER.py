import numpy as np
import cv2 as cv
import sys,os

#ZONA DEFINICIÓN DE CONSTANTES
MAX_DIVISION = 1.15
MIN_DIVISION = 0.85


def cogerImagen(name_img):
    try:
       img = cv.imread(name_img)
       return img
    except Exception:
        print('No se puede cargar la imagen,saliendo')
        sys.exit(-1)

def hazmeCuadrado(rectangulo):
    x = int(round(rectangulo[0] * 0.99))
    y = int(round(rectangulo[1] * 0.98))
    w = rectangulo[2]
    h = rectangulo[3]
    if w > h:
        w = int(round(w * 1.25)) 
        h = w
    else:
        h = int(round(h * 1.25))
        w = h
    return np.array([x,y,w,h])


# Mejor contraste en imagen: sacado de https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
def mejorContraste(img):
    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return final

if __name__ == '__main__':


    for imagen in os.listdir('./train_10_ejemplos/'):
        img = cogerImagen(f'./train_10_ejemplos/{imagen}')
        imgcontraste = mejorContraste(img)
        mser = cv.MSER_create(_delta = 7, _max_area =20000,
                              _max_variation = .15)

        while True:
            gray = cv.cvtColor(imgcontraste, cv.COLOR_BGR2GRAY)
            # Cogemos las regiones detectadas y sus arrays de coordenadas x,y
            # anchura y altura en ese orden

            regions, x  = mser.detectRegions(gray)
            vis = img.copy()
            for region,rectangle in zip(regions,x):
                breakpoint();
                # Por cada region encontrada, pintamos su rectangulo
                if (rectangle[2]/rectangle[3] >= MIN_DIVISION) and (rectangle[2]/rectangle[3] <= MAX_DIVISION):
                    x,y,w,h = hazmeCuadrado(rectangle)
                    cv.rectangle(vis,(x,y),(x + w, y + h),(0,255,0))

            cv.imshow('img', vis)
            if cv.waitKey(5) == 27:
                break
cv.destroyAllWindows()
