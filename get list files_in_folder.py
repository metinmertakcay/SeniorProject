# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 20:18:42 2018
@author: Metin
"""

import os

file_list = os.listdir("key_frame")

i = 0
size = len(file_list)
while i < size:
    tmp = file_list[i].split('.')
    file_list[i] = float(tmp[0] + "." + tmp[1])
    i += 1

file_list.sort()
