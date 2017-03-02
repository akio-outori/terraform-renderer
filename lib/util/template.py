#!/usr/bin/python

import os
from jinja2 import Template
from files import read as read_file

def read(source_file, parent_dir):
    dest_file = parent_dir + "/" + os.path.basename(source_file)
    content   = Template(read_file(source_file))
    return dest_file, content
