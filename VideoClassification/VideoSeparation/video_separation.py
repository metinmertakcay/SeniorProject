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
            print(fps)
            video_chapter_name = 1
            """" fpsi 30 dan büyük küçük diye ayırdım her 13 için çokta iyi gözükmediği için böyle yaptım"""
            if (fps > 30):
                each = 2
            if (fps <= 30):
                each = 1
            """" bu j değeri de each'e göre frame eklemek için kullandım 0 verince direk 40.satırdaki if'e girebileceği için -1 verdim"""
            j = -1
            """ eğer each 2 ise fpsi 2ye bölüyorum video hızlı hareket etmesin diye"""
            if (each==2):
                fps = int((fps/each))
            writer = imageio.get_writer("videos/" +filename + "_c" +str(video_chapter_name).zfill(2) + ".avi", fps=fps)
            for i, frame in enumerate(reader):
                if((i+1) % each == 0):
                    """ j -1 ise ilk kez girdiğini anlıyorum"""
                    if (j==-1):
                        j = 0
                    writer.append_data(frame)
                    j = j+1
                """ videoları 40 yerine 120 frame uzunlukta yaptım daha anlaşılır oluyor"""
                if (j % 120 == 0):
                    j = -1
                    writer.close()
                    video_chapter_name = video_chapter_name + 1
                    writer = imageio.get_writer("videos/" + filename + "_c" + str(video_chapter_name).zfill(2) + ".avi", fps=fps)
            writer.close()




