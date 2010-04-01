#!/usr/bin/env python
"""
Main script for setting recovering
"""

from backup_test import *
from infoio import *
import os
import re
import sys

class EastWind:
    ppa_list = []
    install_list = []
    backup_list = JsonInfo('backup.json')

    def __init__(self):
        if len(sys.argv) == 1:
            self.load()
            self.recover()
            self.source()
            self.update()
            self.install()
        elif sys.argv[1] == "backup":
            self.load_backup_list()
            self.backup()
        else:
            print "The argument is not correct!"

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
            # for t in s.info['Backup']:
            #     if 'path' in t:
            #         if type(t['path']) == list:
            #             tmp = t.copy()
            #             for u in t['path']:
            #                 tmp.['path'] = u
            #         else:
            #             self.backup_list.info['Path'].append(t)

    def load_backup_list(self):
        # TODO might need to improve the performence of checking a file is in 
        # list or not
        """
        load 'path' from json files, add them to backup list if
        it's not in the list.
        """
        for jsons in os.listdir('setting'):
            if re.match("[^.]*.json$",jsons) == None:
                continue
            blist = json.dumps(self.backup_list.info['Path'])
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
                                blist = json.dumps(
                                        self.backup_list.info['Path'])
                    else:
                        if t['path'] not in blist:
                            print "add %s to backup list" % t['path']
                            self.backup_list.info['Path'].append(t)
                            blist = json.dumps(self.backup_list.info['Path'])

    # def clean_backup(self):
    #     os.system("rm backup/*.tar.bz2")
    #     os.remove("backup.json")
    #     self.backup_list = JsonInfo("backup.json")

    def backup(self):
        """ Backup files """
        print "Start to backup files:"
        b = self.backup_list.info['Path']
        for i in b[:]:
            print "  %s" % i["path"]
            tmp = backup(i)
            #print tmp
            if tmp != None:
                b[b.index(i)]=tmp.copy()
            else:
                # tmp == None if the i['path'] is not exist.
                b.remove(i)
        self.backup_list.write()
        """  Remove old backup files. """

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
    EastWind()

