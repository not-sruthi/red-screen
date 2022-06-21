from os import access
import cv2
import time
import numpy as np

#save output in file

format = cv2.VideoWriter_fourcc(*'XVID')

outputFile = cv2.VideoWriter('output.avi', format, 20.0, (640,480))


#starting webcam

start = cv2.VideoCapture(0)
#warmup cam
time.sleep(2)
#capturing bg frame
bg = 0
#running for 60 
for i in range(60):
    ret, bg = start.read()
#invert image
bg = np.flip(bg, axis = 1)


#read frames while cam is open
while (start.isOpened()):
    #is open? ret = boolean value
    ret,img = start.read()

    if not ret:
        break

    #invert image for consistency
    img = np.flip(img, axis = 1)

    #converting colour from bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #check for reds (within certain range)
    lower_red =  np.array([0,120,50])
    upper_red =  np.array([10,255,255])

    #create mask 1 
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    #create mask 2
    lower_red =  np.array([170,120,70])
    upper_red =  np.array([180,255,255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2
    
    #open and expand image where mask 1

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    #not red bits
    mask2 = cv2.bitwise_not(mask1)

    #replacing red with bg image
    res1 = cv2.bitwise_and(img,img,mask=mask2)
    res2 = cv2.bitwise_and(bg,bg,mask=mask1)

    #merging both resolutions
    merge = cv2.addWeighted(res1,1, res2,1, 0)
    
    outputFile.write(merge)

    #displaying output to user

    cv2.imshow('Magic', merge)
    cv2.waitKey(1)

start.release()

cv2.destroyAllWindows()