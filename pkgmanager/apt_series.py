'''
Eastwind Package Management Interface APT Implementation
'''

import subprocess

import utils
from manager_base import EastwindPkgMangerSkeleton

class EastwindPkgMangerAPT(EastwindPkgMangerSkeleton):
    def update(self):
        utils.need_root_access()
        handle = subprocess.Popen('sudo aptitude update',
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE).wait()

    def upgrade(self):
        utils.need_root_access()
        handle = subprocess.Popen('sudo aptitude upgrade',
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)
        stdout, stderr = handle.communicate('y\n')

    def install(self, pkgs):
        utils.need_root_access()
        handle = subprocess.Popen('sudo aptitude install %s' % (" ".join(pkgs)),
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        # TODO: replace this with a shell script instead?
        utils.need_root_access()
        handle = subprocess.Popen('sudo apt-get %s' % (" ".join(pkgs)),
                                  shell=True)

    def purge(self, pkgs):
        utils.need_root_access()
        handle = subprocess.Popen('sudo aptitude purge %s' % (" ".join(pkgs)),
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)
        stdout, stderr = handle.communicate('y\n')
