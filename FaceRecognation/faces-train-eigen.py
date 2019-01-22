import os
import cv2
import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images")

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.EigenFaceRecognizer_create()

current_id=0
label_ids={}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root,file)
            file = file.replace(".jpg","")

            # etiket için klasör isimlerini alıyor
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            # eğer label dictionary'de yoksa yenisini ekliyor
            if not label in label_ids:
                label_ids[label] = current_id

                current_id += 1
            id_ = label_ids[label]


            pil_image = Image.open(path).convert("L") # grayscale

            # burayı yüzleri daha iyi tanıması için yaptı ama ben pek fark göremedim
            # size = (550,550)
            # final_image = pil_image.resize(size, Image.ANTIALIAS)

            image_array = np.array(pil_image,"uint8") # resmi array'e dönüştürme
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5) # yüzler bulunuyor
            for(x,y,w,h) in faces:
                # yüzleri ve id'yi diziye ekliyor
                roi = image_array[y:y+h, x:x+w]
                x_train.append(cv2.resize(roi,(128,128)))
                y_labels.append(id_)


# isimleri ve id'leri tutmak için dosyaya kaydediyor
with open("labels.pickle",'wb') as f:
    pickle.dump(label_ids,f)

# eğitim yapıp kaydediyor
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")


