#!/usr/bin/python

import sys
import yaml

def read(template):
    try:
        with open(template) as f:
            data = yaml.safe_load(f)
            return data
    except Exception, e:
        print("Invalid YAML" + str(e.problem_mark))
        sys.exit(1)
