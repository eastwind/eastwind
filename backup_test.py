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
    """
    file['path'] file['name'] file['version'] file['backuped']
    """
    _path = os.path.expanduser(file['path'])
    if os.path.exists(_path) == False:
        print "    %s does not exist!" % _path
        return None
    print "    Start to tar %s" % _path
    """ Tar the target into a single file """
    mtime = os.stat(_path).st_mtime
    if 'version' in file:
        if mtime <= file['version']:
            print "    %s is up to date" % _path
            return file
    filename = backup_path(_path)
    os.system("cd %s && tar -jpc -f %s ./%s" % (
       os.path.split(os.path.abspath(_path))[0],\
       os.path.abspath(filename),\
       os.path.split(os.path.abspath(_path))[1] )
    )
    print "    Backup %s success" % _path
    return {'path':file['path'],'name':file['name'],
            'version':mtime,'backuped':filename}

def recover(file, dest):
    """ Copy the backed file to that path. """
    file = os.path.abspath(file)
    dest = os.path.expanduser(dest)
    if os.path.exists(file) == False:
        print "    %s is disappeared!" % file
        return
    if os.path.exists(dest) == False:
        print "    %s does not exist, make it." %dest
        os.makedirs(os.path.expanduser(dest))
        mtime = 0
    else:
        mtime = os.stat( dest ).st_atime
    print "    Start to recover %s " % file
    os.system("tar -xjp -f %s -C %s" % (file,os.path.split(dest)[0]))
    #print "    Recovering %s success" % file
    if checkfile( dest , mtime ) == True:
       print "    Recovering %s success" % file
    else:
       print "    Failed to recover %s" % file
    """
    TODO need to know if backup and recovering really succeed.
    Check modify time.
    """

def checkfile( fname , ftime ):
    """
        fname : file name ,
        ftime : the latest modified time of the file should be later than this.
    """
    t = os.stat(fname).st_atime
    if t > ftime:
        return True
    else:
        return False
