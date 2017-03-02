#!/usr/bin/python

import os
import sys

def getCredentials():
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
