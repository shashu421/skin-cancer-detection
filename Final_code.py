import numpy as np
import cv2
import webbrowser
import os

global r1
global g1
global b1
global r1p
global g1p
global b1p
global flag
global empty
global block

first_block_l=[70,30]
first_block_r=[190,150]
second_block_l=[260,30]
second_block_r=[380,150]
third_block_l=[450,30]
third_block_r=[570,150]
fourth_block_l=[70,180]
fourth_block_r=[190,300]
fifth_block_l=[260,180]
fifth_block_r=[380,300]
sixth_block_l=[450,180]
sixth_block_r=[570,300]
seventh_block_l=[70,330]
seventh_block_r=[190,450]
eighth_block_l=[260,330]
eighth_block_r=[380,450]
ninth_block_l=[450,330]
ninth_block_r=[570,450]

def nothing(x):
    pass
cap=cv2.VideoCapture(0)
cv2.ocl.setUseOpenCL(False)
cv2.namedWindow('test')
cv2.createTrackbar('R','test',0,255,nothing)
cv2.createTrackbar('G','test',0,255,nothing)
cv2.createTrackbar('B','test',0,255,nothing)
switch='0:OFF \n 1:ON'
cv2.createTrackbar(switch,'test',0,1,nothing)

fgbg=cv2.createBackgroundSubtractorMOG2()

main_gesture=[[0]]
gesture=[0]

empty=[]
empty1=[0]

while cv2.waitKey(1)!=103 and cap.isOpened:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    r=cv2.getTrackbarPos('R','test')
    g=cv2.getTrackbarPos('G','test')
    b=cv2.getTrackbarPos('B','test')
    s=cv2.getTrackbarPos(switch,'test')
    if s==0:
        lower=np.array([255,255,255])
        higher=np.array([255,255,255])
    else:
        lower=np.array([r,g,b])
        higher=np.array([255,255,255])

    mask=cv2.inRange(hsv,lower,higher)

    res=cv2.bitwise_and(frame,frame,mask=mask)

    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('test',res)
    
while cv2.waitKey(1)!=27:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)

    first=cv2.rectangle(frame,(first_block_l[0],first_block_l[1]),(first_block_r[0],first_block_r[1]),(0,0,255),1)
    second=cv2.rectangle(frame,(second_block_l[0],second_block_l[1]),(second_block_r[0],second_block_r[1]),(0,0,255),1)
    third=cv2.rectangle(frame,(third_block_l[0],third_block_l[1]),(third_block_r[0],third_block_r[1]),(0,0,255),1)
    fourth=cv2.rectangle(frame,(fourth_block_l[0],fourth_block_l[1]),(fourth_block_r[0],fourth_block_r[1]),(0,0,255),1)
    fifth=cv2.rectangle(frame,(fifth_block_l[0],fifth_block_l[1]),(fifth_block_r[0],fifth_block_r[1]),(0,0,255),1)
    sixth=cv2.rectangle(frame,(sixth_block_l[0],sixth_block_l[1]),(sixth_block_r[0],sixth_block_r[1]),(0,0,255),1)
    seventh=cv2.rectangle(frame,(seventh_block_l[0],seventh_block_l[1]),(seventh_block_r[0],seventh_block_r[1]),(0,0,255),1)
    eighth=cv2.rectangle(frame,(eighth_block_l[0],eighth_block_l[1]),(eighth_block_r[0],eighth_block_r[1]),(0,0,255),1)
    ninth=cv2.rectangle(frame,(ninth_block_l[0],ninth_block_l[1]),(ninth_block_r[0],ninth_block_r[1]),(0,0,255),1)
    
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower=np.array([r,g,b])
    higher=np.array([255,255,255])
    mask=cv2.inRange(hsv,lower,higher)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    
    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    fgmask=fgbg.apply(thresh)
    blur=cv2.GaussianBlur(fgmask,(5,5),0)
    img, contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #img=cv2.drawContours(frame, contours, -1,(0,0,255),1)

        

    for i in range(len(contours)):
        cnt=np.array(contours[i])
    nothing
    
    hull=cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)

    (x,y),radius=cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    rect=cv2.minAreaRect(cnt)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    final=cv2.circle(frame,center,radius,(0,255,0),2)
    final2=cv2.circle(frame,center,10,(255,0,0),2)
    final3=cv2.drawContours(frame,[box],0,(0,0,255),2)
    img = cv2.circle(img,center,radius,(255,0,0),2)


    if contours==empty:
        if gesture==empty1:
            pass
        else:
            main_gesture.append(gesture)
        gesture=[0]

    else:
        if first_block_l[0]<center[0]<first_block_r[0] and first_block_l[1]<center[1]<first_block_r[1]:
            block=1
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif second_block_l[0]<center[0]<second_block_r[0] and second_block_l[1]<center[1]<second_block_r[1]:
            block=2
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif third_block_l[0]<center[0]<third_block_r[0] and third_block_l[1]<center[1]<third_block_r[1]:
            block=3
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif fourth_block_l[0]<center[0]<fourth_block_r[0] and fourth_block_l[1]<center[1]<fourth_block_r[1]:
            block=4
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)
        elif fifth_block_l[0]<center[0]<fifth_block_r[0] and fifth_block_l[1]<center[1]<fifth_block_r[1]:
            block=5
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif sixth_block_l[0]<center[0]<sixth_block_r[0] and sixth_block_l[1]<center[1]<sixth_block_r[1]:
            block=6
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif seventh_block_l[0]<center[0]<seventh_block_r[0] and seventh_block_l[1]<center[1]<seventh_block_r[1]:
            block=7
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif eighth_block_l[0]<center[0]<eighth_block_r[0] and eighth_block_l[1]<center[1]<eighth_block_r[1]:
            block=8
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        elif ninth_block_l[0]<center[0]<ninth_block_r[0] and ninth_block_l[1]<center[1]<ninth_block_r[1]:
            block=9
            if gesture[len(gesture)-1] != block:
                    gesture.append(block)

        else:
            pass


    print(gesture)
    print(main_gesture)

    if main_gesture[len(main_gesture)-1]==[0,2,5,6,3]:
        img=cv2.imread('img.jpg')
        #webbrowser.open('https://www.google.co.in')
        os.startfile("notepad.exe")
        #cv2.imshow('result',img)
        #cv2.waitKey()
        break
        
    cv2.imshow('test',res)
    cv2.imshow('final',final)
    cv2.imshow('final',final2)
    cv2.imshow('final',final3)

    cv2.imshow('final',first)
    cv2.imshow('final',second)
    cv2.imshow('final',third)
    cv2.imshow('final',fourth)
    cv2.imshow('final',fifth)
    cv2.imshow('final',sixth)
    cv2.imshow('final',seventh)
    cv2.imshow('final',eighth)
    cv2.imshow('final',ninth)

    cv2.resizeWindow('final',640,480)
    
    
cap.release()    
cv2.destroyAllWindows()
