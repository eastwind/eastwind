

"""
Backup scripts and setting.
"""
import os
import shutil

def make_filename(file):
    """ Hash the filename with time variant. """

def backup(file, dest):
    file=os.path.expanduser(file)
    """ Backup the files to destination. """
    if os.path.exists(file) == False:
        raise RuntimeError("The file you want to backup does not exist!")
    """ Tar the target into a single file """
    os.system("cd %s && tar -jpcv -f %s ./%s" % (os.path.split(os.path.abspath(file))[0], dest, os.path.split(os.path.abspath(file))[1]))

def recover(file, dest):
    """ look up file is log and copy it to that path. """
