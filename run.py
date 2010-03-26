#!/usr/bin/env python

from cmdlib import *
from listing import *
import os

#print ppa_list
#print install_list

for i in ppa_list:
    os.system("add-apt-repository %s" % i)

os.system("apt-get update")

for i in install_list:
    os.system("apt-get install --yes %s" % i)

