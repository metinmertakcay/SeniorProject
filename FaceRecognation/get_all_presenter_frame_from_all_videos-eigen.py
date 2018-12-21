import numpy as np
import cv2
import pickle
import imageio
import os

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.EigenFaceRecognizer_create()
recognizer.read("trainner.yml")
labels = {"person_name":1}

with open("labels.pickle",'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

for x in labels:
    print(labels[x])


def detect(frame,i,j):
     # resmi griye çeviriyoruz
     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

     # nesneleri algılıyor bir dikdörtgenler listesi döndürüyor
     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)

     for(x,y,w,h) in faces:
         roi_gray = gray[y:y+h, x:x+w]

         id_,conf = recognizer.predict(cv2.resize(roi_gray,(128,128)))
         # videodan anladığım kadarıyla condifence değeri için kesin bir şey bulamadığından bahsediyor ve bu değerleri kullanıyor
         # bu değeri 60dan büyük yaptım bu sefer daha iyi buldu ama şuan mantığını tam anlayamadım
         # eğer yüz tanırsa isim resme yazdırılıyor

         font = cv2.FONT_HERSHEY_SIMPLEX
         name = labels[id_]
         color = (255,255,255)
         stroke = 2
         cv2.putText(frame,name,(x,y-10),font,1,color,stroke,cv2.LINE_AA)
         color = (0, 0, 255)
         cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
         createFolder("presenters/" + str(i))
         cv2.imwrite("presenters/" + str(i) + "/%s____%d____%d.jpg" %(name,conf,j), frame)
     return frame

# videodan okunup yeniden yazdırılıyor
path = "../news"
createFolder("presenters")
video_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
print(video_count)
for i in range(0, video_count-1):
    videoName = path + "/" + str(i) + ".avi"
    print(videoName)
    video = cv2.VideoCapture(videoName)
    isFinish = False
    imageName = 0
    while (video.isOpened() and (isFinish == False)):
        """ Capture frame-by-frame """
        ret, frame = video.read()
        if ret == True:
            frame = detect(frame,i, imageName)
            imageName += 1
        else:
            """ Break the loop"""
            isFinish = True

    """ When everything done, release the video capture object"""
    video.release()
