#!/usr/bin/python

import random
import os
import sys
from lib.util.parse_yaml import read as read_yaml
from lib.util.files import mkdir, cp, read
from lib.util.template import read as read_template 

class terraform():
    
  def __init__(self, template):
    self.template   = read_yaml(template)
    self.variables  = self.template[0]['config']

    self.__setEnv()
    self.__getTemplates()

  def __setEnv(self):
    self.env = 'inventory/environments/' + self.variables['environment']['name'] + '/' + self.variables['name']

  def __getTemplates(self):
    self.templates = os.listdir('lib/templates' + '/' + self.variables['class'])
    self.templates = [ os.path.abspath('lib/templates' + '/' + self.variables['class']) + '/' + template for template in self.templates ]

  def write(self):
    mkdir(self.env)
    for template in self.templates:
      content   = read_template(template)
      dest_file = self.env + '/' + os.path.basename(template)
      with open(dest_file, 'w') as f:
        f.write(content.render(variables=self.variables)) 
