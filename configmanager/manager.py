"""
    Config backup manager
"""

import utils
import os
import json
import tarfile

class EastwindConfigManager:
    """ Manager for config backup/recover """

    def __init__(self, backup_path):
        self.backup_path = backup_path
        self.config = os.path.join(self.backup_path, 'backup')
        self.dir_hash = {}

    def backup(self, orig_path):
        """ Backup the files to destination. """
        hashed_file = utils.hash_name(orig_path)
        backup_path = os.path.join(self.backup_path, hashed_file)
        tar_file = tarfile.open(backup_path, 'w:gz')
        tar_name = os.path.basename(os.path.normpath(orig_path))
        tar_file.add(os.path.expanduser(orig_path), tar_name)
        tar_file.close()
        # mapping original path to hashed file
        self.dir_hash[orig_path] = hashed_file

    def recover(self, orig_path):
        """ Copy the backed file to that path. """
        with open(self.config, 'r') as f:
            self.dir_hash = json.load(f)
            hashed_file = self.dir_hash[orig_path]
            recover_path = os.path.dirname(os.path.normpath(orig_path))
            from_path = os.path.join(self.backup_path, hashed_file)
            tar_file = tarfile.open(from_path, 'r:gz')
            tar_file.extractall(os.path.expanduser(recover_path))
            tar_file.close()

    def dump(self):
        """ Dump the hash => path info to a json """
        with open(self.config, "w") as f:
            json.dump(self.dir_hash, f, sort_keys=True, indent=4)

