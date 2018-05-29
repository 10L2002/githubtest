import cv2
import numpy as np
import random
import os

def cvpaste(img, imgback, x, y, angle, scale):  
    # x and y are the distance from the center of the background image 

    r = img.shape[0]
    c = img.shape[1]
    rb = imgback.shape[0]
    cb = imgback.shape[1]
    hrb=round(rb/2)
    hcb=round(cb/2)
    hr=round(r/2)
    hc=round(c/2)

    # Copy the forward image and move to the center of the background image
    imgrot = np.zeros((rb,cb,3),np.uint8)
    imgrot[hrb-hr:hrb+hr,hcb-hc:hcb+hc,:] = img[:hr*2,:hc*2,:]

    # Rotation and scaling
    M = cv2.getRotationMatrix2D((hcb,hrb),angle,scale)
    imgrot = cv2.warpAffine(imgrot,M,(cb,rb))
    # Translation
    M = np.float32([[1,0,x],[0,1,y]])
    imgrot = cv2.warpAffine(imgrot,M,(cb,rb))

    # Makeing mask
    imggray = cv2.cvtColor(imgrot,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(imggray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of the forward image in the background image
    img1_bg = cv2.bitwise_and(imgback,imgback,mask = mask_inv)

    # Take only region of the forward image.
    img2_fg = cv2.bitwise_and(imgrot,imgrot,mask = mask)

    # Paste the forward image on the background image
    imgpaste = cv2.add(img1_bg,img2_fg)

    return imgpaste

def effect_random(src): #put effect randomly on whole image
    import cv2
    import numpy as np
    import sys
    import random
    import os
    import matplotlib.pyplot as plt

    base =  "image" + "_"
    if not os.path.exists("effect_data"): #name of saving directory
        os.mkdir("effect_data")
    # making lookup table
    min_table = 50
    max_table = 205
    diff_table = max_table - min_table
    gamma1 = 0.5
    gamma2 = 1.5

    #choose 1 effect from 6 types of effect randomly
    x=random.randrange(6)
    #print(x)
    if x==0:
        LUT_HC = np.arange(256, dtype = 'uint8' )
        #making LUT for high contrast
        for i in range(0, min_table):
            LUT_HC[i] = 0
        for i in range(min_table, max_table):
            LUT_HC[i] = 255 * (i - min_table) / diff_table
        for i in range(max_table, 255):
            LUT_HC[i] = 255
        high_cont_img = cv2.LUT(src, LUT_HC)
         #high contrast
        
        return high_cont_img
    if x==1:
        LUT_LC = np.arange(256, dtype = 'uint8' )
        # making LUT for low contrast and gamma correction
        for i in range(256):
            LUT_LC[i] = min_table + i * (diff_table) / 255
            #LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
            #LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)
        low_cont_img = cv2.LUT(src, LUT_LC)
          #low contrast
        
        return low_cont_img
    if x==2:
        LUT_G1 = np.arange(256, dtype = 'uint8' )
        for i in range(256):
            LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
        g1_img=cv2.LUT(src, LUT_G1)
         # when gunnma = 0.5
        
        return g1_img
    if x==3:
        LUT_G2 = np.arange(256, dtype = 'uint8' )
        for i in range(256):
            LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)
        g2_img=cv2.LUT(src, LUT_G2)
        #when gunma = 1.5
        
        return g2_img 
    if x==4:
        row,col,ch= src.shape
        mean = 0
        sigma = 15
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        gauss_img = src + gauss

        
        #gaussian noise
        
        return gauss_img
    if x==5:
        row,col,ch = src.shape
        s_vs_p = 0.5
        amount = 0.004
        out = src.copy()
        # Salt mode
        num_salt = np.ceil(amount * src.size * s_vs_p)
        coords = [np.random.randint(0, i-1 , int(num_salt))
            for i in src.shape]
        out[coords[:-1]] = (255,255,255)

        # Pepper mode
        num_pepper = np.ceil(amount* src.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i-1 , int(num_pepper))
            for i in src.shape]
        out[coords[:-1]] = (0,0,0)
         #salt&pepper noise
        return out






img = cv2.imread('roll_data/img_roll_25.jpeg') #place of sholip logo data ('name of directory/name of images.jpeg')
image_count=800 #number of images that you want put sholip logo
input_data_path='result'# name of directory for input 
output_path='result3' #name of directory for output (saving)

for i in range(image_count):
    if os.path.isfile(input_data_path+ '/image(' + str(i) + ')'+ '.jpeg'): #name of images that you want to put effect(for example 'image(1).jpeg')
        imgback = cv2.imread(input_data_path+'/image('+str(i)+').jpeg')

        rows,cols,channels = imgback.shape
        #print(imgback.shape)
        x=(random.uniform(-cols/4,cols/4)) # x distancec for x axis from center 
        y=(random.uniform(-rows/4,cols/4)) # y y distance from center
        angle=(random.randint(-1, 360)) # decide angle from 0 to 360
        scale=(random.uniform(0.5,2))    # chose the sholipe logo sacale 

        imgpaste = cvpaste(img, imgback, x, y, angle, scale)

        with_effect=effect_random(imgpaste)
        cv2.imwrite(output_path+'/image'+str(i)+'.jpeg', with_effect)
    else:
      print('image' + str(i) + ':No File')
