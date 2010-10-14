'''
Eastwind Package Management Interface APT Implementation
'''

import subprocess

import eastwind.utils as utils

class EastwindPkgMangerAPT:
    def update(self):
        utils.need_root_access('apt-get update')
        handle = subprocess.Popen('sudo apt-get update',
                                  shell=True).wait()

    def upgrade(self):
        utils.need_root_access('apt-get upgrade')
        handle = subprocess.Popen('sudo apt-get upgrade',
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install(self, pkgs):
        utils.need_root_access('apt-get install')
        handle = subprocess.Popen('sudo apt-get install %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        utils.need_root_access('apt-get install')
        ret = subprocess.Popen('sudo apt-get install %s' % (" ".join(pkgs)),
                                  shell=True).wait()
        return ret

    def purge(self, pkgs):
        utils.need_root_access('apt-get remove')
        handle = subprocess.Popen('sudo apt-get remove --purge %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')
        handle = subprocess.Popen('sudo apt-get autoremove --purge',
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def purge_interactive(self, pkgs):
        utils.need_root_access('apt-get remove')
        ret = subprocess.Popen('sudo apt-get remove --purge %s' %
                               (" ".join(pkgs)), shell=True).wait()
        if 0 == ret:
            subprocess.Popen('sudo apt-get autoremove --purge',
                                      shell=True).wait()
        return ret

    def add_external_sources(self, sources):
        utils.need_root_access('add-apt-repository')
        for source in sources:
            print 'Adding %s to system...' % source
            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
                                      shell=True).wait()

