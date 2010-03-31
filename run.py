#!/usr/bin/env python
"""
Main script for setting recovering
"""

from backup import *
from infoio import *
import os
import re
import sys

class EastWind:
    ppa_list = []
    install_list = []
    backup_list = JsonInfo('backup.json')

    def __init__(self):
        if sys.argv[1] == "backup":
            self.load()
            self.clean_backup()
            self.backup()
            #print self.backup_list.info
        elif len(sys.argv) == 1:
            self.load()
            self.recover()
            self.source()
            self.update()
            self.install()
        else:
            print "The argument is not correct!"

    def load(self):
        """ Loads all the settings from ./setting """
        print "Start loading settings:"
        for jsons in os.listdir('setting'):
            if re.match("[^.]*.json", jsons) == None:
                continue
            s = JsonInfo('setting/%s' % jsons)
            print "    Loading %s" % s
            for t in s.info['Apps']:
                if "name" in t:
                    self.install_list.append(t["name"])
                if "ppa" in t:
                    self.ppa_list.append(t["ppa"])
            for t in s.info['Backup']:
                if "path" in t:
                    if type(t['path']) == list:
                        for u in t['path']:
                            self.backup_list.info['Path'].append({"path": u})
                    else:
                        self.backup_list.info['Path'].append({"path": t['path']})

    def clean_backup(self):
        #open("backup.json", 'w').close()
        self.backup_list = JsonInfo("backup.json")
        """ TODO: delete brz2 """

    def backup(self):
        """ Backup files """
        print " Start to backup files:"
        for i in self.backup_list.info['Path']:
            print "%s" % i["path"]
            i["backuped"] = backup(i["path"])
        self.backup_list.write()

    def recover(self):
        """ Recover files """

    def source(self):
        print "Start adding sources:"
        for i in self.ppa_list:
            os.system("add-apt-repository %s" % i)

    def update(self):
        print "Updating:"
        os.system("apt-get update")

    def install(self):
        print "Installing:"
        os.system("apt-get install --yes %s" % " ".join(self.install_list))

if __name__ == "__main__":
    EastWind()

