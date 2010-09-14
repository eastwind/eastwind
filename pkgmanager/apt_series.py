'''
Eastwind Package Management Interface APT Implementation
'''

import subprocess

import utils
from manager_base import EastwindPkgMangerSkeleton

class EastwindPkgMangerAPT(EastwindPkgMangerSkeleton):
    def update(self):
        utils.need_root_access('apt-get update')
        handle = subprocess.Popen('sudo apt-get update',
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def upgrade(self):
        utils.need_root_access('apt-get upgrade')
        handle = subprocess.Popen('sudo apt-get upgrade',
                                  shell=True).wait()

    def install(self, pkgs):
        utils.need_root_access('apt-get install')
        handle = subprocess.Popen('sudo apt-get install %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        utils.need_root_access('apt-get install')
        handle = subprocess.Popen('sudo apt-get %s' % (" ".join(pkgs)),
                                  shell=True).wait()

    def purge(self, pkgs):
        utils.need_root_access('apt-get remove')
        handle = subprocess.Popen('sudo apt-get remove --purge %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')
        handle = subprocess.Popen('sudo apt-get autoremove --purge %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def add_external_sources(self, sources):
        utils.need_root_access('add-apt-repository')
        for source in sources:
            print 'Adding %s to system...' % source
            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
                                      shell=True).wait()
