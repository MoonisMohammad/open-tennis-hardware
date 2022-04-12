#@author Chhavi Sujeebun updated
#importing the required libraries 
import cv2
import argparse
import numpy as np

#stores the image being processed
getimage = ' '

#stores the reference points selected ion the image 
arrpt=[]

#This method displays the image and records the coordinate of any mouse click in an array
#the mouse clicks are the reference points chosen
#@param image - is the image to be processed
def ref(image):
    def click_event(event, x, y, flags, params):
         
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
     
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
            
            #allow upto 9 reference points to be selected
            if(len(arrpt) < 9):
                arrpt.append((x,y))
            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(x) + ',' +
                        str(y), (x,y), font,
                        0.5, (255, 0, 0), 2)
            cv2.circle(img, (x, y), 6, (0, 255, 255), -1)
            cv2.imshow('mimage', img)
     
        # checking for right mouse clicks    
        if event==cv2.EVENT_RBUTTONDOWN:
     
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
                        

            # displaying the coordinates
            # on the image window      
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL 
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            cv2.putText(img, str(b) + ',' +
                        str(g) + ',' + str(r),
                        (x,y), font, 5,
                        (255, 255, 0), 2)
            cv2.imshow('mimage', img)
     
    # driver function
    
     
    # reading the image sent as parameter 
        
    img = cv2.imread(image,1)
    getimage = img
    #shows the image so that user can click on the image to select reference points 
    cv2.imshow('mimage', img)
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('mimage', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()

#@returns an array containing the reference points selected 
def getpts():
    
    return arrpt
#clears the array arrpt after the points have been selected and saved to the database
def resetarr():
    arrpt.clear()
    