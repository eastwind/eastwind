#!/usr/bin/env python
import os
import shutil
import hashlib
import time

"""
Backup scripts and setting.
"""

def backup_path(file,dest):
    """ Hash the filename with time variant. """
    hashed = hashlib.sha1("%s-%f" % (file, time.time())).hexdigest()
    return "%s/%s.tar.bz2" %( os.path.abspath(os.path.expanduser(dest)),hashed)

def backup(file, dest):
    """ Backup the files to destination. """
    file = os.path.expanduser(file)
    if os.path.exists(file) == False:
        raise RuntimeError("The file you want to backup does not exist!")

    print "Start to tar %s" % file
    """ Tar the target into a single file """
    os.system("cd %s && tar -jpc -f %s ./%s" % (os.path.split(os.path.abspath(file))[0], backup_path(file,dest), os.path.split(os.path.abspath(file))[1]))
    print "Backup success"

def recover(file, dest):
    """ look up file is log and copy it to that path. """

