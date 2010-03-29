#!/usr/bin/env python
import os
import sys
ans=''
print "Backup or recover?(b/r)"
ans=raw_input().strip()
print "where is your emacs lisp file directory?"
lisp_dir=raw_input()#todo need to remove / at end

if (ans=='b'):
    print "Backing up your .emacs and emacs lisp"
    os.system("rm -rf ./emacs")
    os.system("mkdir emacs")
    os.system("cp -p ~/.emacs ./emacs ")
    os.system("cd "+lisp_dir.strip()+" && tar -jpcv -f ~/backup/emacs/lisp.tar.bz2 ./*")
    

if (ans=='r'):
    print "Recovering your .emacs and emacs lisp"
    os.system("rm -rf "+lisp_dir.strip())
    os.system("rm ~/.emacs")
    os.system("mkdir "+lisp_dir.strip())	
    os.system("cp -p ./emacs/.emacs ~/")
    os.system("tar -jxv -f ./emacs/lisp.tar.bz2 -C "+ lisp_dir.strip())
