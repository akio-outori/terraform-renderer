#!/usr/bin/python

import os
from jinja2 import Template, Environment
from files import read as read_file

def read(source_file):
    content   = Template(read_file(source_file))
    content.environment = Environment(trim_blocks=True)
    return content
