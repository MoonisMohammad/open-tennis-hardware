import tkinter as tk
import cv2
import argparse
from database import *
#from shapely.geometry import Popint, Polygon
from courtreference import *
def creategui():
    #for test purposes
    
    
    window = tk.Tk()
    greeting = tk.Label(text="Hello, This GUI is designed to set up reference points for a tennis court")
    greeting.pack()
    
    #spacelabel allows button or other features to be spaced
    spacelabel = tk.Label(text = " ")
    spacelabel.pack()
    
    userlabel= tk.Label(text="userID")    #user inputs his/her name
    pwlabel = tk.Label(text = "passsword")   #user inputs his/her email   
    #courtlabel= tk.Label(text="Enter court number") 
    #allowing user to input data 
    entry = tk.Entry()
    entry1 = tk.Entry()
    #entry2 = tk.Entry() 

    userlabel.pack()
    entry.pack()
    pwlabel.pack()
    entry1.pack()
    #courtlabel.pack()
    #entry2.pack()
    spacelabel.pack()
    label=tk.Label(text="Select 4 reference points for each tennis court respectively. Start with court 1. The 4 optimal references are the 4 corner points of a court")
    label.pack()
    
    #get userid and password, compare to authenticate user
    #if user is authenticated, buttons will appear 
    
    #def reset():
        #none
        
    def delete():
        print("deleting")
    
    #For test purposes, the camera instantly captures an image and allows user to set references 
    #def captureimage():
        #none
    #saves the reference points in a database
    def save():
        arrpt = getpts()
        print(arrpt)
        print(adapt_array(arrpt))
        cursor.execute("INSERT INTO courtdatabase (court,points) VALUES (?,?)", (1,adapt_array(arrpt)))
        dbconnect.commit()
         
#         #newarrpt = np.reshape(arrpt, (maxcourt, 4))
#         print(arrpt)
#         print(type(arrpt[0][0]))
#         cursor.execute("INSERT INTO database (court,x1,y1,x2,y2,x3,y3,x4,y4) VALUES (?,?,?,?,?,?,?,?,?)", (1,(arrpt[0][0]),(arrpt[0][1]),(arrpt[1][0]),(arrpt[1][1]),(arrpt[2][0]),(arrpt[2][1]),(arrpt[3][0]),(arrpt[3][1])))
#         dbconnect.commit()
#         cursor.execute("INSERT INTO database (court,x1,y1,x2,y2,x3,y3,x4,y4) VALUES (?,?,?,?,?,?,?,?,?)", (2,(arrpt[4][0]),(arrpt[4][1]),(arrpt[5][0]),(arrpt[5][1]),(arrpt[6][0]),(arrpt[6][1]),(arrpt[7][0]),(arrpt[7][1])))
#         dbconnect.commit()
        
    
    #button0 =  tk.Button(window,text = "Enter Court Number",command = courtnum)
    #button0.pack()
    button =  tk.Button(window,text = "Set Up Reference",command = ref)
    button.pack()
    spacelabel.pack()
    button1 =  tk.Button(window,text = "Delete Point",command = delete)
    button1.pack()
    spacelabel.pack()
    button2 =  tk.Button(window,text = "OK",command = save)
    button2.pack()
    #button3 =  tk.Button(window,text = "START SOFTWARE",command = start)
    #button3.pack()


#the following method displays the image captured when the setup button is clicked on the gui
#user is allowed to click 4 reference points of the tennis court on the image
#when the image is clicked, the coordinates of that point is stored

    window.mainloop()  

if __name__=="__main__":
    gui = creategui()