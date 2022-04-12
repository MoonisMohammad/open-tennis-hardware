#@author Chhavi Sujeebun
#the following code allows the pi camera to capture images every 3 seconds
#the time delay can be modified according to our requirements
import time
import picamera

with picamera.PiCamera() as camera:
    camera.start_preview()
    for filename in camera.capture_continuous('/home/pi/Images/2court{counter:03d}.jpg'):
        print('Captured %s' % filename)
        time.sleep(3) 
    camera.stop_preview()
    camera.close()
    