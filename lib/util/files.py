#!/usr/bin/python

import os
import sys
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
    try:    
      shutil.copy(source, dest)
    except Exception as error:
      print error
      sys.exit(1)

def read(source_file):
  with open(source_file) as f:
    return f.read()

