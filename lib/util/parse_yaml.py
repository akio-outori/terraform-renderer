#!/usr/bin/python

import yaml

def read(template):
     with open(template) as f:
         data = yaml.safe_load(f)
         return data
