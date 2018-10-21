# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 21:06:28 2018
@author: Metin
"""
import cv2

""" VideoCapture object created and reading from input file
If the input is taken from the camera, pass 0 instead of the video file name. """
video = cv2.VideoCapture("deneme.avi")

length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (width, height))

""" Check if camera opened successfully """
if (video.isOpened()== False): 
  print("Error opening video stream or file")

isFinish = False
while(video.isOpened() and (isFinish == False)):
    """ Capture frame-by-frame """
    ret, frame = video.read()
    if ret == True:                
        """ Write out frame to video """
        out.write(frame) 
        
        """ Display the resulting frame """
        cv2.imshow('frame', frame)
 
        """ Press Q on keyboard to  exit """
        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else:
        """ Break the loop"""
        isFinish = True
 
""" When everything done, release the video capture object"""
video.release()
out.release() 

""" Closes all the frames """
cv2.destroyAllWindows()