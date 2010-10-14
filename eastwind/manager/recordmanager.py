"""
    Manager for record in CLI
"""

import eastwind.utils as utils
import os

class _EastwindRecordManager:

    def __init__(self):
        self.current_file = None
        self.current_name = None
        if os.path.exists(utils.app_path('record_lock')):
            with open(utils.app_path('record_lock') as f:
                self.current_name = r.read().rstrip()
            self.current_file = utils.app_path('record/%s' % self.current_name)
            #TODO: need to load file here
            self.set = None

    def start(self, name):
        if self.current_name:
            # error handling...
            print >> stderr, "There is a recording already."
            return
        with open(utils.app_path('record_lock') as f:
            f.write(name)
        #TODO: use model to generate a file

    def add(self, action):
        pass

    def stop(self):
        if not self.current_name:
            # error handling...
            print >> stderr, "There is no record to be stopped."
            return
        #TODO: delete record_lock file

