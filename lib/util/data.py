#!/usr/bin/python

def validate(template, category, *args):
    try:
        for option in args:  
            if template[category][option] is None:
                print option + " is blank!  Blank options are not supported."
                sys.exit(1)
        
        return template[category]

    except KeyError, Argument:
        print "No value specified for " + category + ":" + Argument[0]
        sys.exit(1)

