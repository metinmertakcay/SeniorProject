# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 21:06:28 2018
@author: Metin
"""
import cv2

""" VideoCapture object created and reading from input file
If the input is taken from the camera, pass 0 instead of the video file name. """
video = cv2.VideoCapture("deneme.avi")
fps   = video.get(cv2.CAP_PROP_FPS)

""" Check if camera opened successfully """
if (video.isOpened()== False): 
  print("Error opening video stream or file")

count = 0
isFinish = False
while(video.isOpened() and (isFinish == False)):
    """ Capture frame-by-frame """
    ret, frame = video.read()
    if ret == True:
        """ save frame as JPEG file """
        cv2.imwrite("frame/%f.jpg" % float(count/fps), frame)
        count += 1
        
        """ Display the resulting frame """
        cv2.imshow('frame', frame)
 
        """ Press Q on keyboard to  exit """
        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else: 
        """ Break the loop """
        isFinish = True
 
""" When everything done, release the video capture object"""
video.release()
 
""" Closes all the frames """
cv2.destroyAllWindows()