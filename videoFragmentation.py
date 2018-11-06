# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 21:06:28 2018
@author: Metin
"""
import cv2

video = cv2.VideoCapture("news/28.avi")

fps    = video.get(cv2.CAP_PROP_FPS)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

count = 0
isFinish = False
while (video.isOpened() and (isFinish == False)):
    ret, frame = video.read()
    if ret == True:
        if (count / fps > 103):
            out.write(frame)

        cv2.imshow('frame', frame)
        count += 1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else:
        isFinish = True

video.release()
out.release()
cv2.destroyAllWindows()