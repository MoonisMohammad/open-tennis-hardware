## About this repo

#### Hardware
A camera sensor is wired to a raspberry pi via the camera port and it has been configured to capture an image every ten minutes. The captured image is processed on the raspberry pi to extract relevant data such as the number of tennis courts and the number of players on a court, and to preserve the privacy of tennis court players, the captured image is deleted immediately after it has been processed.
Tennis courts will be equipped with camera sensors such that we have a maximum of two tennis courts per camera sensor to ensure that the camera can capture quality photos to perform object detection for the occupancy of the tennis facility. It will capture images of the courts every ten minutes. To set up the system, an authorized user will have to access a graphical user interface in the raspberry pi to set up reference points for the tennis courts captured by the camera. These reference points are then added to an array and stored in a database. The camera is then set to capture images every ten minutes, the captured images will then be processed on the raspberry pi to detect the number of people in each image. The tennis court reference points and person detection data will then be further used to identify the number of  players on each tennis court. 
The number of players on a tennis court will  be sent to the server. The server will update its database and data from the database will be accessed by the app so that users can get current occupancy of the court.

Currently the code processes images from our dataset, however if the system is to be implemented, it will process real-time images captured by the camera every 10 minutes.

#### Image Processing 
After an image is captured by the set-up camera, it is processed on the raspberry pi for person and tennis court detection. The data obtained from person and tennis court detection are further used to differentiate between players and spectators as our goal is to detect the number of players on a tennis court and update the real-time occupancy of that tennis court.
#### Person Detection 
To detect persons, we have investigated two pre-trained object detection models using the Python library OpenCV. 

1. Histogram of Oriented Gradients (HOG) with a pre-trained machine learning model, Support Vector Machine (SVM). HOG is a feature descriptor that extracts useful features from image data. The input image is preprocessed by converting the image to grayscale and HOG moves a sliding detection window of a fixed size around the grayscale image. For each window, features are extracted and the gradient in x and y direction is computed. The gradient in x direction is the difference between the pixel intensities in x direction, and the gradient in y direction is the difference between the pixel intensities in the x direction. The HOG gradient magnitude is then calculated using the equation √(gradient in x direction)2 + (gradient in y direction)2 	. The HOGgradient direction is calculated using the equation tan-1(gradient in x direction/gradient in y direction). The HOG gradient magnitude and direction is computed for each sliding window. A Histogram of gradients is generated using the above computed values. The HOG gradient direction has values between 0and 180, thus, a histogram of 9 bins is used. The HOG gradient magnitude calculated for each window is placed in the appropriate histogram bin.  For each window, the sum of each histogram bin is calculated and a feature vector (HOG Description Vector) of the sum of size 9 is generated. 
The feature vector is then supplied to a pre-trained SVM classifier to classify whether the window is of a person or not.

2. The Mobilenet Single Shot Detector which takes one single shot to detect multiple objects within an image. This model is pre-trained on the COCO dataset which is a large-scale object detection, segmentation, and captioning dataset published by Microsoft. The SSD approach is based on a feed-forward convolutional network that produces a fixed size collection of bounding boxes and scores for the presence of object class instances in those boxes. MobileNet is the base network used for high quality image classification. Convolutional layers added to the end of the base network decrease progressively and allow predictions of detections at multiple scales. Each layer produces a fixed set of predictions using a set of convolutional filters. Non-max suppression is then used to remove duplicates and produce the final predictions. 

#### Player Detection
The data obtained from the Objection Detection models is then further used, to differentiate between players and spectators in the tennis court facility by verifying if the persons detected are within the predefined tennis court region or not.

The main constraint in our system is the limited amount of training data, thus, HOG with SVM and Mobilenet SSD is used in our system as it is the most suitable machine learning model with a relatively high accuracy and does not require a large amount of the training data and can run on a raspberry pi 3.

## Installation steps for Visual Studio Code

1. Install Python - Download and install ```Python 3``` from https://www.python.org/downloads/. 
2. Install visual Studio code - Download and install ```Vscode``` from https://code.visualstudio.com/download
3. In Vscode import the following python libraries numpy, shapely, pysqlite3, argparse, imutils, tk, requires.io, opencv-python
4. If the libraries are not already installed, open the ubuntu terminal in VS code and type the following commands:
  pip: sudo apt-get install python3-pip
  numpy: pip3 install numpy
  Shapely: pip3 install Shapely
  OpenCV: sudo pip3 install opencv-python
  pandas: pip3 install pandas 
  sqlite3: sudo apt install sqlite3
  tkinter: sudo apt-get install python3-tk
  csv: pip3 install python-csv
  json: pip install jsonlib
  argparse: pip install argparse
  imutils: sudo pip install imutils
  
5. Unzip the project and open it in VS code and run tenniscourt_gui.py in VS code by typing python3 tennniscourt_gui.py in the terminal
6. when step 5 is executed, a GUI will be displayed
   6.1 Use the buttons "Set Up court0" and "Set Up court1" to select reference points for the tennis courts with the corresponding id 0 or 1.
   6.2 Simply click the shown image to select your reference points
7. select the "OK" button to start the Mobilenet SSD Object Detection model
   7.1 The Object Detection model can be changed to HOG Descriptor by updating the code at line 124 in playerdetection.py to 'boxes = detectperson(image,     (2,2),(4,4),1.2)'
   
## Installation steps for Raspberry pi 3 Model B+
Open terminal window
1. Install python3 if it is not already installed by typing sudo apt-get install python3
2. Install the required libraries as explained in step 4 for Installation steps for Visual Studio Code
3. Unzip the project, cd into the file and run tenniscourt_gui.py by typing python3 tennniscourt_gui.py in the terminal window
4. Repeat steps 6 to 7 to run thr Object Detection models on the raspberry pi
5. To capture images using the pi camera, install the picamera library : pip install picamera and type python3 capturepic.py in the terminal

## Running Test
1. Ensure the required libraries are installed
2. run project_testing.py typing python3 project_testing.py in the terminal window
3. Testing can be done for both models
   Ensure that the imagepath is set to read images from the Images_sorted_updated folder for HOG Descriptor
   3.1 For Mobilenet SSD: line 260 in project_testing.py is set to 'personboxes = testdetectperson(imagename,confidence)'
   3.2: For HOG descriptor: line 260 in project_testing.py is set to 'personboxes = detectperson(imagepath,(2,2),(4,4),1.2)'
