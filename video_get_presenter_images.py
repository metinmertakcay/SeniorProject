# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:48:53 2018
@author: Metin
"""

import os, os.path
import cv2

path = "news"
video_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

imageName = 0
for i in range(0, video_count):
    videoName = path + "/" + str(i) + ".avi"
    video = cv2.VideoCapture(videoName)

    if (video.isOpened()== False): 
      print("Error opening video stream or file")

    j = 1
    count = 10
    isFinish = False
    while(video.isOpened() and (isFinish == False) and count != 0):
        """ Capture frame-by-frame """
        ret, frame = video.read()
        if ret == True:
            if(j % 3 == 0):
                cv2.imwrite("presenter_images/%d.jpg" % imageName, frame)
                imageName += 1
                count -= 1
            j += 1
                
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
    
    """ Closes all the frames """
    cv2.destroyAllWindows()