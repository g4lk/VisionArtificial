# Write Python code here
# import the necessary packages 
import cv2 as cv
import os,sys
import numpy as np



def mejorContraste(img):
    #-----Converting image to LAB Color model-----------------------------------

    lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return final

#https://stackoverflow.com/questions/32522989/opencv-better-detection-of-red-color/32523532?noredirect=1#comment74897695_32523532
def generarMascaraRojos(img):
    inversa = ~img
    hsv_inversa = cv.cvtColor(inversa,cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_inversa,np.array([90-10, 10, 70]),np.array([90+10, 255, 255]))
    return mask

# Mascaras: circular,triangular,octogonal
count_c, count_t, count_o = 0, 0, 0
contador_c, contador_t, contador_o = np.zeros(shape=(25, 25, 3)), np.zeros(shape=(25, 25, 3)), np.zeros(shape=(25, 25, 3))
for dir in os.listdir('./train_recortadas/'):
    for dir2 in os.listdir(f'./train_recortadas/{dir}/'):
        for imagen in os.listdir(f'./train_recortadas/{dir}/{dir2}/'):
            img = cv.imread(f'./train_recortadas/{dir}/{dir2}/{imagen}')
            image = mejorContraste(img)
            mask = generarMascaraRojos(image)
            res = cv.bitwise_and(image, image, mask=mask)
            if dir == 'obligacion':
                count_c += 1
                contador_c = cv.add(contador_c, np.float64(cv.resize(res, (25, 25))))
            elif dir == 'peligro':
                count_t += 1
                contador_t = cv.add(contador_t, np.float64(cv.resize(res, (25, 25))))
            elif dir == 'stop':
                count_o += 1
                contador_o = cv.add(contador_o, np.float64(cv.resize(res, (25, 25))))
np.set_printoptions(threshold=sys.maxsize)
mc = np.uint8(np.divide(contador_c,count_c))
mt = np.uint8(np.divide(contador_t,count_t))
mo = np.uint8(np.divide(contador_o,count_o))
cv.imshow('mc',cv.resize(mc, (250,250)))
cv.imshow('mt',cv.resize(mt, (250,250)))
cv.imshow('mo',cv.resize(mo, (250,250)))
cv.waitKey(0)
print('MC:' + str(mc))
print('MT:' + str(mt))
print('MO:' + str(mo))


# close all open windows 
cv.destroyAllWindows()
