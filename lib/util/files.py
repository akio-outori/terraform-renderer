#!/usr/bin/python

import os
import shutil

def mkdir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)

        return path
                
    except:
        print("Directory " + path + " could not be created!")
        sys.exit(1)

def cp(source, dest):
    if not os.path.isfile(dest + '/' + os.path.basename(source)):
        shutil.copy(source, dest)

def read(source_file):
    with open(source_file) as f:
        return f.read()

