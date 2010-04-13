#!/usr/bin/env python
"""
Main script for setting recovering
"""

from backup import *
from info import *
from time import *
import os
import re
import sys

class EastWind:
    data = Info()

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
            self.load()
            self.backup()
        elif sys.argv[1] == "recover":
            if len(sys.argv) == 3:
                self.recover(argv[2])
            else:
                self.recover()
        else:
            print "The argument is not correct!"

    def to_install(self, pkg):
        #TODO: check if the pkg is installed correctly before adding it into json
        conf = self.data.new_parser("setting/%s.conf" % strftime("%Y-%m-%d-%H-%M-%S"))
        conf.add_section("Install")
        conf.set("Install", "install", pkg)
        self.data.info["install"] = pkg
        self.install()
        self.data.write()

    def to_ppa(self, pkg_src):
        #TODO: check if the ppa is correctly added
        conf = self.data.new_parser("setting/%s.conf" % strftime("%Y-%m-%d-%H-%M-%S"))
        conf.add_section("Ppa")
        conf.set("Ppa", "ppa", pkg_src)
        self.data.info["ppa"] = pkg_src
        self.source()
        self.data.write()

    def load(self):
        """ Loads all the settings from ./setting """
        print "Start loading settings:"
        self.data.read_files('setting/', os.listdir('setting'))

    def load_recover(self):
        """ Load folders for recovery """
        print "    Find the folders for recovery"
        dirs = os.listdir('backup')
        for d in dirs:
            if re.match("^\.", d) != None:
                dirs.remove(d)
        return dirs

    def backup(self):
        """ Backup files """
        print "Start to backup files:"
        folder = strftime("%Y-%m-%d-%H-%M-%S")
        backupconf = Info()
        os.makedirs(os.path.abspath("backup/%s" % folder))
        conf = backupconf.new_parser("backup/%s/backup.conf" % folder)
        conf.add_section('Backuped')
        if 'backup' in self.data.info:
            for b in self.data.info['backup']:
                for j in b.split(' '):
                    try:
                        path = backup(j, folder)
                        conf.set('Backuped', j, path)
                    except NotFoundError as e:
                        print "    Error: Can't find file %s" % e
            backupconf.write()

    def recover(self, version = None):
        """ Recover files """
        if version == None:
            dirs = self.load_recover()
            if len(dirs) == 0:
                return
            version = max(dirs)
        path = "backup/%s/backup.conf" % version
        if not os.path.exists(path):
            print "    Error: Config file %s not exist!" % path
            return
        recoverconf = Info()
        recoverconf.read(path)
        print "Recovering files:"
        for i,j in recoverconf.info.items():
            try:
                recover(j[0], i)
            except NotFoundError as e:
                print "    Error: Can't find file %s" % e

    def source(self):
        if 'ppa' in self.data.info:
            print "Start adding sources:"
            for i in self.data.info['ppa']:
                os.system("add-apt-repository %s" % i)

    def update(self):
        print "Updating:"
        os.system("apt-get update")

    def install(self):
        if 'pre-install' in self.data.info:
            print "Executing pre-install commands:"
            for s in self.data.info['pre-install']:
                os.system(s)
        if 'install' in self.data.info:
            print "Installing:"
            os.system("apt-get install --yes %s" % " ".join(self.data.info['install']))
        if 'post-install' in self.data.info:
            print "Executing post-install commands:"
            for s in self.data.info['post-install']:
                os.system(s)

if __name__ == "__main__":
    e = EastWind()
    e.cli()

