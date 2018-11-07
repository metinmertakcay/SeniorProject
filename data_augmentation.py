# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 00:51:43 2018

@author: User
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import os

datagen = ImageDataGenerator(
            #rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            #shear_range=0.1,
            #zoom_range=0.1,
            #horizontal_flip=True,
            fill_mode='nearest')

i = 0
size = len(os.listdir("presenter_images"))

while i < size:
    img = load_img('presenter_images/%d.jpg' % i)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    
    j = 0
    for batch in datagen.flow(x, batch_size = 1, save_to_dir = 'augmentation', save_prefix='person', save_format='jpg'):
        j += 1
        if j > 3:
            break
    i += 1