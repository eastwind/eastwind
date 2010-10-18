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
        os.makedirs(dir_path)
    except OSError: pass
    return total_path

def record_path(name):
    return app_path('record/%s' % name)

def hash_name(name):
    """ Hashing a name for the temp folder """
    unhashed = "%s-%f" % (name, time.time())
    return hashlib.sha1(unhashed).hexdigest()

def slog(level, msg):
    '''
    Command line logging interface for Eastwind
    '''
    prefix = { 'DEBUG'    : '\033[1;32m',
               'INFO'     : '\033[1;34m',
               'WARNNING' : '\033[1;33m',
               'ERROR'    : '\033[1;31m',
               'FATAL'    : '\033[1;37;41m' };

    print >> sys.stderr, '%s%s\033[m' % (prefix[level], msg)

    if 'FATAL' == level:
        sys.exit(1)

def need_root_access(name):
    '''
    Prompt user for updating timestamp of sudo
    '''
    if not 0 ==  os.geteuid():
        subprocess.Popen('sudo -v', shell=True).wait()

