#!/usr/bin/python

import os
import shutil

def mkdir(template, system):
    try:
        parent_dir = os.path.dirname(template) + '/' + system
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
                
    except:
        print("Directory " + parent_dir + " could not be created!")
        sys.exit(1)

    return parent_dir

def cp(source, parent_dir):
    shutil.copy(source, parent_dir)

def read(source_file):
    with open(source_file) as f:
        return f.read()

