#!/usr/bin/env python
"""
Main script for setting recovering
"""

from infoio import *
import os
import re

ppa_list = []
install_list = []

for jsons in os.listdir('setting'):
    if re.match("[^.]*.json", jsons) == None:
        continue
    s = JsonInfo('setting/%s' % jsons)
    for t in s.info['Apps']:
        if "name" in t:
            install_list.append(t["name"])
        if "ppa" in t:
            ppa_list.append(t["ppa"])
    for t in s.info['Backup']

for i in ppa_list:
    os.system("add-apt-repository %s" % i)

os.system("apt-get update")
os.system("apt-get install --yes %s" % " ".join(install_list))

