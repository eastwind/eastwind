'''
Eastwind utils
'''

import logging
import logging.handlers
import os
import subprocess
import sys

CONFIG_DIR = os.path.expanduser('~/.config/eastwind')
LOG_FILE = os.path.expanduser('~/.config/eastwind/eastwind.log')

try:
    os.mkdir(CONFIG_DIR)
except OSError: pass

def need_root_access(name):
    if not 0 ==  os.geteuid():
        subprocess.Popen('sudo -v', shell=True).wait()
