#!/usr/bin/env python
import os
import shutil
import hashlib
import time 

"""
Backup scripts and setting.
"""

def make_filename(file):
    """ Hash the filename with time variant. """
    return hashlib.sha1(file+"%f"%time.time()).hexdigest()

    
def backup(file, dest):
    """ Backup the files to destination. """
    file=os.path.expanduser(file)
    if os.path.exists(file) == False:
        raise RuntimeError("The file you want to backup does not exist!")
        
    dest="%s/%s%s"%(os.path.abspath(os.path.expanduser(dest)),make_filename(file),".tar.bz2")
    print "Start to tar %s to %s" % (file,dest)
    """ Tar the target into a single file """
    os.system("cd %s && tar -jpc -f %s ./%s" % (os.path.split(os.path.abspath(file))[0], dest, os.path.split(os.path.abspath(file))[1]))
    print "Backup success"

def recover(file, dest):
    """ look up file is log and copy it to that path. """

backup("~/.emacs.d","~/backup/")

