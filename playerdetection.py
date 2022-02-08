from person import *
import numpy as np
import cv2
from database import *
from shapely.geometry import Polygon, Point
#calculate midpoints of bottom line using bottom points of bounding boxes
#given x,y,w,h start point always at top left corner and end point at bottom right corner
#top left = x,y|top right = x+w,y|bottom left = x,y+h|bottom right = x+w,y+h
#returns a numpy array storing the midpoints
def calculatemidpoint(bounding_boxes):
    midpoints= []
    #arrayi = []
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        midpointx = ((2*x)+w)/2
        midpointy = y+h
        midpoints.append((midpointx,midpointy))
        #arrayi.append(i)
    print(midpoints)
    isplayer(midpoints)
    #return midpoints



#reads the tennis court coordinates from the database and uses shapely to verify if person is player or spectator
def isplayer(midpoints):
    #midpoints = [(1605.5, 2248), (1688.5, 2538), (2344.5, 1518), (3968.5, 1551), (3682.5, 1394), (1899.5, 1437), (847.5, 1472), (2513.0, 2023), (1906.0, 1394), (999.0, 743)]
    playercount = 0
    cursor.execute("SELECT * from courtdatabase")
    record = cursor.fetchall()
    for row in record:
        courtid = row[0]
        courtarray = convert_array(row[1])
        print("ca",courtarray)
        polytenniscourt = Polygon(courtarray)
        print(polytenniscourt)
        for p in midpoints:
            #increment counter is person is within tennis court 
            playerpoint= Point(p)
            print(playerpoint)
            playerbool = polytenniscourt.contains(playerpoint)
            print(playerbool)
            if (playerbool== True):
                #rint(polytenniscourt.contains(playerpoint))
                playercount = playercount + 1
                
                
    print("court id, players", courtid, playercount) #write upload here
        #print(row[0],row[1])
        #print(convert_array(row[1]))
        #print(type(convert_array(row[1])))
        
image = 'playingr337.jpg'
boxes = detectperson(image)
midpoint = calculatemidpoint(boxes)
#isplayer()