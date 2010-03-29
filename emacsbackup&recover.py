#!/usr/bin/env python
import os
import sys
import shutil

ans=''
work_dir=os.popen('pwd').read().strip()
print work_dir
home_dir=os.popen('echo $HOME').read().strip()
print home_dir
print "Backup or recover?(b/r)"
ans=raw_input().strip()
print "where is your emacs lisp file directory?"
lisp_dir=raw_input()#todo need to remove / at end . use os.path.split

if (ans=='b'):
    print "Backing up your .emacs and emacs lisp"
    if(os.path.exists('emacs')):
        shutil.rmtree('emacs')
#    os.system("rm -rf /emacs")
    os.system("mkdir emacs")
    shutil.copy(home_dir+'/.emacs',work_dir+'/emacs/.emacs')
    os.system("cd "+lisp_dir.strip()+" && tar -jpcv -f "+work_dir+"/emacs/lisp.tar.bz2 ./*")
# use os.rmdir() to remove directory, use os.path.exists() to test file existence

if (ans=='r'):
    print "Recovering your .emacs and emacs lisp"
    if (os.path.exists(os.path.abspath(lisp_dir))):
        print lisp_dir+" already exist remove it"
        shutil.rmtree(os.path.abspath(lisp_dir))
    if (os.path.exists('~/.emacs')):
        print ".emacs already exist, remove it"
        os.unlink('~/.emacs')
    os.system("mkdir "+lisp_dir.strip())
    shutil.copy(work_dir+'/emacs/.emacs',home_dir+'/.emacs')
    #os.system("cp -p ./emacs/.emacs ~/")
    os.system("tar -jxv -f ./emacs/lisp.tar.bz2 -C "+ lisp_dir.strip())
