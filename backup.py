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

class RecoverError(Exception):
    def __init__( self , value ):
        self.value = value
    def __str__( self ):
        return repr( self.value )

def backup_path(file):
    """ Hash the filename with time variant. """
    hashed = hashlib.sha1("%s-%f" % (file, time.time())).hexdigest()
    return "backup/%s.tar.bz2" % hashed

def backup(file):
    """ Backup the files to destination. """
    # file['path'] file['name'] file['version'] file['backuped']
    # 'version' and 'backuped' might not exist if this is the first time
    # of backing up this file.
    _path = os.path.expanduser(file['path'])
    if os.path.exists(_path) == False:
        print "    %s does not exist!" % _path
        return None
    print "    Start to tar %s" % _path
    """ Tar the target into a single file """
    mtime = os.stat(_path).st_mtime
    # mtime is the last modified time of this file or dir.
    if 'version' in file:
        # file['version'] record the modified time of the previous 
        # backuped file.
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
    # return a dict variable with same format. 

def recover(file, dest):
    """
    Copy the backed file to that path.
    return values:
        0 : recover properly.
        1 : failed to recover but backuped file exist.
        2 : can't find backuped file.
    """
    file = os.path.abspath(file)
    dest = os.path.expanduser(dest)

    if os.path.exists(file) == False:
        raise NotFoundError( file )
    if os.path.exists(dest) == False:
        print "    %s does not exist, make it." %dest
        os.makedirs(os.path.expanduser(dest))
        # Since dest doesn't exist, let atime = 0
        atime = 0
    else:
        # otherwise atime equal to last access time of dest.
        atime = os.stat( dest ).st_atime

    print "    Start to recover %s " % file
    os.system("tar -xjp -f %s -C %s" % (file,os.path.split(dest)[0]))
    #print "    Recovering %s success" % file
    if checkfile( dest , atime ) == True:
       print "    Recovering %s success" % file
    else:
       raise RecoverError( file )
    # TODO need to see if there is a better way to check whether the file
    # is recovered properly. 

def checkfile( fname , ftime ):
    """
    fname : file name
    ftime : the latest access time of the file should be later than this.
    """
    if os.path.exists(fname) == False:
        return False

    t = os.stat(fname).st_atime
    if t > ftime:
        return True
    else:
        return False
