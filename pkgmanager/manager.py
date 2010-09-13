'''
Eastwind Package Management Interface
'''

from apt_series import EastwindPkgMangerAPT
#from rpm_series import EastwindPkgMangerRPM

class EastwindPkgManager:
    def __init__(self):
        '''
        Guess the target package management system and assign a agent to it
        '''
        self.agent = EastwindPkgMangerAPT()

    def update(self):
        '''
        Update package list
        '''
        print 'Updating package list...'
        self.agent.update()

    def upgrade(self):
        '''
        Upgrade packages
        '''
        print 'Upgrading packages...'
        self.agent.upgrade()

    def install(self, pkgs):
        '''
        Install packages
        pkgs: a list containning packages to install
        '''
        print 'Installing %s...' % (' '.join(pkgs))
        self.agent.install(pkgs)

    def install_interactive(self, pkgs):
        '''
        Install interactively
        pkgs: a list containning packages to install, pkgs will be add to
              Eastwind database for further manipulation
        '''
        self.agent.install_interactive(pkgs)

    def purge(self, pkgs):
        '''
        Remove pkgs
        pkgs: a list containning packages to remove, also remove package
              configurations
        '''
        print 'Purging %s...' % (' '.join(pkgs))
        self.agent.purge(pkgs)
