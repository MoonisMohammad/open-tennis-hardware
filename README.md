## About this repo

#### Hardware
A camera sensor is wired to a raspberry pi via the camera port as shown in the appendix 5 and it has been configured to capture an image every ten minutes. The captured image is processed on the raspberry pi to extract relevant data such as the number of tennis courts and the number of players on a court, and to preserve the privacy of tennis court players, the captured image is deleted immediately after it has been processed.
To ensure that the camera can capture quality photos to perform object detection for the occupancy of the tennis facility, it is recommended to have one camera for a maximum of two tennis courts and the camera and raspberry pi must be set up at an optimal position where a captured image includes the four corners of each tennis court. The above criteria are critical to obtaining an accurate number of tennis courts and the number of players on a court when the captured image is processed. 
Therefore, at a facility with four tennis courts, there will be two cameras, each on opposite ends, to capture all the courts properly. This is required because it will become very difficult to outline the tennis courts and to differentiate between people playing tennis (players) and people not playing tennis (spectators)  in the background.

#### Image Processing 
After an image is captured by the set-up camera, it is processed on the raspberry pi for person and tennis court detection. The data obtained from person and tennis court detection are further used to differentiate between players and spectators as our goal is to detect the number of players on a tennis court and update the real-time occupancy of that tennis court.
#### Person Detection 
Person Detection is performed using Histogram of Oriented Gradients (HOG) with a pre-trained machine learning model, Support Vector Machine (SVM). HOG is a feature descriptor that extracts useful features from image data. 
The input image is preprocessed by converting the image to grayscale and HOG moves a sliding detection window of a fixed size around the grayscale image. For each window, features are extracted and the gradient in x and y direction is computed. The gradient in x direction is the difference between the pixel intensities in x direction, and the gradient in y direction is the difference between the pixel intensities in the x direction. The HOG gradient magnitude is then calculated using the equation (gradient in x direction)2 + (gradient in y direction)2 . The HOGgradient direction is calculated using the equation tan-1(gradient in x directiongradient in y direction). The HOG gradient magnitude and direction is computed for each sliding window. 
A Histogram of gradients is generated using the above computed values. The HOG gradient direction has values between 0and 180, thus, a histogram of 9 bins is used. The HOG gradient magnitude calculated for each window is placed in the appropriate histogram bin.  For each window, the sum of each histogram bin is calculated and a feature vector (HOG Description Vector) of the sum of size 9 is generated. 
The feature vector is then supplied to a pre-trained SVM classifier to classify whether the window is of a person or not [1].The main constraint in our system is the limited amount of training data, thus, HOG with SVM is used in our system as it is the most suitable machine learning model with a high accuracy and does not require a large amount of the training data and can run on a raspberry pi.

## Installation steps

1. Install Java - Download and install ```Python 3``` from https://www.python.org/downloads/. 
2. Install rails - Download and install ```Vscode``` from https://code.visualstudio.com/download
3. In Vscode import the following python libraries numpy, shapely, pysqlite3, argparse, imutils, tk, requires.io, opencv-python




