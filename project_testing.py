#Chhavi Sujeebun, updated
#imporint required libraries and methods from other python scripts 
import pandas as pd
import numpy as np
import cv2
from persondetection_dnn import *
from playerdetection import *
from persondetection_hog import *
import ast
import json
import csv
#stores iou for each image 
totaliou=[]



#write to csv file for testing purposes
#@param confidence is the confidence theshold used in the object detection model
#@param iou is the iou calculated for persons in the dataset
#@param precision is the precision calculated for persons inthe dataset
#@recall is the recall calculated for persons in the dataset
#@playeriou is the iou calculated for players in the dataset
#@playerprec is the precision calculated for players in the dataset
#@playerrec is the precision calculated for players inthe dataset
def writecsv(confidence,iou,precision,recall,playeriou,playerprec,playerrec):
    data = []
    
    f = open('test_result.csv', 'a')
    data.append(confidence)
    data.append(iou)
    data.append(precision)
    data.append(recall)
    data.append(playeriou)
    data.append(playerprec)
    data.append(playerrec)
    writer = csv.writer(f)
    writer.writerow(data)
    
#read annotated json file to retrieve tennis court reference points and form tennis court polygons
#@param imagename is the imagename for which tennis court reference points must be read
#@return arrays containg the xy coordinates of each tennis court 
def gettenniscourt(imagename):
    t = 0
    #stores x,y coordinates of tennis courts 
    x_coord = []
    y_coord = []
    x1_coord = []
    y1_coord = []
    xy_coord = []
    xy1_coord = []
    xy2_coord = []
    xy3_coord = []
    x2_coord = []
    y2_coord = []
    x3_coord = []
    y3_coord = []
    
    #opening json file
    #reads the x and y coordinates for each tennis court
    f = open('tennistest_updated.json')
    data = json.load(f)
    x_coord = data[imagename]['regions']['0']['shape_attributes']['all_points_x']
    y_coord = data[imagename]['regions']['0']['shape_attributes']['all_points_y']
    
    #checks if there are more than 1 tennis court in the image and attempts to read them if they exist
    try:
        x_1coord = data[imagename]['regions']['1']['shape_attributes']['all_points_x']
        y_1coord = data[imagename]['regions']['1']['shape_attributes']['all_points_y']
    except:
        x_1coord = []
        y_1coord = []
        
    try:
        x_2coord = data[imagename]['regions']['2']['shape_attributes']['all_points_x']
        y_2coord = data[imagename]['regions']['2']['shape_attributes']['all_points_y']
    except:
        x_2coord = []
        y_2coord = []
    try:
        x_3coord = data[imagename]['regions']['3']['shape_attributes']['all_points_x']
        y_3coord = data[imagename]['regions']['3']['shape_attributes']['all_points_y']
    except:
        x_3coord = []
        y_3coord = []
        
    #stores the coordinates as an array of tuples 
    if(len(x_coord)!= 0):
        for i in range(len(x_coord)):
            xy_coord.append((x_coord[i],y_coord[i]))
            
    elif(len(x1_coord) != 0):
        for i in range(len(x1_coord)):
            xy1_coord.append((x1_coord[i],y1_coord[i]))
            
    elif(len(x2_coord) != 0):
        for i in range(len(x2_coord)):
            xy2_coord.append((x2_coord[i],y2_coord[i]))
            
    elif(len(x3_coord) != 0):
        for i in range(len(x3_coord)):
            xy3_coord.append((x3_coord[i],y3_coord[i]))

    return xy_coord, xy1_coord, xy2_coord, xy3_coord

#testing for players detected by calculating the iou, precision and recall
#@param imagename is the image being processed
#@param imageboxes is the array of annotated ground truth bounding boxes read from csv file
#@param predboxes is the array of predicted bounding boxes from the object detction models
#@rteurn average iou, precision and recall for players in each image 
def playertest(imagename,imageboxes,predboxes):
    annotatedplayers = []
    predplayers =[]
    court1 = []
    court2 = []
    court3 = []
    court0 =[]
    courts =[]
    playeriou = []
    playerprecision = []
    playerrecall= []
 
    court0,court1,court2,court3 = gettenniscourt(imagename) #obtaining tennis court for each image 
    courts.append(court0)
    courts.append(court1)
    courts.append(court2)
    courts.append(court3)
    #get player boxes for annotated boxes
    for c in courts:
        if len(c) != 0:            
            annotatedplayers = detectannotatedplayer(c,imageboxes)  
            #get player boxes for predicted boxes 
            predplayers = detectannotatedplayer(c,predboxes)
            
            #calculates the iou,precision,recall using ground truth and predicted player boxes
            if(predplayers != []):
                if(annotatedplayers != []):
                    iou,precision,recall = ioumany(annotatedplayers,predplayers)
                    playeriou.append(iou)
                    playerprecision.append(precision)
                    playerrecall.append(recall)
            else:
                continue
    if len(playeriou) == 0:
        return 0,0,0
           
    #calculates the average iou, precision and recall
    avgiou = sum(playeriou)/len(playeriou)
    avgprecision = sum(playerprecision)/len(playerprecision)
    avgrecall = sum(playerrecall)/len(playerrecall)
    
    return avgiou,avgprecision,avgrecall
    
            
            
#calculates the iou for ground truth and predicted bounding boxes
#@param imageboxes is an array of ground truth boxes
#@param predboxes is an array of predicted boxes from the model
#@return the average iou, precision and recall
def ioumany(imageboxes, predboxes):
    temp =[]
    imageboxmatch = []
    predboxmatch = []
    
    #precision = True positive/total persons predicted
    #recall = True positive/ total persons expected from annotations
    #True positive is when iou > 0.45
    
