#@author Chhavi Sujeebun updated
#importing required libraries 
import cv2
import imutils 
import numpy as np
from imutils.object_detection import non_max_suppression

#iou calculates the overlap between two bounding boxes 
def iou(a, b):  # returns None if rectangles don't intersect
    
    dx = min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
    dy = min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1])
    boxAArea = a[2]*a[3]
    boxBArea = b[2]*b[3]
    if (dx>=0) and (dy>=0):
        interArea = dx*dy
    else:
        interArea = 0
    iou = interArea / (boxAArea + boxBArea - interArea)
    return iou, boxAArea, boxBArea

#@return only the bounding boxes that were picked using the integer data type
def non_max_suppression_fast(boxes,weights,overlapThresh):
# if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
        # initialize the list of picked indexes	
        pick = []
        # grab the coordinates of the bounding boxes
        x1 = boxes[:,0]
        y1 = boxes[:,1]
        x2 = boxes[:,2]
        y2 = boxes[:,3]
        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)
        # keep looping while some indexes still remain in the indexes
        # list
        while len(idxs) > 0:
            # grab the last index in the indexes list and add the
            # index value to the list of picked indexes
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            # find the largest (x, y) coordinates for the start of
            # the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])
            # compute the width and height of the bounding box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            # compute the ratio of overlap
            overlap = (w * h) / area[idxs[:last]]
            print(overlap)
            # delete all indexes from the index list that have
            idxs = np.delete(idxs, np.concatenate(([last],
                np.where(overlap > overlapThresh)[0])))
        # return only the bounding boxes that were picked using the
        # integer data type
        return boxes[pick].astype("int")


#@param image is the image to be processed
#@param stride, padding, scale are the hyperparameters of the HOG Descriptor model that need to be tuned
#@return a numpy array containing the bounding boxes of persons detected in the processed image

def detectperson(image,stride, padding, scale):
    # Initializing the HOG descriptor
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
       
    # Reading the Image sent as parameter
    image = cv2.imread(image)
    #image is preprocessed by converting it to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #rects stores the array of bounding boxes of persons detected, weights is the confidence threshold 
    rects, weights = hog.detectMultiScale(img_gray, winStride= stride, padding= padding, scale= scale)
    #non max suppression removes duplicates and returns the final predictions which is stored in newrects 
    newrects = non_max_suppression(rects,overlapThresh=0.3)
    
    #The folowing code is attempting to detect overlaps between bounding boxes for the same person
    #we has cases where there was one good prediction and one overlap which was thrice the size of the good prediction box
    #if there is an overlap, the code rejects the box with a greater area and keeps the saller one for the same person
    for i in range(len(newrects)):
        for j in range(i+1,len(newrects)):
            rect1 = newrects[i]
            rect2 = newrects[j]
            
            ioucalculated,boxaarea,boxbarea = iou(rect1,rect2)
            if ioucalculated >= 0.8:
                if boxbarea > boxaarea:
                    newrects = np.delete(newrects,(1,j),axis = 0)
                    
                else:
                    newrects = np.delete(newrects,(1,i),axis = 0)
                    
    #newects stores an array of the bouding boxes of persons detected
    #each boundingbox stores data [x,y,w,h]
    #the code loops through the array of bounding boxesand draws the bouding box in an output image is the weight/ confidence threshold is greater than 0.3
    #the weight threshold can be modified
    for i, (x, y, w, h) in enumerate(newrects):
        #print(i)
        if weights[i]< 0.3:
            continue
        else:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image, str(np.round(weights[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
    #print('Human Detected : ', newrects,len(newrects))
    #draws the boudning boxes in the image and creates a new image using the specified name
    cv2.imwrite("out5.jpg", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #returns array of bounding boxes of persons
    return newrects
