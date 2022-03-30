import pandas as pd
import numpy as np
import cv2
#from persondetection_dnn import *
from playerdetection import *
from person import *
import ast
import json
initialimage = " "
initial = False
totaliou=[]
import csv


#write to csv file
def writecsv(confidence,iou,precision,recall,playeriou,playerprec,playerrec):
    data = []
    #header =['confidence','iou','precision','recall','playeriou','playerprecision','playerrecall']
    f = open('test_result_hog.csv', 'a')
    data.append(confidence)
    data.append(iou)
    data.append(precision)
    data.append(recall)
    data.append(playeriou)
    data.append(playerprec)
    data.append(playerrec)
    writer = csv.writer(f)
    writer.writerow(data)
#read annotated json file to form tennis court polygons 
def gettenniscourt(imagename):
    t = 0
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
    #'tennistest.json'
    f = open('tennistest_updated.json')
    data = json.load(f)
    x_coord = data[imagename]['regions']['0']['shape_attributes']['all_points_x']
    y_coord = data[imagename]['regions']['0']['shape_attributes']['all_points_y']
    
    #checks if there are more than 1 polygon
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
            #print("ap,pp",annotatedplayers,predplayers)
            if(predplayers != []):
                if(annotatedplayers != []):
                    iou,precision,recall = ioumany(annotatedplayers,predplayers)
                    playeriou.append(iou)
                    playerprecision.append(precision)
                    playerrecall.append(recall)
            else:
                continue
    if len(playeriou) == 0:
        #print("i,p,r using formula", 0, prec, rec)
        return 0,0,0
            
    avgiou = sum(playeriou)/len(playeriou)
    avgprecision = sum(playerprecision)/len(playerprecision)
    avgrecall = sum(playerrecall)/len(playerrecall)
    
    return avgiou,avgprecision,avgrecall
    
            
            
#calculates the iou
def ioumany(imageboxes, predboxes):
    temp =[]
    
    #returnlist =[]
#     tp= 0
#     fn = 0
#     fp = 0
#     precision = 0
#     recall = 0
    #fp = 0
    imageboxmatch = []
    predboxmatch = []
    
    #precision = True positive/total persons predicted
    #recall = True positive/ total persons expected from annotations
    #True positive is when iou > 0.45
    #iouval = -1
       #a is imageboxes
    print("img boxes", imageboxes)
    print("pred boxes", predboxes)
    # returns None if rectangles don't intersect
  #initialimage = getinitialimage(
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
        
        for a in imageboxes:
            for b in predboxes:
            
                #checking if expected bounding boxes is none and predicted is none, iou,prec,rec = 1 else 0
                #print("len a", len(a))
                #print("len b", len(b))
        
                print("a",a)
                print("b",b)            
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
                    temp.append(iou)
                    #tp += 1
                    #fp += 0
                    imageboxmatch.append(a)
                    predboxmatch.append(b)
                #if iou > 0.6:
                    #iou_dnn = iou
                else:
                    #tp += 0
                    #fp += 1
                    continue
                

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

            #precision = tp/len(predboxes)
            #recall = tp/len(imageboxes)
            #print("tp", tp)
            #print("tpp", tp)
                    
            if len(temp) == 0:
                #print("i,p,r using formula", 0, prec, rec)
                print("i,p,r", 0, precision, recall)
                print("____________________________________")
                return 0,precision,recall
                
      
        
                
            avgiou = sum(temp)/len(temp)
            #returnlist.append(avgiou)
            #returnlist.append(precision)
            
            
            #tp = 0
                    #else:
                    #    iouval = sum(temp)/len(temp)
                       
                    #totaliou.append(iou)
                        #print("iou", iou)  
            #avg_iou_dnn= sum(totaliou)/len(totaliou)
            #print("iou", avg_iou_dnn)
            #print("temp", temp)
            print("i,p,r", avgiou, precision, recall)
            #print("i,p,r using formula", avgiou, prec, rec)
            print("____________________________________")
            #return avgiou,precision #,recall
            return avgiou,precision,recall
            #break
    
    #imgperson.clear()
    #totaliou.clear()
