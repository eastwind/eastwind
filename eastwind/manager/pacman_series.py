'''
Eastwind Package Management Interface Pacman Implementation
'''

import subprocess
from os.path import exists
from platform import architecture

class EastwindPkgMangerPacman:
    def update(self):
        handle = subprocess.Popen('sudo pacman -Syy',
                                  shell=True)

    def upgrade(self):
        handle = subprocess.Popen('sudo pacman -Su',
                                  shell=True).wait()
        stdout, stderr = handle.communicate('y\n')

    def install(self, pkgs):
        handle = subprocess.Popen('sudo pacman -S %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        handle = subprocess.Popen('sudo pacman -S %s' % (" ".join(pkgs)),
                                  shell=True).wait()

    def purge(self, pkgs):
        handle = subprocess.Popen('sudo pacman -Rsn --purge %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    #def add_external_sources(self, sources):
    #    #if exists('/usr/bin/yaourt'):
    #    #    return

    #    with open('/etc/pacman.conf', 'r') as f:
    #        if not '[archlinuxfr]' in f.readlines():
    #            handle = subprocess.Popen(
    #                              'sudo echo "[archlinuxfr]" >/etc/pacman.conf',
    #                              shell=True).wait()
    #            handle = subprocess.Popen(
    #                    'sudo echo "Server = http://repo.archlinux.fr/%s" >'
    #                    ' /etc/pacman.conf' %
    #                    'i686' if architecture()[0] == '32bit' else 'x86_64',
    #                              shell=True).wait()
    #    self.update()
    #    self.install('yaourt')
