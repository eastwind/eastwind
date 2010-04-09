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
            self.load_backup_list()
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

    def load_backup_list(self):
        # TODO The performence of checking blist might not be good enough.
        """
        load 'path' from json files, add them to backup list if
        it's not in the list.
        """
        # blist record the 'path' which are already in backup_list
        # when we add a path into backup_list, we also add it into blist
        blist = []
        for v in self.backup_list.info['Path']:
            blist.append(v['path'])

        for jsons in os.listdir('setting'):
            if re.match("[^.]*.json$",jsons) == None:
                continue

            s = JsonInfo( 'setting/%s' % jsons )
            for t in s.info['Backup']:
                if 'path' in t:
                    if type(t['path']) == list:
                        v = t.copy()
                        for u in t['path']:
                            if u not in blist:
                                print "add %s to backup list" % u
                                v['path']=u
                                self.backup_list.info['Path'].append(v.copy())
                                blist.append(u)
                    else:
                        if t['path'] not in blist:
                            print "add %s to backup list" % t['path']
                            self.backup_list.info['Path'].append(t)
                            blist.append(t['path'])

    def backup(self):
        """ Backup files """
        print "Start to backup files:"
        b = self.backup_list.info['Path']
        # Since we might change backup_list in the loop, we iterate on a
        # copy of b, which denote by b[:]
        for i in b[:]:
            print "  %s" % i["path"]
            tmp = backup(i)
            if tmp != None:
                b[b.index(i)]=tmp.copy()
            else:
                # tmp == None if i['path'] is not exist, remove it from
                # backup list
                b.remove(i)
        self.backup_list.write()
        """  Replace old backup list. """

    def recover(self):
        """ Recover files """
        for i in self.backup_list.info['Path']:
            if 'backuped' in i:
                try:
                    recover(i['backuped'], i['path'])
                except NotFoundError as e:
                    print "Can't find file %s" % e
                except RecoverError as e:
                    print "Failed to recover %s" % e

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