#return totaliou
  #return interArea / (boxAArea + boxBArea - interArea)

def annotated(filename,stride, padding, scale):
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
        #print("imgbox", imagebox)
        #print("as",ast.literal_eval(imagebox))
        print("imgname", imagename)
        #print("imgb", ast.literal_eval(imagebox))
        #print("t",type(imagebox))
        #personboxes = testdetectperson(imagename,confidence)
        
        #using hog
        #update the path
        newpath = "C:\Users\chhav\OneDrive\Documents\WINTER 2022\4th year project\Project_codes\Images_sorted_updated/" + imagename
        personboxes= detectperson(newpath,stride, padding, scale)
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
        #print("RL",returnedlist)
        #iou = returnedlist[0]
        #prec = returnedlist[1]
        #print("i,p,r",iou, prec, rec)
        totalimageiou.append(iou)
        precision.append(prec)
        recall.append(rec)

        
        
    averageiou = sum(totalimageiou)/len(totalimageiou)
    averageprecision = sum(precision)/len(precision)
    averagerecall = sum(recall)/len(recall)
    avgplayeriou = sum(playeriou)/len(playeriou)
    avgplayerprecision = sum(playerprecision)/len(playerprecision)
    avgplayerrecall = sum(playerrecall)/len(playerrecall)
    
    #print("total", totalimageiou)
    print("average iou for person detection using dnn: ", averageiou)
    print("average precision: ", averageprecision)
    print("average recall: ", averagerecall)
    print("average player iou:", avgplayeriou)
    print("average player precision: ", avgplayerprecision)
    print("average player recall: ", avgplayerrecall)
    writecsv(scale,averageiou,averageprecision,averagerecall,avgplayeriou,avgplayerprecision,avgplayerrecall)
#     annotateddata = pd.read_csv(filename)
#     #print(annotateddata.columns)
#     imagebox = [] #bounding box of an image
#     #imagebox2 = []
#     #multipleimagebox = []
#     totalimageiou=[]    
#     #imagenames = annotateddata["imgname"]
#     #print(imagenames.head)
#     #imagebox = annotateddata[["x","y","w","h"]]
#     #print(imagebox.head)
#     for i in range(annotateddata.shape[0]): #shape[0] gives the total number of rows in the file
#         
#         imagebox.clear()
#         
#         data = annotateddata.iloc[i]
#         #done = False
#         imagename = data["imgname"]
#         imagebox.append(data["x"])
#         imagebox.append(data["y"])
#         imagebox.append(data["w"])
#         imagebox.append(data["h"])
#         
#         personboxes = testdetectperson(imagename) #boxes retuned from dnn
#         #personboxes = [648,416,36,80]
#         #print("type",type(personboxes))
#         #print("pbox",personboxes)
#         #print("size", annotateddata.shape[0]-1)
#         if (i < annotateddata.shape[0]):
#             totalimageiou.append(ioumany(imagebox,personboxes))
#             
#         averageiou = sum(totalimageiou)/len(totalimageiou)
#         print("total", totalimageiou)
#         print("average iou for person detection using dnn: ", averageiou)
    
