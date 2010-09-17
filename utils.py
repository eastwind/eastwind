'''
Eastwind utils
'''

import logging
import os
import subprocess
import sys

CONFIG_DIR = os.path.expanduser('~/.config/eastwind')
LOG_FILE = os.path.expanduser('~/.config/eastwind/eastwind.log')

try:
    os.mkdir(CONFIG_DIR)
except OSError: pass

def slog(level, msg):
    if level == 'DEBUG':
        prefix = ''
    elif level == 'INFO':
        prefix = ''
    elif level == 'WARNNING':
        prefix = ''
    elif level == 'ERROR':
        prefix = ''
    elif level == 'FATAL':
        prefix = ''

    print >> sys.stderr, '%s%s\033[m' % (prefix, msg)

def need_root_access(name):
    '''
    Prompt user for updating timestamp of sudo
    '''
    if not 0 ==  os.geteuid():
        subprocess.Popen('sudo -v', shell=True).wait()
