
import cv2
import os
import imageio

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face_LBPHFaceRecognizer.create()
recognizer.read("trainner.yml")
labels = {"person_name":1}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# keyframes klasöründeki keyfamelerin videoda kaçıncı frame olduğu her resim için başlık olarak yazdırdım
# daha sonra bu keyframlerin kaçıncı karede olduğu keyframes dizisine kayıt ediliyor
def add_keyframe(image_dir):
    keyframes = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            file = file.replace(".jpg","")
            if not file == "Thumbs.db":
                keyframes.append(int(file))
    print(keyframes)
    return  keyframes

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


# frame'de sunucu var ise 1 yok ise 0 döndürüyor
def detect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:
            return 1
    return 0

path = "../news"
createFolder("VideosWithoutPresenter")
video_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
print(video_count)
write = 0
# şimdilik ilk 16 videonun keyframeleri belli olduğundan 15e kadar yazdırdım daha sonra video count olarak değiştirilecek
for i in range(1, 15):
    videoName = path + "/" + str(i) + ".avi"
    video = cv2.VideoCapture(videoName)
    fps = video.get(cv2.CAP_PROP_FPS)
    isFinish = False

    # keyframeler listeye alınıyor
    keyframes = []
    keyframes = add_keyframe("keyframes/" + str(i))

    # dosyanın yazılacağı dizin
    writer = imageio.get_writer("VideosWithoutPresenter/" + str(i) + ".avi", fps=fps)
    j = 0
    write = 0
    while (video.isOpened() and (isFinish == False)):
        """ Capture frame-by-frame """
        ret, frame = video.read()
        if ret == True:
            # keyframe'in olduğu karede presenter var mı diye kontrol ediliyor var ise videoya yazma kesiliyor
            # yazma kesildikten itibaren bir sonraki keyfame'e geldiğinde yine sunucu var mı diye kontrol ediyor
            # eğer sunucu yoksa yine yazmaya başlıyor
            if (j in keyframes):
                presenter = detect(frame)
                if (presenter == 1):
                    write = 0
                else:
                    write = 1
            if (write == 1):
                # bu renk değişimi yapıldığı zaman renkleri farklı yazıyor video daha mavimsi oluyor
                scene = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(scene)
            j = j + 1
        else:
            """ Break the loop"""
            isFinish = True

    """ When everything done, release the video capture object"""
    video.release()
    writer.close()


