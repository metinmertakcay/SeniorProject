import cv2
import os
import imageio

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir,"data")
# data içine ayıralacak videoları koyuyorum ve onları burada okuyorum
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        # Thumbs.db dosyası kendiliğinden oluşabiliyor ve hata verebiliyor o yüzden kontrol ediyorum ve değilse işlem yapıyorum
        if filename != "Thumbs.db":
            # videonun olduğunu dizin
            file = "data/" + filename
            # video ismi için videonun noktadan önceki kısmını alıyorum
            parts = filename.split(".")
            filename = parts[0]
            # videoyu okuyorum
            reader = imageio.get_reader(file)
            fps = reader.get_meta_data()['fps']
            video_chapter_name = 1
            writer = imageio.get_writer("videos/" +filename + "_c" +str(video_chapter_name).zfill(2) + ".avi", fps=fps)
            for i, frame in enumerate(reader):
                writer.append_data(frame)
                if ((i+1) % 40 == 0):
                    writer.close()
                    video_chapter_name = video_chapter_name + 1
                    writer = imageio.get_writer("videos/" + filename + "_c" + str(video_chapter_name).zfill(2) + ".avi", fps=fps)
            writer.close()




