'''
Eastwind Package Management Interface APT Implementation
'''

import subprocess

class EastwindPkgMangerAPT:
    def update(self):
        handle = subprocess.Popen('sudo apt-get update',
                                  shell=True).wait()

    def upgrade(self):
        handle = subprocess.Popen('sudo apt-get upgrade',
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install(self, pkgs):
        handle = subprocess.Popen('sudo apt-get install %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        ret = subprocess.Popen('sudo apt-get install %s' % (" ".join(pkgs)),
                                  shell=True).wait()
        return ret

    def purge(self, pkgs):
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
        ret = subprocess.Popen('sudo apt-get remove --purge %s' %
                               (" ".join(pkgs)), shell=True).wait()
        if 0 == ret:
            subprocess.Popen('sudo apt-get autoremove --purge',
                                      shell=True).wait()
        return ret

    def add_external_sources(self, sources):
        for source in sources:
            print 'Adding %s to system...' % source
            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
                                      shell=True).wait()