def readannotated(filename):#"annotation_piimages.csv"
   
    annotateddata = pd.read_csv(filename)
    #print(annotateddata.columns)
    imagebox = [] #bounding box of an image
    imagebox2 = []
    multipleimagebox = []
    totalimageiou=[]    
    #imagenames = annotateddata["imgname"]
    #print(imagenames.head)
    #imagebox = annotateddata[["x","y","w","h"]]
    #print(imagebox.head)
    for i in range(annotateddata.shape[0]): #shape[0] gives the total number of rows in the file
        
        imagebox.clear()
        imagebox2.clear()
        data = annotateddata.iloc[i]
        #done = False
        imagename = data["imgname"]
        imagebox.append(data["x"])
        imagebox.append(data["y"])
        imagebox.append(data["w"])
        imagebox.append(data["h"])
        
        personboxes = testdetectperson(imagename) #boxes retuned from dnn
        #personboxes = [648,416,36,80]
        print("type",type(personboxes))
        print("pbox",personboxes)
        print("size", annotateddata.shape[0]-1)
        if (i < annotateddata.shape[0]):
            if(i == annotateddata.shape[0]-1):
                totalimageiou.append(ioumany([imagebox],personboxes))
                averageiou = sum(totalimageiou)/len(totalimageiou)
                print("total", totalimageiou)
                print("average iou for person detection using dnn: ", averageiou)
            else:          
                nextdata = annotateddata.iloc[i+1]
                nextimagename = nextdata["imgname"]
                #print("nxtimgname", nextimagename)
               
               # data[["x","y","w","h"]] #boxes returned from image in csv file
                print("___________________________________") 
                print("imgname", imagename)
                print("nxtimgname", nextimagename)
                print("imgbox", imagebox)
                
                if(imagename == nextimagename):
                    data2 = annotateddata.iloc[i+1]          
                    imagebox2.append(data2["x"])
                    imagebox2.append(data2["y"])
                    imagebox2.append(data2["w"])
                    imagebox2.append(data2["h"])
                    
                    same= True
                    print("s", same)
                    #if the current image and next image are same, build an array of the bounding boxes 
                    multipleimagebox.append(imagebox)
                    multipleimagebox.append(imagebox2)
                    print("morebox", multipleimagebox)
#                     if(i <= annotateddata.shape[0]-2):
#                         nextdata2 = annotateddata.iloc[i+2]
#                         nextimagename2 = nextdata2["imgname"]
#                         if(imagename == nextimagename2):
#                             same = True
#                             print("ss", same)
#                             continue
#                         else:
#                             same = False
#                             print("ss", same)
#                             totalimageiou.append(ioumany(multipleimagebox,personboxes))
#                             print("total1", totalimageiou)
                            #multipleimagebox.clear()
                    #else:
                    #    continue
                    #iou(True,imagebox,personboxes)
                else:
                    same = False                    
                    #multipleimagebox.append(imagebox)          
                    totalimageiou.append(ioumany([imagebox],personboxes))
                    print("total2", totalimageiou)
                    multipleimagebox.clear()
                
        
            

        
       
        #print([imagebox])
        #total_iou.append(iou(imagename,imagebox,personboxes))
    #avg_iou_dnn= np.mean(total_iou)
    #print("Average iou for deep Learning is: ", avg_iou_dnn)
        
def initialimage(imagename):
    initialimage = imagename 
def getinitialimage():
    if initialimage != " ":
        return imagename
def testdetectperson(imagename,confidence):
    path = "/home/pi/Project_codes/Images_sorted_updated/"
    newpath = path + imagename
    #print(newpath)
    personboxes_dnn = detectpersondnn(newpath,confidence)
    #print("t",type(personboxes_dnn))
    #print("tp",personboxes_dnn)
    return personboxes_dnn
    ##"[[644,415,50,91]]",210middle00001.jpg
if __name__=="__main__":
    #readannotated("annotation_piimages2.csv")
    #"annotation_piimages1.csv" #"annotation_updated.csv"
    stride = (2,2)
    padding = (4,4)
    #conf = [0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.60] #0.45, 0.5,0.51,0.52,0.61,0.62,0.63,0.5,0.65,
    #conf = [0.71,0.72,0.72,0.73,0.74,0.75,0.8,0.81,0.82,0.83,0.85,0.87,0.9,1.0]
    #scale
    scale = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,3,3.5,4]
    for c in scale:
        print("c",c)
        #annotated(filename,stride, padding, scale)
        annotated("annotation_updated.csv",stride,padding,c)
    #annotated("a3.csv")
    #img = cv2.imread("/home/pi/Project_codes/Images_sorted/2court013.jpg")
    #cv2.imshow('test', img)
#   average iou for person detection using dnn:  0.5927923519988099

