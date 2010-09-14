"""
    Handler for eastwind package
"""

from pkgmanager.manager import EastwindPkgManager

class EastwindPackage:
    """ Handles a eastwind package """

    def __init__(self, config):
        """
            Initialize an EastwindPackage for install/dump
            config: a instance of EastwindSet
        """
        self.pkg_manager = EastwindPkgManager()
        self.config_manager = EastwindConfigManager()
        #TODO: EastwindConfigManager not implemented, or maybe this is not needed?
        self.config = config

    def extract(self, pkg_path):
        """
            Extracting an EastwindPackage and turn it to a instance
            pkg_path: path to EastwindPackage, will expanded to user path
        """
        pass
    extract = classmethod(extract)

    def install(self):
        """ Execute the actions in the package """
        for action in self.config.actions:
            self.__react(action.type, action.arg)

    def dump(self, pkg_path):
        """
            Dump a EastwindPackage to a single package
            pkg_path: path to the target .eastwind file
        """
        pass

    def __react(self, action, arg):
        """
            React to different operations
            action: atomic action name, ex: source, install ...
            args: argument(s) for each atomic actions
        """
        if action == 'source':
            self.pkg_manager.add_external_sources([arg])
        elif action == 'install':
            self.pkg_manager.install([arg])
        elif action == 'config':
            self.config_manager.recover([arg])
        elif action == 'exec':
            pass
        elif action == 'download':
            pass
        else:
            raise ValueError

