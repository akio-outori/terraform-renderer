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
    self.access_key, self.secret_key = self.__getAWSCredentials()
    self.__constructVars()
    self.__constructInstance()
    self.__constructSG()
    print(self.access_key + " " + self.secret_key)

  def __read_yaml(self, template):
    with open(template) as f:
      data = yaml.safe_load(f)  
    return data

  def __constructVars(self):
    self.region  = self.data['variables']['region']
    self.vpc     = self.data['variables']['vpc']
    self.subnet  = random.choice(self.data['variables']['subnet'].values())
    self.ami     = self.data['variables']['ami']
    self.keypair = self.data['variables']['keypair']
    self.user    = self.data['variables']['user']

  def __constructInstance(self):
    self.instance_name = self.data['instance']['name']
    self.instance_type = self.data['instance']['type']

  def __constructSG(self):
    self.prefix      = self.data['security_group']['prefix']
    self.description = self.data['security_group']['description']
    self.ports       = self.data['security_group']['ports']

  def __createDir(self, template, system):
    if ".yml" in template:
      extension  = template.find('.yml')
      parent_dir = template[0:extension] + '/' + system 
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

  def writeVars(self, source_file):
    dest_file = self.parent_dir + "/" + os.path.basename(source_file)
    content   = Template(self.__readSource(source_file))
  
    with open(dest_file, "w+") as f:
      f.write(content.render(region=self.region, vpc=self.vpc, subnet=self.subnet, ami=self.ami, keypair=self.keypair, user=self.user))

  def writeInstance(self, source_file):
    dest_file = self.parent_dir + "/" + os.path.basename(source_file)
    content   = Template(self.__readSource(source_file))

    with open(dest_file, "w+") as f:
      f.write(content.render(instance_name=self.instance_name, instance_type=self.instance_type))

  def writeSG(self, source_file):
    dest_file = self.parent_dir + "/" + os.path.basename(source_file)
    content   = Template(self.__readSource(source_file))

    with open(dest_file, "w+") as f:
      f.write(content.render(name=self.instance_name, prefix=self.prefix, description=self.description, ports=self.ports))

  def writeCredentials(self, source_file):
    dest_file = self.parent_dir + '/' + os.path.basename(source_file)
    content   = Template(self.__readSource(source_file))

    with open(dest_file, "w+") as f:
      f.write(content.render(access_key=self.access_key, secret_key=self.secret_key))

  def writeMetaData(self):
    for source in [ "templates/.gitignore", "templates/aws_config.tf" ]:
      shutil.copy(source, self.parent_dir)
    
