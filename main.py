import cv2
import cvzone
from matplotlib import scale
import numpy as np
import pickle

cap = cv2.VideoCapture('carPark.mp4')
width,height = 107 , 40
with open('CarParkPos' , 'rb')as f:
    posList = pickle.load(f)

def checkParkingspace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
        imgcrop = imgPro[y:y+height , x:x+width]
        #cv2.imshow(str(x*y),imgcrop)
        count = cv2.countNonZero(imgcrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3) , scale=1,thickness=2,offset=0)

        if count<900:
            color = (7, 252, 3)
            thic = 4
            spaceCounter+=1
        else:
            color = (0, 0, 200)
            thic =2
        
        cv2.rectangle(img, pos ,(pos[0]+width,pos[1]+height) , color ,thic)
    cvzone.putTextRect(img,f'Free:{spaceCounter}/{len(posList)}',(100,50) , scale=3,thickness=3,offset=20,colorR=(0,200,2))

while True:
    sucess , img = cap.read()
    
    #To repeate the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
    #Filtering the video
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray , (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur ,225, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,25,16)
    imgMeidan = cv2.medianBlur(imgThreshold , 5)
    kernal = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMeidan , kernel=kernal,iterations=1 )

    checkParkingspace(imgDilate)
        


    cv2.imshow("Image" , img)
    #cv2.imshow("ImageBlue" , imgBlur)
    #cv2.imshow("ImageThreshold" , imgThreshold)
    #cv2.imshow("ImgMedian" , imgMeidan)
    #cv2.imshow("ImgDilate" , imgDilate)
    cv2.waitKey(1)