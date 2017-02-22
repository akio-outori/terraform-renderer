#!/usr/bin/python

import os
import re
import sys
import yaml
import shutil
import random
from jinja2 import Template

class terraform_generator():

  def __init__(self, template, system):
    self.data                        = self.__read_yaml(template)
    self.parent_dir                  = self.__createDir(template, system)

  def __read_yaml(self, template):
    with open(template) as f:
      data = yaml.safe_load(f)  
    return data

  def __constructVars(self, category, *args):
    try:
      for option in args:  
        if self.data[category][option] is None:
          print option + " is blank!  Blank options are not supported."
          sys.exit(1)
    
    except KeyError, Argument:
      print "No value specified for " + category + ":" + Argument[0]
      sys.exit(1)
    
    return self.data[category]
      
  def __createDir(self, template, system):
    parent_dir = os.path.dirname(template) + '/' + system 
    try:
      if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
      
      return parent_dir
    
    except:
      print("Directory " + parent_dir + " could not be created!")
      sys.exit(1)

  def __readSource(self, source_file):
    with open(source_file) as f:
      content = f.read()
    return content

  def __getAWSCredentials(self):
    try:
      with open(os.path.expanduser('~') + '/' + '.aws/credentials') as credfile:
        for line in credfile:
          if 'aws_access_key_id' in line:
            access_key = line[20:].strip()
          elif 'aws_secret_access_key' in line:
            secret_key = line[24:].strip()
    
    except:
      print("Could not read credential file!")
      sys.exit(1)
    
    return access_key, secret_key

  def __getDestFile(self, source_file):
    dest_file = self.parent_dir + "/" + os.path.basename(source_file)
    content   = Template(self.__readSource(source_file))
    return dest_file, content

  def writeVars(self, source_file):
    dest_file, content = self.__getDestFile(source_file) 
    variables          = self.__constructVars('variables', 'region', 'vpc', 'subnet', 'ami', 'keypair', 'user')
    with open(dest_file, "w+") as f:
      f.write(content.render(random=random, variables=variables)) 
         
  def writeInstance(self, source_file):
    dest_file, content = self.__getDestFile(source_file)
    instance           = self.__constructVars('instance', 'name', 'type')
    with open(dest_file, "w+") as f:
      f.write(content.render(instance=instance))

  def writeSG(self, source_file):
    dest_file, content = self.__getDestFile(source_file)
    instance           = self.__constructVars('instance', 'name')
    security_group     = self.__constructVars('security_group', 'prefix', 'description', 'services')
    with open(dest_file, "w+") as f:
      f.write(content.render(instance=instance, security_group=security_group))

  def writeCredentials(self, source_file):
    dest_file, content     = self.__getDestFile(source_file)
    access_key, secret_key = self.__getAWSCredentials()
    with open(dest_file, "w+") as f:
      f.write(content.render(access_key=access_key, secret_key=secret_key))

  def writeMetaData(self):
    for source in [ "templates/.gitignore", "templates/aws_config.tf" ]:
      shutil.copy(source, self.parent_dir)
    
