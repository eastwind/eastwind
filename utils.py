'''
Eastwind utils
'''

import logging
import os
import subprocess
import sys
import hashlib
import time

ROOT_PATH = '~/.config/eastwind/'

def app_path(path):
    """ Generate and make path for app """
    total_path = os.path.join(os.path.expanduser(ROOT_PATH), path)
    dir_path = os.path.dirname(total_path)
    try:
        os.mkdir(dir_path)
    except OSError: pass
    return total_path

def hash_name(name):
    """ Hashing a name for the temp folder """
    unhashed = "%s-%f" % (name, time.time())
    return hashlib.sha1(unhashed).hexdigest()

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

