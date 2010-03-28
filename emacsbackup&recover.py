#!/usr/bin/env python
import os
import sys
ans=''
print "Backup or recover?(b/r)"
ans=raw_input().strip()
print "where is your emacs lisp file directory?"
lisp_dir=raw_input()

if (ans=='b'):
    print "Backing up your .emacs and emacs lisp"
    os.system("rm -rf ./emacs")
    os.system("mkdir emacs")
    os.system("mkdir emacs/lisp")
    os.system("cp -p ~/.emacs ./emacs ")
    os.system("cp -pr "+lisp_dir.strip()+"/* ./emacs/lisp")
    

if (ans=='r'):
    print "Recovering your .emacs and emacs lisp"
    os.system("rm -rf "+lisp_dir.strip())
    os.system("rm ~/.emacs")
    os.system("mkdir "+lisp_dir.strip())	
    os.system("cp -p ./emacs/.emacs ~/")
    os.system("cp -pr ./emacs/lisp/* "+lisp_dir.strip())
