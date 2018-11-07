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

video = cv2.VideoCapture("output.mp4")

fps    = video.get(cv2.CAP_PROP_FPS)
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

count = 0
first = True
isFinish = False
prevHist = [0] * 64
prevFrame = np.zeros(shape=(height, width))
currentFrame = np.zeros(shape=(height, width))

while(video.isOpened() and (isFinish == False)):
    ret, frame = video.read()
    if ret == True:
        if first == False:
            for i in range(0, height):
                for j in range(0, width):
                    currentFrame[i][j] = createRGBPixelValue(frame[i][j][0], frame[i][j][1], frame[i][j][2])
            currentHist = calculateHistogram(currentFrame, 64)
            dist = np.linalg.norm(currentHist - prevHist)
            dist = dist / (width * height)
            print(dist)
            if(dist > 0.1):
                cv2.imwrite("rgb_key_frame/%f.jpg" % float(count / fps), frame)
            prevHist = currentHist
        else:
            cv2.imwrite("rgb_key_frame/%f.jpg" % float(count / fps), frame)
            for i in range(0, height):
                for j in range(0, width):
                    prevFrame[i][j] = createRGBPixelValue(frame[i][j][0], frame[i][j][1], frame[i][j][2])
            prevHist = calculateHistogram(prevFrame, 64)
            first = False

        cv2.imshow('frame', frame)
        count += 1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else:
        isFinish = True

video.release()
cv2.destroyAllWindows()

file_list = os.listdir("rgb_key_frame")

i = 0
size = len(file_list)
while i < size:
    tmp = file_list[i].split('.')
    file_list[i] = tmp[0] + "." + tmp[1]
    i += 1

file_list.sort()

i = 0
while i < size:
    number = float(file_list[i])
    specific_list = [item for item in file_list if (float(item) >= number and  number + 1 >= float(item))]

    if (len(specific_list) > 2):
        del specific_list[0]
        del specific_list[-1]

        j = 0
        while j < len(specific_list):
            file_list.remove(specific_list[j])
            os.unlink("rgb_key_frame/%s" % specific_list[j] + ".jpg")
            j = j + 1
        size = len(file_list)
    i = i + 1