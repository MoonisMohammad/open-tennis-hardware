#@Chhavi Sujeebun, updated
#importing the required libraries 
import cv2

#detectpersondnn makes use of the Mobilenet SSD object detection model to detect persons in an image using MS COCO dataset
#@param image is the image to be processed
#@param confidence is the confidence threshold at which or greater than which detections must be considered as a person
def detectpersondnn(image,confidence):
    #reads the image sent as parameter
    img =cv2.imread(image)
    #personbox stores an array of the bounding boxes of persons detected
    personbox = []
    #an array storing the classes that can be detected by the model, obtained by reading te coco file
    classNames= []
    classFile = "Object_Detection_Files/coco.names"
    with open(classFile,"rt") as f:
        classNames = f.read().rstrip('\n').split('\n') #reads the class names 
    
    #configuring the congifpath and weightpath 
    configPath = "Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    weightsPath = "Object_Detection_Files/frozen_inference_graph.pb"
    
    #Initializing the Detection model, setting the input size of images, the inpu scale and input mean
    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(1280,720)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    
    #classIds stores the classID that the predicted bounding box belongs to
    #confs stores the confidence of the prediction
    #bbox stores the bounding box of the prediction
    #confThreshold is set to the confidence sent as parameter, if the confidence of a bounding box is >= confThreshold,
    #that bounding box is considered as that of a person else it is rejected
    classIds, confs, bbox = net.detect(img,confThreshold=confidence) #0.56

    #The following code verifies the classId and confidence for each prediction
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            #classID 1 is that of a person, the classid and confidence is verified for each prediction
            #if the detection is that of a person and the confidence is > 0.55, then that prediction is accepted and
            #its boudning box is appended to the personbox array
            if(classId == 1 and confidence >0.55):
                
                personbox.append(list(box))
                #the following code is to draw the bounding box in the image along with the confidence threshold
                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0],box[1]),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    #cv2.imshow('Output',img)
    #cv2.imwrite("outcoconew.jpg", img)
    #cv2.waitKey(1)
    
    #returns a numpy array containing bounding boxes of persons detected in the image
    return personbox 

