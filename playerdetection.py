#@chhavi sujeebun, updated
#importing required libraries and methods from other python scripts 
from persondetection_hog import *
import numpy as np
import cv2
from database import *
from shapely.geometry import Polygon, Point
from persondetection_dnn import *
from tenniscourt_gui import *
from ast import literal_eval
from upload import *

#stores reference points for tennis courts
courts_coord = []
authorizationId = "2OCC9876543210"    #use this auth Id its already registered in backend and is owned ny lyndwood manager and this device is named test data upload
static_ip = "52.229.94.153"               #ip address of server

#calculate midpoints of bottom line using bottom points of bounding boxes
#given x,y,w,h start point always at top left corner and end point at bottom right corner
#top left = x,y|top right = x+w,y|bottom left = x,y+h|bottom right = x+w,y+h
#@param bounding_boxes is the bounding boxes of detected persons 
#@returns a numpy array storing the midpoints
def calculatemidpoint(bounding_boxes):
    midpoints= []
    
    #returns null is no persons are detected
    if len(bounding_boxes) == 0:
        return []
    else:
        #calculates the mmispoint for each bounding box/person detected
        for i, (x, y, w, h) in enumerate(bounding_boxes):
            midpointx = ((2*x)+w)/2
            midpointy = y+h
            midpoints.append((midpointx,midpointy))

        return midpoints



#reads the tennis court coordinates from the database and uses shapely to verify if person is within the predefined tennis court region
#within the tennis court region, person is player and the playercount is updated and uploaded to the server
#else spectator and is ignored
def isplayer(midpoints,boxes):
    playerbox =[] #stores bounding boxes of players
    
    #reads the tennis court coordinates from the database
    cursor.execute("SELECT * from courtdb")
    record = cursor.fetchall()
    
    #loops though each tennis court coordinate to determine the persons are players on which court
    for row in record:
        if(midpoints == None): 
            playercount = 0
            break;
            
        print("____________________")

        playercount = 0
        #must check if it is empty or not 
        courtid = row[0]
        #courtarray stores the array of refernce points read from the database
        courtarray = literal_eval(row[1])
        #A polygon is formed using the tennis court reference points 
        polytenniscourt = Polygon(courtarray)
        
        #loops through the array of midpoints and verifies if the midpoint is within the polygon formed using tennis court points
        for i in range(len(midpoints)):
       
            #playerpoint is the midpoint converted as a point
            playerpoint= Point(midpoints[i])
            
            playerbool = polytenniscourt.contains(playerpoint) #true if midpoint is within tennis court polygon
            
            if (playerbool== True):
                #playercount is incremented and the bounding box is appended to playerbox
                playercount = playercount + 1
                playerbox.append(boxes[i])
            else:
                playercount = playercount + 0
                
        #prints the number of players on each court
        print("court id", courtid)
        print("players", playercount)
        
        #the following code is used to upload the playercount to the server
        #must be uncommented when the server is on else gives error
        #uploadData(referenceNumber,count,authorizationId,static_ip)
        #uploadData(courtid,playercount,authorizationId,static_ip)
       
#detectplayer using provided court coordinates and bouding boxes of players for testing, has same logic as above method
def testplayer(court,midpoints,boxes):
    playerbox =[]
        
    polytenniscourt = Polygon(court)

    if len(midpoints) == 0:
        return []
    else:
        for i in range(len(midpoints)):
       
            #increment counter is person is within tennis court 
            playerpoint= Point(midpoints[i])
            if (polytenniscourt.contains(playerpoint)):
                playerbox.append(boxes[i])
            else:
                continue
        #print("players box",playerbox)
        return playerbox


def setcoord(coord):
    
    courts_coord.append(coord)
  
def getcoord():
    
    return courts_coord

#@param image is image to be processed
# detects persons by calling detectpersondnn method
#calculates midpoin of each bounding box by calling calculatemidpoint method
#counts the number of players by calling isplayer method and using tennis court coordinates from database
def detectplayer(image):
    boxes = detectpersondnn(image,0.49)
    midpoint = calculatemidpoint(boxes)
    playerbox = isplayer(midpoint,boxes)
    
#same use as previous method except 
#counts the number of players by calling isplayer method and using tennis court coordinates from annotated json file
#@param court is annotated court coordinate read from json file
#@param boxes is the bounding boxes of persons detected for that image 
#@returns the bounding boxes of players detected
def detectannotatedplayer(court,boxes):
    midpoint = calculatemidpoint(boxes) 
    return testplayer(court,midpoint,boxes) 
    