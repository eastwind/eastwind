import os
import shutil
import hashlib
import time

"""
Backup scripts and setting.
"""
class NotFoundError(Exception):
    def __init__( self , value ):
        self.value = value
    def __str__( self ):
        return repr( self.value )

def backup_path(file, version):
    """ Hash the filename with time variant. """
    hashed = hashlib.sha1("%s-%f" % (file, time.time())).hexdigest()
    return "backup/%s/%s.tar.bz2" % (version, hashed)

def backup(file, version):
    """ Backup the files to destination. """
    path = os.path.expanduser(file)
    if os.path.exists(path) == False:
        raise NotFoundError(path)
    print "    Start to tar %s" % path
    # Tar the target into a single file
    filename = backup_path(path, version)
    os.system("cd %s && tar -jpc -f %s ./%s" % (
       os.path.split(os.path.abspath(path))[0],\
       os.path.abspath(filename),\
       os.path.split(os.path.abspath(path))[1] )
    )
    print "    Backup %s success" % path
    return filename

def recover(file, dest):
    """ Copy the backed file to that path. """
    file = os.path.abspath(file)
    dest = os.path.expanduser(dest)

    if os.path.exists(file) == False:
        raise NotFoundError(file)
    if os.path.exists(dest) == False:
        print "    %s does not exist, make it." %dest
        os.makedirs(os.path.expanduser(dest))

    print "    Start to recover %s " % file
    os.system("tar -xjp -f %s -C %s" % (file, os.path.split(dest)[0]))

    #TODO: need to see if there is a better way to check whether the file
    # is recovered properly.
    print "    Recovering %s success" % file

