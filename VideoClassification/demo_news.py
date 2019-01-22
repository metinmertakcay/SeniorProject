"""
Given a video path and a saved model (checkpoint), produce classification
predictions.

Note that if using a model that requires features to be extracted, those
features must be extracted first.

Note also that this is a rushed demo script to help a few people who have
requested it and so is quite "rough". :)
"""
from keras.models import load_model
from data_news import DataSet
import numpy as np
import glob
import cv2
import os
import imageio
os.environ["CUDA_VISIBLE_DEVICES"]="1"

def predict(data_type, seq_length, model, image_shape, video_name, class_limit):
    """ her seferinde bu fonksiyonda modeli yüklüyordu artık direk yüklenmiş modeli yolluyorum fonksiyona"""
    # model = load_model(saved_model)

    # Get the data and process it.
    if image_shape is None:
        data = DataSet(seq_length=seq_length, class_limit=class_limit)
    else:
        data = DataSet(seq_length=seq_length, image_shape=image_shape,
            class_limit=class_limit)
    
    # Extract the sample from the data.
    sample = data.get_frames_by_filename(video_name, data_type)

    # Predict!
    prediction = model.predict(np.expand_dims(sample, axis=0))
    print(prediction)
    sport = data.print_class_from_prediction(np.squeeze(prediction, axis=0))
    return sport

def putText(frame,label):
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    name = str(label)
    color = (255, 255, 255)
    stroke = 1
    cv2.putText(frame, name, (10, 30), font, 1, color, stroke, cv2.LINE_AA)
    return frame
def main():
    # model can be one of lstm, lrcn, mlp, conv_3d, c3d.
    model = 'lstm'
    # Must be a weights file.
    saved_model = 'data/checkpoints/lstm-features.008-0.127.hdf5'
    # Sequence length must match the lengh used during training.
    seq_length = 40
    # Limit must match that used during training.
    class_limit = 4

    # Demo file. Must already be extracted & features generated (if model requires)
    # Do not include the extension.
    # Assumes it's in data/[train|test]/
    # It also must be part of the train/test data.
    # TODO Make this way more useful. It should take in the path to
    # an actual video file, extract frames, generate sequences, etc.
    #video_name = 'v_Archery_g04_c02'
    video = 'v_Deneme_g28'
    video_class = "z"
    videos = glob.glob(os.path.join('data', 'test', video_class, video + '_c*.avi'))

    # Chose images or features and image shape based on network.
    if model in ['conv_3d', 'c3d', 'lrcn']:
        data_type = 'images'
        image_shape = (80, 80, 3)
    elif model in ['lstm', 'mlp']:
        data_type = 'features'
        image_shape = None
    else:
        raise ValueError("Invalid model. See train.py for options.")

    """ Videonun kaç fps olacağını öğrenmek için ilk videodaki fps değerini alıyorum """
    reader = imageio.get_reader(videos[0])
    fps = reader.get_meta_data()['fps']
    # Video yazıcıyı oluşturuyorum
    writer = imageio.get_writer(video + ".avi", fps=fps)
    reader.close()
    # Tüm ayırılmış videoları geziyorum
    """ modelli burda yüklüyorum ve aşağıdaki predict fonksiyonuna saved model yerine bu modeli gönderiyorum"""
    """ bu arada son chapteri bulamıyor bunun nedeni de son chapter 40 frameden az olduğu için o chapterin özellikleri
        çıkarılmıyor o yüzden hata verip sonlanıyor ama video yinede oluşuyor sadece son chapter yok """
    model = load_model(saved_model)
    for item in videos:
        # İtemi ayırıp sadece video isminini alıyorum
        news = item.split("\\")
        news_name = news[3]
        parts = news_name.split(".")
        video_name = parts[0]
        # Tahmin yapılıyor
        predict_label = predict(data_type, seq_length, model, image_shape, video_name, class_limit)
        # Tahmin edilen videoya tahmin sonucunu yazdırıyorum
        reader = imageio.get_reader(item)
        for i, frame in enumerate(reader):
            frame = putText(frame,predict_label)
            writer.append_data(frame)
        reader.close()
    writer.close()
if __name__ == '__main__':
    main()
