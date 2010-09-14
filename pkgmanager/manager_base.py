'''
Eastwind Package Management Interface Base class
'''

class EastwindPkgMangerSkeleton:
    def update(self):
        raise NotImplementedError

    def upgrade(self):
        raise NotImplementedError

    def install(self, pkgs):
        raise NotImplementedError

    def install_interactive(self, pkgs):
        # TODO: Add pkgs to Eastwind database
        raise NotImplementedError

    def purge(self, pkgs):
        raise NotImplementedError

    def add_external_sources(self, args):
        raise NotImplementedError
