# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:55:28 2018
@author: Metin
"""

import cv2
import os

directory = 'dataset_presenter_detection/negative'
file_list = os.listdir(directory)

i = 0
size = len(file_list)
while i < size:
    try:
        image = cv2.imread('dataset_presenter_detection/negative/%s' % file_list[i])
        resized_image = cv2.resize(image, (320, 240), interpolation = cv2.INTER_AREA)
        cv2.imwrite('dataset_presenter_detection/negative/%s.jpg' % i, resized_image)
    except Exception as e:
        print(str(e))
    i += 1

"""print(file_list[0])
image = cv2.imread('dataset_presenter_detection/negative/%s' % file_list[0])
cv2.imshow("Show by CV2", image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
