from person import *
import numpy as np
import cv2
from database import *
from shapely.geometry import Polygon, Point
from persondetection_dnn import *
from tenniscourt_gui import *
from ast import literal_eval
from upload import *
#from database_postgres import *
courts_coord = []
authorizationId = "2OCC9876543210"    #use this auth Id its already registered in backend and is owned ny lyndwood manager and this device is named test data upload
static_ip = "52.229.94.153"               #ip address of server
#calculate midpoints of bottom line using bottom points of bounding boxes
#given x,y,w,h start point always at top left corner and end point at bottom right corner
#top left = x,y|top right = x+w,y|bottom left = x,y+h|bottom right = x+w,y+h
#returns a numpy array storing the midpoints
def calculatemidpoint(bounding_boxes):
    midpoints= []
    #print("BB",bounding_boxes)

    if len(bounding_boxes) == 0:
        return []
    else:
        for i, (x, y, w, h) in enumerate(bounding_boxes):
            midpointx = ((2*x)+w)/2
            midpointy = y+h
            midpoints.append((midpointx,midpointy))
            #arrayi.append(i)
        #print(midpoints)
        #isplayer(midpoints,bounding_boxes)
        return midpoints



#reads the tennis court coordinates from the database and uses shapely to verify if person is player or spectator
def isplayer(midpoints,boxes):
    playerbox =[]
    #midpoints = [(1605.5, 2248), (1688.5, 2538), (2344.5, 1518), (3968.5, 1551), (3682.5, 1394), (1899.5, 1437), (847.5, 1472), (2513.0, 2023), (1906.0, 1394), (999.0, 743)]
    cursor.execute("SELECT * from courtdb")
    #print("midpts",midpoints)
    #cursorpostgres.execute("SELECT * from courtdb")
    record = cursor.fetchall()
    #print("rec",len(record))
    #record = cursorpostgres.fetchall()
    #courts_coord = getallcourtscoord()
    #print("coord", courts_coord)
    
    for row in record:
        if(midpoints == None):
            playercount = 0
            break;
            #playercount = 0
        print("____________________")
    #carr = getcoord()
    #print("check", carr)
    #for i in range (len(carr)):
        playercount = 0
        #must check if it is empty or not 
        courtid = row[0]
        #courtid = i
        #print(courtid)
        #allow_pickle=True
        #ca = row[1]

        courtarray = literal_eval(row[1])
        #print("ca type", type(courtarray))
        #print("ca",courtarray)
            #do nothing
        #courtarray = row[1]
        
            #courtarray = carr[i]
        
        polytenniscourt = Polygon(courtarray)
        #print("polygon", polytenniscourt)
        #for p in midpoints:
        for i in range(len(midpoints)):
       
            #increment counter is person is within tennis court 
            playerpoint= Point(midpoints[i])
            #print(playerpoint)
            playerbool = polytenniscourt.contains(playerpoint)
            #print(playerbool)
            if (playerbool== True):
                #rint(polytenniscourt.contains(playerpoint))
                playercount = playercount + 1
                playerbox.append(boxes[i])
            else:
                playercount = playercount + 0
        
        print("court id", courtid)
        print("players", playercount)
        #print("players box",playerbox)
        #return playerbox
        
        #uploadData(referenceNumber,count,authorizationId,static_ip)
        #uploadData(courtid,playercount,authorizationId,static_ip)
        #print(row[0],row[1])
        #print(convert_array(row[1]))
        #print(type(convert_array(row[1])))
    
#detectplayer using provided court coordinates and bouding boxes of players 
def testplayer(court,midpoints,boxes):
    playerbox =[]
        
    polytenniscourt = Polygon(court)
    #print("polygon", polytenniscourt)
    #for p in midpoints:
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
    #np.append(courts_coord,coord, axis=0)
    courts_coord.append(coord)
    #print("cc")
    #print("len", len(courts_coord))
def getcoord():
    #print("ccg", courts_coord)
    return courts_coord
def detectplayer(image):
    #print("Image",image)
    #boxes = detectperson(image)
    boxes = detectpersondnn(image,0.56)
    midpoint = calculatemidpoint(boxes)
    playerbox = isplayer(midpoint,boxes)

def detectannotatedplayer(court,boxes):
    midpoint = calculatemidpoint(boxes) #calls isplayer method
    return testplayer(court,midpoint,boxes) 
    #playerbox = isplayer(midpoint,boxes)