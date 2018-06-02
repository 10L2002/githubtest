import numpy as np
import matplotlib.pyplot as plt
import cv2

def generate_points(src,a,b,center_x,center_y): #this function returns the rotated point according to the given angle(ba)
    b= np.matrix([center_x+src[0], center_y+src[1]]).A1
    pythagoras = b- a
    r = np.sqrt( (pythagoras[0] * pythagoras[0]) + (pythagoras[1] * pythagoras[1] ))
    # tan theta (Inclination)
    tant = (b[1] - a[1]) / (b[0] - a[0])
    # theta
    tan = np.arctan(tant)
    # AD = r*cos α
    # BD = r*sin α
    AD = r * np.cos(tan)
    BD = r * np.sin(tan)
    theta = np.deg2rad(ba) # angle

    rotateMat = np.matrix([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)],
    ])
    xy = np.matrix([[AD], [BD]])

    cxy = (rotateMat * xy)
    cxy = cxy.A1 + a
    # cx = AD*cos θ-BD*sin θ+ax
    # cy = AD*sin θ+BD*cos θ+ay
    AD2 = b[0] - a[0]
    BD2 = b[1] - a[1]
    cx = ((AD2 * np.cos(theta)) - (BD2 * np.sin(theta))) + a[0]
    cy = ((AD2 * np.sin(theta)) + (BD2 * np.cos(theta))) + a[1]
    out=[cx,cy]
    return out




def generate_box(Pc,bx,by,ba,bs):
    if Pc==1:
        img2 =(cv2.imread('**',cv2.IMREAD_COLOR)) #images including logo
        
        center_x=(img2.shape[1])/2-bx   #x coordinate of center of logo 
        center_y=(img2.shape[0])/2+by   # y coordinate of center of logo
        a = np.matrix([center_x, center_y]).A1

        img_logo= cv2.imread('**')   # file name oflogo 
        y=img_logo.shape[0]
        x=img_logo.shape[1]

        src=[-x*bs/2,y*bs/2]    
        b= np.matrix([center_x+src[0], center_y+src[1]]).A1    
        result=generate_points(src,a,b,center_x,center_y)    # point1 after rotation

        src=[-x*bs/2,-y*bs/2]
        b2= np.matrix([center_x+src[0], center_y+src[1]]).A1
        result2=generate_points(src,a,b,center_x,center_y)   # point2 after rotation

        src=[x*bs/2,-y*bs/2]
        b3= np.matrix([center_x+src[0], center_y+src[1]]).A1
        result3=generate_points(src,a,b,center_x,center_y)   # point3 after rotation

        src=[x*bs/2,y*bs/2]
        b4= np.matrix([center_x+src[0], center_y+src[1]]).A1
        result4=generate_points(src,a,b,center_x,center_y)   # point4 after rotation


        pts=np.array([[result[0], result[1]], [result2[0], result2[1]], [result3[0], result3[1]], [result4[0], result4[1]]], np.int32)

        yAxis = cv2.flip(img2, 1)
        img=(cv2.polylines(yAxis, [pts], True, (0, 0, 255), 5))  # generate box according to the 4 points(pts)

        img=cv2.flip(img,1)
        
        output_path='saving'                  #saving directory
        cv2.imwrite(output_path+'/image_box'+'.jpeg', img)
    else:
        pass

#bx=150
#by=150
#ba=80
#bs=1.5
#Pc=1
#generate_box(Pc,bx,by,ba,bs)
    