#returns None if rectangles don't intersect

    if len(imageboxes) == 0 and len(predboxes) == 0:
        print("i,p,r", 1,1,1)
        return 1,1,1
        #break
    elif len(imageboxes) == 0 and len(predboxes) != 0:
        print("i,p,r", 0,0,0)
        return 0,0,0
        #break
    elif len(imageboxes) != 0 and len(predboxes) == 0:
        print("i,p,r", 0,0,0)
        return 0,0,0
        #break
    else:
        #loops through the arrays and calculates the iou for each pair of boxes, only selects iou >= 0.45
        for a in imageboxes:
            for b in predboxes:
        
                #print("a",a)
                #print("b",b)            
                #print("a 0....3",a[0],a[1],a[2],a[3])
                #print("b 0....3",b[0],b[1],b[2],b[3])
                dx = min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
                dy = min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1])
                if (dx>=0) and (dy>=0):
                    interArea = dx*dy
                else:
                    interArea = 0
                    
                boxAArea = a[2]*a[3]
                boxBArea = b[2]*b[3]
                iou = interArea / (boxAArea + boxBArea - interArea)
                print("iou", iou)
                if iou >= 0.45:
                    temp.append(iou) #temp stores the iou of detections in the image 
                    imageboxmatch.append(a) #imageboxmatch stores the ground truth box 
                    predboxmatch.append(b) #predboxmatch stores the pred box
                else:
                    continue
                
        #the True positive, False positive and False negative are computed as shown below and
        #are further used to calculate the precision and recall
        tp = len(imageboxmatch)
        print("tp",tp)
        if tp == 0:
            return 0,0,0
        else:
            fn = len(imageboxes)-len(imageboxmatch)
            print("fn",fn)
            fp = len(predboxes) - len(predboxmatch)
            print("fp",fp)
            precision = tp/(tp+fp)
            recall = tp/(tp+fn)

                    
            if len(temp) == 0: #no overlap >=0.45 with the ground truth and predicted boxes
                
                print("i,p,r", 0, precision, recall)
                print("____________________________________")
                return 0,precision,recall
                
      
        
                
            avgiou = sum(temp)/len(temp)
            print("i,p,r", avgiou, precision, recall)
            
            print("____________________________________")
            
            return avgiou,precision,recall

#@param filename is the csv file containing annotated grounf truth boxes 
#@param confidence is the confidence threshold for the Mobilenet SSD object detection model
#ground truth boxes are read from csv file and predicted boxes are generated by calllig the model
#iou, precision and recall is calculated for the dataset using the abopve methods 
def annotated(filename,confidence):
    totalimageiou=[]
    precision = []
    recall = []
    returnedlist = []
    playeriou = []
    playerprecision= []
    playerrecall = []
    annotateddata = pd.read_csv(filename)
    for i in range(annotateddata.shape[0]):
        data = annotateddata.iloc[i]
        imagename = data["imgname"]
        imagebox = data["persons"]
        print("imgname", imagename)
        
        #testing is done using both MobilenetSSD and HOG 
        personboxes = testdetectperson(imagename,confidence)
        
        #using hog
        #newpath = "/home/pi/Project_codes/Images_sorted_updated/" + imagename
        #= detectperson(newpath,stride, padding, scale)
        #print("persons detected",personboxes)
        
        #calculating iou for person boxes
        
        iou,prec,rec = ioumany(ast.literal_eval(imagebox),personboxes)
        print("iou person",iou,prec,rec)
        
        #player test for each image
        
        player_iou,playerprec,playerrec = playertest(imagename,ast.literal_eval(imagebox),personboxes)
        print("iou player",player_iou,playerprec,playerrec)
        playeriou.append(player_iou)
        playerprecision.append(playerprec)
        playerrecall.append(playerrec)

        totalimageiou.append(iou)
        precision.append(prec)
        recall.append(rec)

        
    #the average iou,precision and recall is calculated for persons and palyers detected in the dataset
    averageiou = sum(totalimageiou)/len(totalimageiou)
    averageprecision = sum(precision)/len(precision)
    averagerecall = sum(recall)/len(recall)
    avgplayeriou = sum(playeriou)/len(playeriou)
    avgplayerprecision = sum(playerprecision)/len(playerprecision)
    avgplayerrecall = sum(playerrecall)/len(playerrecall)
    
    
    print("average iou for person detection using dnn: ", averageiou)
    print("average precision: ", averageprecision)
    print("average recall: ", averagerecall)
    print("average player iou:", avgplayeriou)
    print("average player precision: ", avgplayerprecision)
    print("average player recall: ", avgplayerrecall)
    #writes the data in s csv file
    writecsv(confidence,averageiou,averageprecision,averagerecall,avgplayeriou,avgplayerprecision,avgplayerrecall)

#@param imagename is the imagename to be processed
#@param confidence is the confidence threshold
#calls the Mobilenet SSD model to peform object detection on specific images
#@return the bounding boxes of persons detected using Mobilenet SSD
def testdetectperson(imagename,confidence):
    path = "/home/pi/Project_codes/Images_sorted_updated/"
    newpath = path + imagename    
    personboxes_dnn = detectpersondnn(newpath,confidence)
    return personboxes_dnn

#main code to run annotated method for different parameters
if __name__=="__main__":
    
    #stride = (2,2)
    #padding = (4,4)
    #conf = [0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.60] #0.45, 0.5,0.51,0.52,0.61,0.62,0.63,0.5,0.65,
    #conf = [0.71,0.72,0.72,0.73,0.74,0.75,0.8,0.81,0.82,0.83,0.85,0.87,0.9,1.0]
    conf = [0.1,0.2,0.3]
    #scale = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,3,3.5,4]
    for c in conf:
        print("c",c)
        #annotated(filename,stride, padding, scale)
        annotated("annotation_updated.csv",c)
   

