"""
    Handler for eastwind package
"""
import utils
import os.path
import tarfile
import subprocess
from manager import EastwindPkgManager, EastwindConfigManager
from model import EastwindSet, EastwindAction

class EastwindPackage:
    """ Handles a eastwind package """

    def __init__(self, config, hash_key=''):
        """
            Initialize an EastwindPackage for install/dump
            config: path to config file
        """
        self.config = EastwindSet(os.path.expanduser(config))
        if hash_key == '':
            self.hash = utils.hash_name(self.config.name)
        else:
            self.hash = hash_key
        self.base_path = utils.app_path(os.path.join('package', self.hash, ''))
        self.config_manager = EastwindConfigManager(self.base_path)
        self.pkg_manager = EastwindPkgManager()

    @classmethod
    def extract(self, pkg_path):
        """
            Extracting an EastwindPackage and turn it to a instance
            pkg_path: path to EastwindPackage, will expanded to user path
        """
        self.pkg_name = os.path.basename(pkg_path)
        tar = tarfile.open(os.path.expanduser(pkg_path), 'r:gz')
        hash_name = utils.hash_name(pkg_path)
        dest_dir = utils.app_path(os.path.join('package', hash_name))
        tar.extractall(dest_dir)
        tar.close()

        config_file = os.path.join(dest_dir, 'control')
        return EastwindPackage(config_file, hash_name)

    def unpack(self):
        """ Execute the actions in the package """
        action_friendly = {
            'source': 'Add external sources',
            'install': 'Install',
            'remove': 'Remove',
            'update': 'Update package list',
            'upgrade': 'Upgrade installed packages',
            'config': 'Add new configuration',
            'exec': 'Execute external command',
            'download': 'Download files'
        }
        print 'Package name: %s' % self.pkg_name
        print 'The following actions are going to be executed:'
        for action in self.config.actions:
            print '%s: %s' % (action_friendly[action.type], action.arg)

        print 'Do you want to proceed? [y/N]',
        try:
            res = raw_input()
        except KeyboardInterrupt:
            res = 'n'
        if 'n' in res.lower():
            print 'Aborted.'
            return

        total = len(self.config.actions)
        for index, action in enumerate(self.config.actions):
            utils.slog('INFO', 'Executing %d of %d actions ...' %
                       (index + 1, total))
            print '%s: %s' % (action.type, action.arg)
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
            tar.add(os.path.join(self.base_path, item), item)
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
        elif action == 'remove':
            self.pkg_manager.remove()
        elif action == 'update':
            self.pkg_manager.update()
        elif action == 'upgrade':
            self.pkg_manager.upgrade()
        elif action == 'config':
            self.config_manager.recover(arg)
        elif action == 'exec':
            subprocess.Popen(arg, shell=True).wait()
        elif action == 'download':
            pass
        else:
            raise ValueError

