#!/usr/bin/env python
"""
Main script for setting recovering
"""

from backup import *
from info import *
from time import *
import environ

import os
import types
import re
import sys
import urllib2

class EastWind:
    data = Info()

    def cli(self):
        self.cmd = os.system
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
            log.error("Error: The argument %s is not correct!" % sys.argv[1])

    def to_install(self, pkg):
        #TODO: check if the pkg is installed correctly before adding it into json
        conf = self.load_auto()
        section = strftime("%Y-%m-%d-%H-%M-%S")
        conf.add_section(section)
        conf.set(section, "install", pkg)
        self.data.info["install"] = pkg
        self.install()
        self.data.write()

    def to_ppa(self, pkg_src):
        #TODO: check if the ppa is correctly added
        conf = self.load_auto()
        section = strftime("%Y-%m-%d-%H-%M-%S")
        conf.add_section(section)
        conf.set(section, "ppa", pkg_src)
        self.data.info["ppa"] = pkg_src
        self.source()
        self.data.write()

    def load(self):
        """ Loads all the settings from ./setting """
        log.section("Start loading settings:")
        self.data.read_files('setting/', os.listdir('setting'))

    def load_recover(self):
        """ Load folders for recovery """
        log.log("    Find the folders for recovery")
        dirs = os.listdir('backup')
        for d in dirs:
            if re.match("^\.", d) != None:
                dirs.remove(d)
        return dirs

    def load_auto(self):
        if os.path.exists("setting/auto.conf"):
            conf = self.data.read("setting/auto.conf")
        else:
            conf = self.data.new_parser("setting/auto.conf")
        return conf

    def backup(self):
        """ Backup files """
        log.section("Start to backup files:")
        folder = strftime("%Y-%m-%d-%H-%M-%S")
        backupconf = Info()
        os.makedirs(os.path.abspath("%s/%s" % (environ.backup_dir, folder)))
        conf = backupconf.new_parser("%s/%s/backup.conf" %
                                     (environ.backup_dir, folder))
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
        path = "%s/%s/backup.conf" % (environ.backup_dir, version)
        if not os.path.exists(path):
            log.error("    Error: Config file %s not exist!" % path)
            return
        recoverconf = Info()
        recoverconf.read(path)
        log.section("Recovering files:")
        for i,j in recoverconf.info.items():
            try:
                recover(j[0], i)
            except NotFoundError as e:
                log.error("    Error: Can't find file %s" % e)

    def source(self):
        if 'ppa' in self.data.info:
            log.section("Start adding sources:")
            for i in self.data.info['ppa']:
                self.cmd("add-apt-repository %s" % i)

    def update(self):
        log.section("Updating:")
        self.cmd("apt-get update")

    def install(self):
        if 'pre-install' in self.data.info:
            log.section("Executing pre-install commands:")
            for s in self.data.info['pre-install']:
                self.cmd(s)
        if 'install' in self.data.info:
            log.section("Installing:")
            self.cmd("apt-get install --yes %s" % " ".join(self.data.info['install']))
        if 'post-install' in self.data.info:
            log.section("Executing post-install commands:")
            for s in self.data.info['post-install']:
                self.cmd(s)

    def get( self , url , fname = None ):
        """ usage:
            get files from internet by using urllib
            url should be a string object
            if fname is not a string, use the last part of url as file name.
            Ex:
                get( "code.google.com/p/eastwind/issues/list" )
                ==> fname = "list"
        """
        #TODO: better policy for generate fname ?
        if type(url) != types.StringType :
            log.error( "In EastWind.get()" )
            log.error( "    url should be a string object" )
            return
        #TODO: what if 404 not found?
        if type(fname) != types.StringType :
            tmp = url.split("/")
            tmp.reverse()
            fname = tmp[0]
            log.section( "Set file name: %s" % fname )
        log.log( "    Getting file %s from %s." % ( fname , url ) )

        f = open(fname, 'w')
        data = urllib2.urlopen(url).read()
        f.write(data)
        f.close()


if __name__ == "__main__":
    e = EastWind()
    e.cli()

