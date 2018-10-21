# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 19:59:39 2018
@author: Metin
"""

import os

path = 'path'
for the_file in os.listdir(path):
    file_path = os.path.join(path, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)