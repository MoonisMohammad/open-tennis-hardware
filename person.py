import cv2
import imutils 
import numpy as np
from imutils.object_detection import non_max_suppression
from matplotlib import pyplot as plt
# Malisiewicz et al.


def iou(a, b):  # returns None if rectangles don't intersect
    #print(a[0],a[1],a[2],a[3],b[0],b[1],b[2],b[3])
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




def detectperson(image,stride, padding, scale):
    # Initializing the HOG person 
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
       
    # Reading the Image 
    image = cv2.imread(image)
    #image = cv2.imread('Snapchat-850053629.jpg')
    #image = cv2.imread(image)
    #image = cv2.imread('download.jpg')
    #dim = (960,1280)
    # image = imutils.resize(image,width=960,height=1280)
    #image = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
    #image = crop(image) #winStride=(2,2), padding=(4,4), scale=1.1
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects, weights = hog.detectMultiScale(img_gray, winStride= stride, padding= padding, scale= scale)
    #print("rects: ", type(rects))
    newrects = non_max_suppression(rects,overlapThresh=0.3)
    #print(type(newrects))
    removed = np.array([])
    for i in range(len(newrects)):
        for j in range(i+1,len(newrects)):
            rect1 = newrects[i]
            rect2 = newrects[j]
            #print('rect1,rect2 ',rect1,rect2)
            ioucalculated,boxaarea,boxbarea = iou(rect1,rect2)
            if ioucalculated >= 0.8:
                if boxbarea > boxaarea:
                    newrects = np.delete(newrects,(1,j),axis = 0)
                    #np.append(removed,newrects[i])
                else:
                    newrects = np.delete(newrects,(1,i),axis = 0)
                    #np.append(removed,newrects[i])
    #print('removed is ', removed)
    for i, (x, y, w, h) in enumerate(newrects):
        #print(i)
        if weights[i]< 0.3:#or weights[i] > 1.0:
            continue
        else:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2) #red rectangles 
            cv2.putText(image, str(np.round(weights[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #print(newrects[i])
        #elif weights[i] < 0.3 and weights[i] > 0.13:
        #    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #   cv2.putText(image, str(np.round(weights[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #   print("confidence interval: ", str(np.round(weights[i],2)))
        #if weights[i] < 0.7 and weights[i] >0.5:
        #    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #    cv2.putText(image, str(np.round(weights[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #result = non_max_suppression(rects, probs=None, overlapThresh=0.3)
         #   print("confidence interval: ", str(np.round(weights[i],2)))
        #if weights[i] > 0.7: #and weights[i] <= 1.0:
        #    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #    cv2.putText(image, str(np.round(weights[i],2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # = non_max_suppression(rects, probs=None, overlapThresh=0.3)
            #print("confidence interval: ", str(np.round(weights[i],2)))
    #result = non_max_suppression(rects, probs=None, overlapThresh=0.3)
        # getting no. of human detected
    print('Human Detected : ', newrects,len(newrects))
    
    #print('Human Detected after checking overlap: ', newrects,len(newrects))      
    #print("acc: ", str(np.round(weights[i].flatten(),2)))
    #cv2.putText(image, str(weights[i]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    #cv2.putText(image, str(weights[i]), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 122, 255), 2)
    #cv2.putText(image, str(weights[i]), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.imshow('HOG detection', image)
        #cv2.imwrite(f"../outputs/{image_name}", image)
    cv2.imwrite("out5.jpg", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return newrects
if __name__=="__main__":
    detectperson('playingr306.jpg')