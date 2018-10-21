# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:24:55 2018
@author: Metin
"""

import fnmatch
import shutil
import os
import re

count = 0
directory = 'news'

for root, dir_names, file_names in os.walk(directory):
    for filename in fnmatch.filter(file_names, '*.avi'):
        filename_new = re.sub(r'.*', str(count) + ".avi", filename)
        shutil.move(os.path.join(root, filename), os.path.join(root, filename_new))
        count += 1
