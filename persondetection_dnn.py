
import cv2
#thres = 0.45 # Threshold to detect object
def detectpersondnn(image,confidence):
    #cap = cv2.VideoCapture(1)
    img =cv2.imread(image) #391
    personbox = []
    # cap.set(3,1280)
    # cap.set(4,720)
    # cap.set(10,70)
     
    classNames= []
    classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
    with open(classFile,"rt") as f:
        classNames = f.read().rstrip('\n').split('\n')
     
    configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"
     
    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(1280,720)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
     
    #while True:
    #success,img = cap.read()
    #img = cv2.imread('playingr306.jpg')
    classIds, confs, bbox = net.detect(img,confThreshold=confidence) #0.56
    #     for classId1 in classIds.flatten():
    #         if(classId1 == 1):
    #             print(classId1,bbox)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            #for classId1 in classIds.flatten():
            if(classId == 1 and confidence >0.55):
                #print("box",list(box))
                personbox.append(list(box))
                #print(classId,box)
                #print(classNames[classId-1])
                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0],box[1]),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    #cv2.imshow('Output',img)
    #cv2.imwrite("outcoconew.jpg", img)
    #cv2.waitKey(1)
    #print("pb",list(personbox))
    return personbox 

#if __name__=="__main__":
#    x = detectpersondnn("/home/pi/Project_codes/Images_sorted/210top100001.jpg")
#    print(x)