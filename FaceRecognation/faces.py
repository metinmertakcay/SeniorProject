import numpy as np
import cv2
import pickle
import imageio

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face_LBPHFaceRecognizer.create()
recognizer.read("trainner.yml")
labels = {"person_name":1}

with open("labels.pickle",'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

def detect(frame):
     # resmi griye çeviriyoruz
     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

     # nesneleri algılıyor bir dikdörtgenler listesi döndürüyor
     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)

     for(x,y,w,h) in faces:
         roi_gray = gray[y:y+h, x:x+w]

         id_,conf = recognizer.predict(roi_gray)
         # videodan anladığım kadarıyla condifence değeri için kesin bir şey bulamadığından bahsediyor ve bu değerleri kullanıyor
         # bu değeri 60dan büyük yaptım bu sefer daha iyi buldu ama şuan mantığını tam anlayamadım
         if conf >= 45 and conf <=85:
             # eğer yüz tanırsa isim resme yazdırılıyor
             font = cv2.FONT_HERSHEY_SIMPLEX
             name = labels[id_]
             color = (255,255,255)
             stroke = 2
             cv2.putText(frame,name,(x,y-10),font,1,color,stroke,cv2.LINE_AA)
             color = (0, 0, 255)
             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
     return frame

# videodan okunup yeniden yazdırılıyor
reader = imageio.get_reader('deneme.avi')
fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('output.avi',fps =fps)
for i,frame in enumerate(reader):
        frame = detect(frame)
        writer.append_data(frame)
        print(i)
writer.close()
