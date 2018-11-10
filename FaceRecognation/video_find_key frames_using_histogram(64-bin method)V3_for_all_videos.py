# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:02:59 2018
@author: Metin
"""
import numpy as np
import cv2
import os

"""RGB degerleri 0-255 arasında olacaktır. Bit_7 msb'yi(most significant bit) gösterir"""
def getMostSignificantBits(value):
    bit_7 = int(value / 128)
    value = value % 128
    bit_6 = int(value / 64)
    return bit_7, bit_6

def createRGBPixelValue(red, green, blue):
    createNewBitSequence = ''
    createNewBitSequence += '0'
    createNewBitSequence += '0'
    bit_7, bit_6 = getMostSignificantBits(red)
    createNewBitSequence += str(bit_7)
    createNewBitSequence += str(bit_6)
    bit_7, bit_6 = getMostSignificantBits(green)
    createNewBitSequence += str(bit_7)
    createNewBitSequence += str(bit_6)
    bit_7, bit_6 = getMostSignificantBits(blue)
    createNewBitSequence += str(bit_7)
    createNewBitSequence += str(bit_6)
    return int(createNewBitSequence, 2)

def calculateHistogram(prevFrame, size):
    hist = [0] * size
    height, width = prevFrame.shape
    for i in range(0, height):
        for j in range(0, width):
            hist[int(prevFrame[i][j]) - 1] += 1
    return np.array(hist, dtype=int)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



path = "../news"
createFolder("keyframes")
video_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
for x in range(0, video_count-1):
    videoName = path + "/" + str(x) + ".avi"
    print(videoName)
    createFolder("keyframes/" + str(x))
    video = cv2.VideoCapture(videoName)
    isFinish = False
    while (video.isOpened() and (isFinish == False)):
        """ Capture frame-by-frame """
        ret, frame = video.read()
        if ret == True:
            fps = video.get(cv2.CAP_PROP_FPS)
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

            count = 0
            first = True
            isFinish = False
            prevHist = [0] * 64
            prevFrame = np.zeros(shape=(height, width))
            currentFrame = np.zeros(shape=(height, width))

            ### DEGİSİKLİK ###
            cnt = 10
            while (video.isOpened() and (isFinish == False)):
                ret, frame = video.read()
                if ret == True:
                    if first == False:
                        for i in range(0, height):
                            for j in range(0, width):
                                currentFrame[i][j] = createRGBPixelValue(frame[i][j][0], frame[i][j][1], frame[i][j][2])
                        currentHist = calculateHistogram(currentFrame, 64)
                        dist = np.linalg.norm(currentHist - prevHist)

                        ### DEGİSİKLİK ###
                        dist = dist / (width * height)
                        cnt += 1
                        if (dist > 0.1):
                            cnt = 0
                        if (cnt == 2):
                            cv2.imwrite("keyframes/" + str(x) + "/%d.jpg" % count, frame)

                        ### DEGİSİKLİK ###
                        prevHist = currentHist
                    else:
                        cv2.imwrite("keyframes/" + str(x) + "/1.jpg", frame)
                        for i in range(0, height):
                            for j in range(0, width):
                                prevFrame[i][j] = createRGBPixelValue(frame[i][j][0], frame[i][j][1], frame[i][j][2])
                        prevHist = calculateHistogram(prevFrame, 64)
                        first = False

                    count += 1
                else:
                    isFinish = True

            video.release()
        else:
            """ Break the loop"""
            isFinish = True

    """ When everything done, release the video capture object"""
    video.release()