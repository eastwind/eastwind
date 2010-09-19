"""
    Handler for eastwind package
"""
import utils
import os
import tarfile
from pkgmanager.manager import EastwindPkgManager
from configmanager.manager import EastwindConfigManager
from model import EastwindSet, EastwindAction

class EastwindPackage:
    """ Handles a eastwind package """

    def __init__(self, config, hash_key=''):
        """
            Initialize an EastwindPackage for install/dump
            config: a instance of EastwindSet
        """
        self.config = config
        if hash_key == '':
            self.hash = utils.hash_name(self.config.name)
        else:
            self.hash = hash_key
        self.base_path = utils.app_path(os.path.join('package', self.hash)))
        self.config_manager = EastwindConfigManager(self.base_path)
        self.pkg_manager = EastwindPkgManager()

    def extract(self, pkg_path):
        """
            Extracting an EastwindPackage and turn it to a instance
            pkg_path: path to EastwindPackage, will expanded to user path
        """
        tar = tarfile.open(os.path.expanduser(pkg_path), 'r:gz')
        hash_name = utils.hash_name(pkg_path)
        dest_dir = utils.app_path(os.path.join('package', hash_name))
        tar.extractall(dest_dir)
        tar.close()

        config_file = os.path.join(dest_dir, 'control')
        config = EastwindSet(config_file)
        return EastwindPackage(config, hash_name)
    extract = classmethod(extract)

    def unpack(self):
        """ Execute the actions in the package """
        for action in self.config.actions:
            self.__react(action.type, action.arg)

    def pack(self, pkg_path):
        """
            Dump a EastwindPackage to a single package
            pkg_path: path to the target .eastwind file
        """
        for action in self.config.actions:
            if action.type == 'config':
                self.config_manager.backup(action.arg)
        self.config.dump(os.path.join(self.base_path, 'control'))
        self.config_manager.dump()
        tar = tarfile.open(os.path.expanduser(pkg_path), 'w:gz')
        for item in os.listdir(self.base_path):
            tar.add(item)
        tar.close()

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
            self.config_manager.recover(arg)
        elif action == 'exec':
            os.system(arg)
        elif action == 'download':
            pass
        else:
            raise ValueError

