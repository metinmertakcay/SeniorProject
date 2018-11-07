# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 21:38:08 2018
@author: Metin
"""

import numpy as np
import cv2
import os

"""
    CNN ağı eğitimi başka bir dosyada yapılacaktır. Eğitim sonucunda oluşan ağırlıklar bir dosyada saklanacaktır. 
    Saklanan ağırlık değerleri burada okunacaktır.
"""


"""
    Bütün videolar teker teker okunacaktır. Programın çalışıp çalışmadığını test etmek amacıyla test 1 video 
    kullanılmıştır  
"""
video = cv2.VideoCapture("deneme.avi")

fps    = video.get(cv2.CAP_PROP_FPS)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

if (video.isOpened()== False): 
    print("Error opening video stream or file")

count = 0
isFinish = False
prevHist = [0] * 256
while(video.isOpened() and (isFinish == False)):
    ret, frame = video.read()
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        hist = cv2.calcHist(gray, [0], None, [256], [0,256]).ravel()
        dist = np.linalg.norm(prevHist-hist)
        prevHist = hist
        
        if(dist > 65.0):
            cv2.imwrite("video_key_frame/%f.jpg" % round(float(count/fps), 6), frame)
        count += 1
 
        if cv2.waitKey(25) & 0xFF == ord('q'):
            isFinish = True
    else: 
        isFinish = True

video.release()
cv2.destroyAllWindows()


"""
    Test işlemleri için (sunucu olup olmadığının tespiti) çıkartılmış olan key frameler kullanılacaktır.Bu yüzden 
    dosyadaki bütün resimlerin isimleri okunuyor.
"""
file_list = os.listdir("video_key_frame")

i = 0
size = len(file_list)
while i < size:
    tmp = file_list[i].split('.')
    file_list[i] = float(tmp[0] + "." + tmp[1])
    i += 1

file_list.sort()


"""
    Ağ kullanılarak key framelerdeki sunucu tespit edilecektir. Her bir key frame için bir liste (result) oluşturulacak. 
    Bu liste sunucu olup olmadığı bilgisini (0 veya 1) tutacaktır. Sunucu tespiti ağ eğitimi sonucunda olacaktır.
"""
result = [0] * len(file_list)

video  = cv2.VideoCapture("deneme.avi")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output_deneme.mp4", fourcc, int(fps), (width, height))

if (video.isOpened()== False): 
    print("Error opening video stream or file")

i = 0
res = 0
count = 0
isFinish = False
while(video.isOpened() and (isFinish == False)):
    ret, frame = video.read()
    if ret == True:
        if ((i < len(file_list)) and (file_list[i] == round(float(count/fps), 6))):
            res = result[i]
            i = i + 1
        if res == 0:
            out.write(frame)
        count += 1
    else: 
        isFinish = True

video.release()
out.release()
cv2.destroyAllWindows()


"""
    Bir sonraki videodan çıkarılacak key framelerin saklanıp işlenebilmesi için eski videodaki key frameler dosya
    içerisinden siliniyor
"""
path = 'video_key_frame'
for file in os.listdir(path):
    file_path = os.path.join(path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
