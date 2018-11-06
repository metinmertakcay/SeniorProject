# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 23:43:46 2018
@author: Metin
"""
import os
import os.path
from keras.models import load_model
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

train_datagen = ImageDataGenerator()
valid_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
    directory   = r"dataset_presenter/train/",
    target_size = (320, 240),
    color_mode  = "rgb",
    batch_size  = 5,
    class_mode  = "binary",
    shuffle     = True
)

valid_generator = valid_datagen.flow_from_directory(
    directory   = r"dataset_presenter/validation/",
    target_size = (320, 240),
    color_mode  = "rgb",
    batch_size  = 5,
    class_mode  = "binary",
    shuffle     = True
)

"""padding = 'same' : means the size of output feature-maps are the same as the input feature-maps 
   activation = 'relu' : output x if x is positive and 0 otherwise."""
model = Sequential()
model.add(Conv2D(32, (5, 5), padding = 'same', activation = 'relu', input_shape = (320, 240, 3)))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding = 'same', activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding = 'same', activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation = 'relu', kernel_initializer='random_uniform'))
model.add(Dropout(0.25))
model.add(Dense(1, activation = 'softmax'))

model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

filepath = "model.h5py"
if(os.path.exists(filepath)):
    model = load_model(filepath)
    print("model.h5py bulunmaktadır.")
else:
    print("model bulunamadı.")

checkpointer = ModelCheckpoint(filepath, verbose=1, save_best_only=True)

"""
Steps_per_epoch should be equivalent to the total number of samples divided by the batch size.
steps_per_epoch = TotalTrainingSamples / TrainingBatchSize
validation_steps = TotalvalidationSamples / ValidationBatchSize
"""
model.fit_generator(
        train_generator,
        steps_per_epoch = 960,
        epochs = 10,
        validation_data = valid_generator,
        validation_steps = 146,
        verbose = 2,
        workers = 8,
        shuffle = True,
        callbacks=[checkpointer]
)
