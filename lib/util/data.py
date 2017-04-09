#!/usr/bin/python

from os import sys
from lib.aws.ec2_defaults import ec2_defaults

def validate(template, category, *args):
    if isinstance(template[category], list):
        for item in template[category]:
            for option in args:
                try:
                    if item[option] is None:
                        print option + " is blank!  Blank options are not supported."
                        sys.exit(1)

                except KeyError, Argument:
                    try:
                        default = ec2_defaults(template['variables']['region'])
                        
                        if   category is 'variables' and option is 'vpc':
                            item[option] = default.vpc()
                        elif category is 'instances' and option is 'subnet':
                            item[option] = default.subnet(template['variables']['vpc'])
                        elif category is 'instances' and option is 'ami':
                            item[option] = default.ami()
                        elif category is 'instances' and option is 'user':
                            item[option] = "ec2-user"
                        elif category is 'security_groups' and option is 'name':
                            item['name'] = 'default_sg'
                        elif category is 'security_groups' and option is 'services':
                            item[option] = ['22']
                        
                        if item[option] == None:
                            raise TypeError
                    
                    except TypeError:
                        print "No valid default could be found for " + str(option)
                        sys.exit(1)


    else:
        for option in args:
            try:
                if template[category][option] is None:
                    print option + " is blank!  Blank options are not supported."
                    sys.exit(1)

            except KeyError, Argument:
                print "No valid option could be found for " + str(option)
                sys.exit(1)

    return template[category]


