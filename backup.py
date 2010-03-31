#!/usr/bin/env python
import os
import shutil
import hashlib
import time

"""
Backup scripts and setting.
"""

def backup_path(file):
    """ Hash the filename with time variant. """
    hashed = hashlib.sha1("%s-%f" % (file, time.time())).hexdigest()
    return "backup/%s.tar.bz2" % hashed

def backup(file):
    """ Backup the files to destination. """
    file = os.path.expanduser(file)
    if os.path.exists(file) == False:
        print "    %s does not exist!" % file
        return

    print "    Start to tar %s" % file
    """ Tar the target into a single file """
    filename = backup_path(file)
    os.system("cd %s && tar -jpc -f %s ./%s" % (os.path.split(os.path.abspath(file))[0], os.path.abspath(filename), os.path.split(os.path.abspath(file))[1]))
    print "    Backup %s success" % file
    return filename

def recover(file, dest):
    """ Copy the backed file to that path. """
    file = os.path.abspath(file)
    dest = os.path.expanduser(dest)
    if os.path.exists(file) == False:
        print "    %s is disappeared!" % file
        return
    print "    Start to recover %s " % file
    os.system("tar -xjp -f %s -C %s" % (file,os.path.split(dest)[0]))
    print "    Recovering %s success" % file
    """ TODO need to know if backup and recovering really succeed. Check modify time ."""

