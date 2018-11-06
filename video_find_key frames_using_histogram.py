# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:02:59 2018
@author: Metin
"""
# from matplotlib import pyplot as plt 
import numpy as np
import cv2

""" VideoCapture object created and reading from input file
If the input is taken from the camera, pass 0 instead of the video file name. """
video = cv2.VideoCapture("news/0.avi")

fps    = video.get(cv2.CAP_PROP_FPS)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

""" Define the codec and create VideoWriter object """
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output_grayscale.mp4", fourcc, int(fps), (width, height))
""" Check if camera opened successfully """
if (video.isOpened()== False): 
  print("Error opening video stream or file")

count = 0
prevHist = [0] * 256
isFinish = False
while(video.isOpened() and (isFinish == False)):
    """ Capture frame-by-frame """
    ret, frame = video.read()
    if ret == True:
        """ Our operations on the frame come here"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        hist = cv2.calcHist(gray, [0], None, [256], [0,256]).ravel()
        dist = np.linalg.norm(prevHist-hist)
        prevHist = hist
        
        if(dist > 65.0):
            cv2.imwrite("key_frame/%f.jpg" % float(count/fps), frame)
        count += 1
        
        """ Write out frame to video """
        out.write(frame) 
        
        """ Display the resulting frame """
        cv2.imshow('frame', frame)
 
        """ Press Q on keyboard to  exit """
        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else: 
        """ Break loop """
        isFinish = True
 
""" When everything done, release the video capture object"""
video.release()
out.release() 

""" Closes all the frames """
cv2.destroyAllWindows()



"""
    save frame as JPEG file
    # cv2.imwrite("grayscaleFrame/%f.jpg" % float(count/fps), frame)
    # count += 1

    # plt.hist(frame.ravel(), 256, [0, 256])
    # plt.show()
    # hist = cv2.calcHist(frame, [0], None, [256], [0,256])
    # plt.plot(hist)
    # plt.show()
    # input()
"""