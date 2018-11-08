import cv2
import imageio

face_cascade = cv2.CascadeClassifier('cascades/haarcascade-frontalface-default.xml')

def detect(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    return frame

reader = imageio.get_reader('deneme.avi')
fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('output.avi',fps =fps)
for i,frame in enumerate(reader):
        frame = detect(frame)
        writer.append_data(frame)
        print(i)
writer.close()