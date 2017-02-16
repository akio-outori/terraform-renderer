#!/usr/bin/python

import os
import yaml
import shutil
import random
from jinja2 import Template

class terraform_generator():

  def __init__(self, template, system=''):
    self.data       = self.__read_yaml(template)
    self.parent_dir = self.__createDir(template, system)
    self.__constructVars()
    self.__constructInstance()
    self.__constructSG()

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
      extension = template.find('.yml')
      try:
        os.makedirs(template[0:extension] + '/' + system)
        return template[0:extension] + '/' + system
      except:
        return "Directory " + template + '/' + system + " could not be created!"

  def __readSource(self, source_file):
    with open(source_file) as f:
      content = f.read()
    return content

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

  def writeMetaData(self):
    for source in [ "templates/.gitignore", "templates/aws_config.tf" ]:
      shutil.copy(source, self.parent_dir)    

