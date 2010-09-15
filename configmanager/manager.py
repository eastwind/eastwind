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

    def __init__(self, orig_path, backup_path):
        self.orig_path = orig_path
        self.backup_path = backup_path

    def backup(file, version):
        """ Backup the files to destination. """
        path = os.path.expanduser(file)
        if os.path.exists(path) == False:
            raise NotFoundError(path)
        # Tar the target into a single file
        filename = backup_path(path, version)
        os.system("cd %s && tar -jpc -f %s ./%s" % (
           os.path.split(os.path.abspath(path))[0],\
           os.path.abspath(filename),\
           os.path.split(os.path.abspath(path))[1] )
        )
        return filename

    def recover(file, dest):
        """ Copy the backed file to that path. """
        file = os.path.abspath(file)
        dest = os.path.expanduser(dest)

        if os.path.exists(file) == False:
            raise NotFoundError(file)
        if os.path.exists(dest) == False:
            os.makedirs(os.path.expanduser(dest))

        os.system("tar -xjp -f %s -C %s" % (file, os.path.split(dest)[0]))

    def __hash(self, path):
        return hashlib.sha1("%s-%f" % (path, time.time())).hexdigest()

