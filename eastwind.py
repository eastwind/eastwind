#!/usr/bin/env python
"""
Main script for setting recovering
"""

from backup import *
from infoio import *
from time import *
import os
import re
import sys

class EastWind:
    ppa_list = []
    install_list = []
    backup_list = JsonInfo('backup.json')

    def cli(self):
        if len(sys.argv) == 1:
            self.load()
            self.recover()
            self.source()
            self.update()
            self.install()
        elif sys.argv[1] == "install":
            self.to_install(sys.argv[2])
        elif sys.argv[1] == "ppa":
            self.to_ppa(sys.argv[2])
        elif sys.argv[1] == "backup":
            self.clean_backup()
            self.load()
            self.backup()
        else:
            print "The argument is not correct!"

    def to_install(self, pkg):
        install_list.append(pkg)
        self.install()
        #TODO: check if the pkg is installed correctly before adding it into json
        s = JsonInfo("%s.json" % strftime("%Y-%m-%d"))
        s.info['Apps'].append({"name": pkg})
        s.write()

    def to_ppa(self, pkg_src):
        ppa_list.append(pkg)
        self.source()
        #TODO: check if the ppa is correctly added
        s = JsonInfo("%s.json" % strftime("%Y-%m-%d"))
        s.info['Apps'].append({"ppa": pkg_src})
        s.write()


    def load(self):
        """ Loads all the settings from ./setting """
        print "Start loading settings:"
        for jsons in os.listdir('setting'):
            if re.match("[^.]*.json$", jsons) == None:
                continue
            s = JsonInfo('setting/%s' % jsons)
            print "    Loading %s" % jsons
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
        os.system("rm backup/*.tar.bz2")
        os.remove("backup.json")
        self.backup_list = JsonInfo("backup.json")

    def backup(self):
        """ Backup files """
        print "Start to backup files:"
        for i in self.backup_list.info['Path']:
            print "  %s" % i["path"]
            i["backuped"] = backup(i["path"])
        self.backup_list.write()

    def recover(self):
        """ Recover files """
        for i in self.backup_list.info['Path']:
            if 'backuped' in i:
                recover(i['backuped'], i['path'])

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
    e = EastWind()
    e.cli()

