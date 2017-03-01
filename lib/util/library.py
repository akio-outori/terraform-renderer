#!/usr/bin/python

import os
import re
import sys
import yaml
import shutil
from jinja2 import Template

class library():
        
    def readYAML(self, template):
        with open(template) as f:
            self.data = yaml.safe_load(f)
            return self.data

    def constructVars(self, category, *args):
        try:
            for option in args:  
                if self.data[category][option] is None:
                    print option + " is blank!  Blank options are not supported."
                    sys.exit(1)
            return self.data[category]

        except KeyError, Argument:
            print "No value specified for " + category + ":" + Argument[0]
            sys.exit(1)
      
    def createDir(self, template, system):
        try:
            self.parent_dir = os.path.dirname(template) + '/' + system
            if not os.path.exists(self.parent_dir):
                os.makedirs(self.parent_dir)
                
        except:
            print("Directory " + self.parent_dir + " could not be created!")
            sys.exit(1)

    def copyFile(self, source):
        shutil.copy(source, self.parent_dir)

    def readSource(self, source_file):
        with open(source_file) as f:
            return f.read()

    def getAWSCredentials(self):
        try:
            with open(os.path.expanduser('~') + '/' + '.aws/credentials') as credfile:
                for line in credfile:
                    if 'aws_access_key_id' in line:
                        access_key = line[20:].strip()
                    elif 'aws_secret_access_key' in line:
                        secret_key = line[24:].strip()
            return access_key, secret_key

        except:
            print("Could not read credential file!")
            sys.exit(1)

    def getDestFile(self, source_file):
        dest_file = self.parent_dir + "/" + os.path.basename(source_file)
        content   = Template(self.readSource(source_file))
        return dest_file, content

