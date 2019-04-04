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
    
    x = rectangulo[0]
    y = rectangulo[1]
    w = rectangulo[2]
    h = rectangulo[3]
    centroX = round(x + w/2)
    centroY = round(y + h/2)
    if w > h:
        w = int(round(w * 1.4)) 
        h = w
    else:
        h = int(round(h * 1.4))
        w = h
    x = int(round(centroX - w/2))
    y = int(round(centroY - h/2))
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
                # Por cada region encontrada, pintamos su rectangulo
                if (rectangle[2]/rectangle[3] >= MIN_DIVISION) and (rectangle[2]/rectangle[3] <= MAX_DIVISION):
                    x,y,w,h = hazmeCuadrado(rectangle)
                   # cv.rectangle(vis,(x,y),(x + w, y + h),(0,255,0))
                    imgnew = imgcontraste[y:y+h,x:x+w]
                    while True:
                        #cv.imshow('img',imgnew)
                        img_hsv=cv.cvtColor(imgnew, cv.COLOR_BGR2HSV)
                         #Cogemos el cuadrado (imagen recortada)
                        new_img = img[y:y+h, x:x+w]
                        hsv = cv.cvtColor(new_img, cv.COLOR_BGR2HSV)

                        # Cogemos los 2 rangos posibles de rojos
                        rojo_bajos1 = np.array([0, 65, 75])
                        rojo_altos1 = np.array([12, 255, 255])
                        rojo_bajos2 = np.array([240, 65, 75])
                        rojo_altos2 = np.array([256, 255, 255])
                        # Buscamos los colores dentro dentro de los limites establecidos y aplicamos la mascara
                        mascara_rojo1 = cv.inRange(hsv, rojo_bajos1,rojo_altos1)  # Establezco valores de H y S que detecten el rojo
                        mascara_rojo2 = cv.inRange(hsv, rojo_bajos2, rojo_altos2)
                        # Unimos las dos mascaras rojo
                        mask3 = cv.add(mascara_rojo1, mascara_rojo2)

                        #Aplicamos la mascara a la imagen

                        res = cv.bitwise_and(new_img, new_img, mask=mask3)
                        circles = cv.HoughCircles(cv.cvtColor(new_img,
                                                              cv.COLOR_BGR2GRAY)
                                                  ,cv.HOUGH_GRADIENT,1,200,param1=50,param2=30,minRadius=0,maxRadius=0)
                        if circles is not None:
                            # convert the (x, y) coordinates and radius of the circles to integers
                            circles = np.round(circles[0, :]).astype("int")

                            # loop over the (x, y) coordinates and radius of the circles
                            for (x, y, r) in circles:
                            # draw the circle in the output image, then draw a rectangle
                            # corresponding to the center of the circle
                                cv.circle(res, (x, y), r, (0, 255, 0), 2)
                        resFinal = cv.resize(res, (300,300))
                        imgOriginal = cv.resize(new_img, (300,300))
                        cv.imshow('Imagen original', imgOriginal)
                        cv.imshow('Imagen con mascara',resFinal)
                        if cv.waitKey(5) == 27:
                            break
        #    cv.imshow('img', vis)
        #    if cv.waitKey(5) == 27:
        #        break
cv.destroyAllWindows()
