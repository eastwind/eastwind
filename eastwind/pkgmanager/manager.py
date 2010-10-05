'''
Eastwind Package Management Interface
'''

import platform

from apt_series import EastwindPkgMangerAPT
from yum_series import EastwindPkgMangerYUM

class EastwindPkgManager:
    def __init__(self):
        '''
        Guess the target package management system and assign a agent to it
        '''
        # set to APT for now
        self.agent = EastwindPkgMangerAPT()

    def update(self):
        '''
        Update package list
        '''
        print 'Updating package list...'
        return self.agent.update()

    def upgrade(self):
        '''
        Upgrade packages
        '''
        print 'Upgrading packages...'
        return self.agent.upgrade()

    def install(self, pkgs):
        '''
        Install packages
        pkgs: a list containning packages to install
        '''
        print 'Installing %s...' % (' '.join(pkgs))
        return self.agent.install(pkgs)

    def install_interactive(self, pkgs):
        '''
        Install interactively
        pkgs: a list containning packages to install, pkgs will be add to
              Eastwind database for further manipulation
        '''
        return self.agent.install_interactive(pkgs)

    def purge(self, pkgs):
        '''
        Remove pkgs
        pkgs: a list containning packages to remove, also remove package
              configurations
        '''
        print 'Purging %s...' % (' '.join(pkgs))
        return self.agent.purge(pkgs)

    def purge_interactive(self, pkgs):
        '''
        Purge interactively
        pkgs: a list containning packages to install, pkgs will be remove from
              Eastwind database
        '''
        return self.agent.purge_interactive(pkgs)

    def add_external_sources(self, sources):
        '''
        Add external sources like PPA for Debian or AUR for Arch
        sources: a list of sources to add
        '''
        print 'Adding external sources: %s' % sources
        return self.agent.add_external_sources(sources)
