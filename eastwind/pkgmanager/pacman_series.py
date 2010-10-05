'''
Eastwind Package Management Interface Pacman Implementation
'''

import subprocess

import eastwind.utils as utils
from manager_base import EastwindPkgMangerSkeleton

class EastwindPkgMangerPacman(EastwindPkgMangerSkeleton):
    def update(self):
        utils.need_root_access('pacman -Syy')
        handle = subprocess.Popen('sudo pacman -Syy',
                                  shell=True)

    def upgrade(self):
        utils.need_root_access('pacman -Su')
        handle = subprocess.Popen('sudo pacman -Su',
                                  shell=True).wait()
        stdout, stderr = handle.communicate('y\n')

    def install(self, pkgs):
        utils.need_root_access('pacman -S')
        handle = subprocess.Popen('sudo pacman -S %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        utils.need_root_access('pacman -S')
        handle = subprocess.Popen('sudo pacman -S %s' % (" ".join(pkgs)),
                                  shell=True).wait()

    def purge(self, pkgs):
        utils.need_root_access('pacman -Rns')
        handle = subprocess.Popen('sudo pacman -Rsn --purge %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

#    def add_external_sources(self, sources):
#        utils.need_root_access('add-apt-repository')
#        for source in sources:
#            print 'Adding %s to system...' % source
#            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
#                                      shell=True).wait()

#TODO AUR
