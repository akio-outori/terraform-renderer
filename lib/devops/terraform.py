#!/usr/bin/python

import random
import os
import sys
from lib.util.parse_yaml import read as read_yaml
from lib.util.files import mkdir, cp, read 
from lib.util.data import validate
from lib.util.template import read as read_template
from lib.util.aws import getCredentials

class terraform():
    
    def __init__(self, template, system):
        self.template   = read_yaml(template)
        self.parent_dir = mkdir(template, system)        

    def writeVars(self, source_file):
        dest_file, content = read_template(source_file, self.parent_dir) 
        variables          = validate(self.template, 'variables', 'region', 'vpc', 'subnet', 'ami', 'keypair', 'user')
        with open(dest_file, "w+") as f:
            f.write(content.render(random=random, variables=variables)) 
            
    def writeInstance(self, source_file):
        dest_file, content = read_template(source_file, self.parent_dir)
        instance           = validate(self.template, 'instance', 'name', 'type')
        with open(dest_file, "w+") as f:
            f.write(content.render(os=os, instance=instance))

    def writeSG(self, source_file):
        dest_file, content = read_template(source_file, self.parent_dir)
        instance           = validate(self.template, 'instance', 'name')
        security_group     = validate(self.template, 'security_group', 'prefix', 'description', 'services')
        with open(dest_file, "w+") as f:
            f.write(content.render(instance=instance, security_group=security_group))

    def writeCredentials(self, source_file):
        dest_file, content     = read_template(source_file, self.parent_dir)
        access_key, secret_key = getCredentials()
        with open(dest_file, "w+") as f:
            f.write(content.render(access_key=access_key, secret_key=secret_key))

    def writeMetaData(self):
        for source in [ "templates/terraform/.gitignore", "templates/terraform/aws_config.tf" ]:
            cp(source, self.parent_dir)
    
