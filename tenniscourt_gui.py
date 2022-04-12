#@author chhavi sujeebun, updated

#importing libraries required and importing the methods from other python scripts 
import tkinter as tk
import cv2
import numpy as np
import argparse
from database import *
from courtreference import *
from playerdetection import *
from upload import *
from timeit import default_timer as timer

#initializing numpy arrays to store coordinates for the court with id 0 and 1
court0_coord =[]
court1_coord =[]
#initializing numpy array to store the array of coordinates for all existing courts 
courts_coord =[]


#creategui method creates a GUI to allow an authorised user to select reference points for one or more tennis courts.
#The reference points are then stored in a MySQL database, the image is further used for object detection and to determine
#the number of players on each tennis court
#@param image -is the image to be processed
#in our case, we are using images from our dataset, however when implementd the image will be the image captured by the picamera
def creategui(image):
    #for test purposes to record the time taken for the method to execute
    #start = timer()
    
    #creating the GUI window with labels and buttons 
    window = tk.Tk()
    greeting = tk.Label(text="Hello, This GUI is designed to set up reference points for a tennis court")
    greeting.pack()
    
    #spacelabel allows button or other features to be spaced
    spacelabel = tk.Label(text = " ")
    spacelabel.pack()
    
    #label with instructions for user to know hoe to select reference points
    label=tk.Label(text="Select reference points for each tennis court respectively. Start with court 0. The 4 optimal references are the 4 corner points of a court")
    label.pack()
    
    #The following methods are defined and called when a specific button is pressed in the GUI
    
    #refcall calls the method ref from courtreference.py with parameter image to be processed
    #This method displays the image and records the coordinate of any mouse click in an array
    #the mouse clicks are the reference points chosen
    def refcall():
        ref(image)
        
    #delete0 deletes the reference point for tennis court with id 0 from the database courtdb
    def delete0():
        cursor.execute("DELETE FROM courtdb WHERE court = 0")  
        dbconnect.commit()
        
    #delete1 deletes the reference point for tennis court with id 1 from the database courtdb
    def delete1():
        cursor.execute("DELETE FROM courtdb WHERE court = 1")  
        dbconnect.commit() 

    #save calls the method detectplayer from playerdetection.py
    #detectplayer method makes use of the Mobilenet SSD object detection model to detect the number of players
    #and update the playercount accordingly and upload it to the server
    def save():
        detectplayer(image)
        
        #for testing purposes, records the time taken for the method to be processed
        #elapsed_time = timer() - start
        #print("time", elapsed_time)

    #setupc0 calls the method refcall which will display the image and allow user to select reference points by clicking on the image
    #method getpts() is called from courtreference.py to obtain an array containing all the reference points selected in the image
    #the database is then updated with the obtained array in the row where the court is 0
    #resetarr is called from courtreference.py to clear the array meant to store points for court 0 so that previous points are not stored as well when new points are selected
    def setupc0():
        refcall()
        arrpt = getpts()
        cursor.execute('''UPDATE courtdb SET points = ? WHERE court= 0''',[str(arrpt)])             
        dbconnect.commit()
        resetarr()

    #setupc1 has the same use as setupc0, except the database is then updated with the obtained array in the row where the court is 1
    def setupc1():
        refcall()
        arrpt = getpts()
        cursor.execute('''UPDATE courtdb SET points = ? WHERE court=1''',[str(arrpt)])             
        dbconnect.commit()
        resetarr()
         
    #The following code are to create buttons for the GUI and command is the method to be called when a specific button is selected on the GUI
    buttonc1 =  tk.Button(window,text = "Set Up court0",command = setupc0)
    buttonc1.pack()
    buttonc2 =  tk.Button(window,text = "Set Up court1",command = setupc1)
    buttonc2.pack()
    button1 =  tk.Button(window,text = "Delete court0 points",command = delete0)
    button1.pack()
    button3 =  tk.Button(window,text = "Delete court1 points",command = delete1)
    button3.pack()
    button2 =  tk.Button(window,text = "OK",command = save)
    button2.pack()

    window.mainloop()


#the main function that calls the methos creategui when tenniscourt_gui.py is executed.
if __name__=="__main__":
    #For test purposes
    #list of images for testing ['2court058.jpg', 'playingr306.jpg', ' playingr326.jpg', 'playingr337.jpg','playingr364.jpg', 'playingr383.jpg','playingr391.jpg']
    
    #currently GUI is set to process the image '2court058.jpg'
    #the image name can be changed to test for different images 
    gui = creategui('2court058.jpg')
    
        