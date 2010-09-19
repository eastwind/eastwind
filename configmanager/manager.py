"""
    Config backup manager
"""

import utils
import os
import shutil

class EastwindConfigManager:
    """ Manager for config backup/recover """

    def __init__(self, backup_path):
        self.backup_path = backup_path
        self.config = os.path.join(self.backup_path, 'backup')
        self.dir_hash = {}
        self.path_hash = {}

    def backup(self, orig_path):
        """ Backup the files to destination. """
        hashed_folder = utils.hash_name(orig_path)
        dest_path = os.path.join(self.backup_path, hashed_folder)
        try:
            os.mkdir(dest_path)
        except OSError: pass

        if os.path.isdir(orig_path):
            folder = os.path.basename(os.path.normpath(orig_path))
            dest_dir = os.path.join(dest_path, folder)
            shutil.copytree(orig_path, dest_dir)
        else:
            shutil.copy2(orig_path, dest_path)
        #TODO: may raise error when orig_path not available

        self.dir_hash[hashed_folder] = os.path.dirname(os.path.normpath(orig_path))
        self.path_hash[orig_path] = hashed_folder

    def recover(self, orig_path):
        """ Copy the backed file to that path. """
        with open(self.config, 'r') as f:
            self.dir_hash, self.path_hash = json.load(f)
            #TODO: recover self.path_hash[orig_path] to self.dir_hash[self.path_hash[orig_path]]

    def dump(self):
        """ Dump the hash => path info to a json """
        with open(self.config, "w") as f:
            json.dump([self.dir_hash, self.path_hash], f, sort_keys=True, indent=4)

