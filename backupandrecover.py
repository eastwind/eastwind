#!/usr/bin/env python
import os
import shutil


def backupfile(file):
    work_dir=os.popen('pwd').read().strip()
    home_dir=os.popen('echo $HOME').read().strip()
    if (not(os.path.exists('backup'))):
        os.makedirs('backup')
    if (not(os.path.exists(file))):
        raise RuntimeError("The file you want to backup does not exist!")
        
    
    if os.path.isdir(file):
        file=os.path.abspath(file)
        os.system("cd "+file.strip()+" && tar -jpcv -f "+work_dir+"/backup/lisp.tar.bz2 ./*")
        
    if not(os.path.isdir('file')):
        file=os.path.abspath(file)
        dir=os.path.split(file)[0]
        os.system("cd "+dir.strip()+" && tar -jpcv -f "+work_dir+"/backup/lisp.tar.bz2 ./"+        os.path.split(file)[1])
           
    """
    Copy file ( if it is a file copy it, if it is a directory tar it).
    Save the original path in a seperate log.
    """

def recoverfile(file):
    """
    look up file is log and copy it to that path.
    """

backupfile('/home/lucaspeng/a')
