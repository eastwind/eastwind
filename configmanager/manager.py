"""
    Config backup manager
"""

import hashlib
import time

class NotFoundError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EastwindConfigManager:
    """ Manager for config backup/recover """

    def __init__(self):
        pass

    def backup(self, orig_path):
        """ Backup the files to destination. """
        pass

    def recover(file, dest):
        """ Copy the backed file to that path. """
        pass

    def __generate_backup_path(self, path):
        self.backup_path = hashlib.sha1("%s-%f" % (path, time.time())).hexdigest()

