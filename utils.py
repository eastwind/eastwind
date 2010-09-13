'''
Eastwind utils
'''

import os
import sys
import subprocess

# TODO: implement a logging/debugging interface

def need_root_access():
    if not 0 ==  os.geteuid():
        print 'Error: please run eastwind with sudo'
        sys.exit(1)

