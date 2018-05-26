def roll_pic(src): #roll sholip logo at random angle
    import cv2
    import numpy as np
    import random
    import os

    if not os.path.exists("roll_data"): #name of saving directory
            os.mkdir("roll_data")
    # 画像読み込み(read image)
   
    h, w = src.shape[:2]
    size = (w, h)

    # 回転角の指定(decide the angle)
    x=(random.randint(0, 360))
    #print(x)
    angle = x
    angle_rad = angle/180.0*np.pi

    # 回転後の画像サイズを計算(caluculate the size of image after rotation)
    w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
    h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
    size_rot = (w_rot, h_rot)

    # 元画像の中心を軸に回転する(pick the center from original image and rotate)
    center = (w/2, h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

    # 平行移動を加える (rotation + translation)
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
    affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2

    img_rot = cv2.warpAffine(src, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)


    cv2.imwrite("roll_data/"  +"img_roll.jpeg" ,img_rot)

    
#import cv2
#import numpy as np
#import random
#import os
#src_img = cv2.imread("./pra/sholip.png")
#roll_pic(src_img)
