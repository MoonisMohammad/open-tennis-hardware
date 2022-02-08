import cv2
import argparse
import matplotlib.pyplot as plt
import numpy as np
# function to display the coordinates of
# of the points clicked on the image
arrpt = []
newarrpt =[]
def ref():
    def click_event(event, x, y, flags, params):
         
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
     
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
            
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
    #         font = cv2.FONT_HERSHEY_SIMPLEX
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
    
     
    # reading the image
    img = cv2.imread('playingr337.jpg',1)
    #plt_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #imgplot = plt.imshow(img)
    #dim =  (img.shape[1],img.shape[0]) #w,h
    #resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # displaying the image
    #>1024 take 14% else take 30%
    #scale_percent = 14 # percent of original size
    #width = int(img.shape[1] * scale_percent / 100)
    #height = int(img.shape[0] * scale_percent / 100)
    #dim = (width, height)
    #resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    #cv2.imshow('image', resized)
    #cv2.imwrite('resized.png', resized)
    #image = cv2.imread('resized.png',1)
    cv2.imshow('mimage', img)
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('mimage', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()
#creates a numpy array using dimension provided
# if max court = 2, a 2d array will be created
#def setpts(maxcourt):
#    newarrpt = np.reshape(arrpt, (maxcourt, 4))
def getpts():
    print(arrpt)
    return arrpt