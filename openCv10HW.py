import cv2
import numpy as np

#defining All the TrackBars ( 1-6 )
def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low: ',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High: ',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low: ',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High: ',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low: ',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High: ',valHigh)

width=640
height=360

#configure and initialize the webcam for video capture using OpenCV
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


cv2.namedWindow('my Tracker')
cv2.moveWindow('my Tracker',width,0)

#initializing the variables
hueLow=10
hueHigh=20
satLow=10
satHigh=250
valLow=10
valHigh=250

#create the 6 TrackBars
cv2.createTrackbar('Hue Low','my Tracker',10,179,onTrack1)
cv2.createTrackbar('Hue High','my Tracker',20,179,onTrack2)
cv2.createTrackbar('Sat Low','my Tracker',10,255,onTrack3)
cv2.createTrackbar('Sat High','my Tracker',250,255,onTrack4)
cv2.createTrackbar('Val Low','my Tracker',10,255,onTrack5)
cv2.createTrackbar('Val High','my Tracker',250,255,onTrack6)


while True:
    ignore, frame = cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #create arrays for define the lower & upper bounds of HSV Color range
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    
    #only the parts of the frame where the myMask is white (255) will be kept. All other parts of the frame will be set to black (0)
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound) #create mask
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    myObject=cv2.bitwise_and(frame,frame,mask=myMask) 
    
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2))) 

    #Retrives only the extreme outer contours
    #Compress Horizontal, Verticle and Diagonal segments and leave only their end point
    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        #calculate the area of contour 
        area=cv2.contourArea(contour)
        if area>=200:
            myContours=[contour]

            #(x,y)=top left corner cordinates rectangle
            #(w,h)=width and height of bounding rectangle
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                          
    cv2.imshow('My Object Window',myObjectSmall)
    cv2.moveWindow('My Object Window',int(width/2),int(height))

    cv2.imshow('my Mask',myMaskSmall)
    cv2.moveWindow('my Mask',0,height)
    frame=cv2.flip(frame,1)
    cv2.imshow('windName',frame)
    cv2.moveWindow('windName',0,0)

    if cv2.waitKey(1) & 0xff==ord('b'):
        break
cv2.destroyAllWindows()