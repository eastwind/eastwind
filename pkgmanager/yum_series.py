'''
Eastwind Package Management Interface YUM Implementation
'''

import subprocess

import utils
from manager_base import EastwindPkgMangerSkeleton

class EastwindPkgMangerYUM(EastwindPkgMangerSkeleton):
    def update(self):
        utils.need_root_access('yum update')
        handle = subprocess.Popen('sudo yum update',
                                  shell=True)
        stdout, stderr = handle.communicate('n\n')

    def upgrade(self):
        utils.need_root_access('yum upgrade')
        handle = subprocess.Popen('sudo yum upgrade',
                                  shell=True).wait()

    def install(self, pkgs):
        utils.need_root_access('yum install')
        handle = subprocess.Popen('sudo yum install %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        utils.need_root_access('yum install')
        handle = subprocess.Popen('sudo yum install %s' % (" ".join(pkgs)),
                                  shell=True).wait()

    def purge(self, pkgs):
        utils.need_root_access('yum remove')
        handle = subprocess.Popen('sudo yum remove %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

# TODO: /etc/yum.repos.d
#    def add_external_sources(self, sources):
#        utils.need_root_access('add-apt-repository')
#        for source in sources:
#            print 'Adding %s to system...' % source
#            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
#                                      shell=True).wait()
