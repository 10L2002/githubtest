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
    LUT_HC = np.arange(256, dtype = 'uint8' )
    LUT_LC = np.arange(256, dtype = 'uint8' )
    LUT_G1 = np.arange(256, dtype = 'uint8' )
    LUT_G2 = np.arange(256, dtype = 'uint8' )

    #making LUT for high contrast
    for i in range(0, min_table):
        LUT_HC[i] = 0
    for i in range(min_table, max_table):
        LUT_HC[i] = 255 * (i - min_table) / diff_table
    for i in range(max_table, 255):
        LUT_HC[i] = 255

    # making LUT for low contrast and gamma correction
    for i in range(256):
        LUT_LC[i] = min_table + i * (diff_table) / 255
        LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1) 
        LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)
        
    # add gauss noise   
    row,col,ch= src.shape
    mean = 0
    sigma = 15
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    gauss_img = src + gauss

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
        
    # put effect 
    high_cont_img = cv2.LUT(src, LUT_HC) 
    low_cont_img = cv2.LUT(src, LUT_LC)
    g1_img=cv2.LUT(src, LUT_G1)
    g2_img=cv2.LUT(src, LUT_G2)

    #choose 1 effect from 6 types of effect randomly
    x=random.randrange(5)
    #print(x)
    if x==0:
        cv2.imwrite("effect_data/" + base +"high_cont.jpeg" ,high_cont_img) #high contrast 
    if x==1:
        cv2.imwrite("effect_data/" + base +"low_cont.jpeg" ,low_cont_img)  #low contrast
    if x==2:
        cv2.imwrite("effect_data/" + base +"gunnma1.jpeg" ,g1_img) # when gunnma = 0.5
    if x==3:
        cv2.imwrite("effect_data/" + base +"gunnma2.jpeg" ,g2_img) #when gunma = 1.5
    if x==4:
        cv2.imwrite("effect_data/" + base +"gauss.jpeg" ,gauss_img) #gaussian noise
    if x==5:
        cv2.imwrite("effect_data/" + base +"salt_pepper.jpeg" ,out) #salt&pepper noise


