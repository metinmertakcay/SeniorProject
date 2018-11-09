import os
import fnmatch
import shutil
import re
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sports_dir = os.path.join(BASE_DIR,"Sport Videos")

# klasör oluşturma
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#dosya isimleri 0,1,2 diye gidecek şekilde değiştiriliyor
def change_file_name(path):
    i = 0
    organized = 0
    for filename in os.listdir(path):
        if filename != "Thumbs.db":
            if filename == str(i) + ".avi":
                organized = 1
            if organized == 0:
                os.rename(os.path.join(path, filename), os.path.join(path, str(i) + '.avi'))
                i = i + 1

def writeFrames(sports_dir,sportName,name):
    path = sports_dir + "/" + sportName + "/" + name
    change_file_name(path)
    video_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    imageName = 0

    for i in range(0, video_count-1):
        videoName = path + "/" + str(i) + ".avi"
        print(videoName)
        video = cv2.VideoCapture(videoName)
        if (video.isOpened() == False):
            print("Error opening video stream or file %d")
            video.release()
        isFinish = False
        j = 1
        while (video.isOpened() and (isFinish == False)):
            """ Capture frame-by-frame """
            ret, frame = video.read()
            if ret == True:
                if (j % 2 == 0):
                    cv2.imwrite("Classification/" + sportName + "/" + name + "/%d.jpg" % imageName, frame)
                    imageName += 1
                j += 1
            else:
                """ Break the loop"""
                isFinish = True

        """ When everything done, release the video capture object"""
        video.release()



createFolder("Classification")
for root, dirs, files in os.walk(sports_dir):
        for sportName in dirs:
            if sportName != "train" and sportName != "test" and sportName != "valid": # son spor dosyasının içindeki klasörlerede baktığı için bu koşulu koydum
                createFolder(BASE_DIR + "/Classification/" + sportName)
                createFolder(BASE_DIR + "/Classification/" + sportName + "/train")
                createFolder(BASE_DIR + "/Classification/" + sportName + "/test")
                createFolder(BASE_DIR + "/Classification/" + sportName + "/valid")
                writeFrames(sports_dir,sportName,"train")
                writeFrames(sports_dir, sportName,"test")
                writeFrames(sports_dir, sportName,"valid")
