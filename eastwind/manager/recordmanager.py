"""
    Manager for record in CLI
"""

import eastwind.utils as utils
import eastwind.model as model
import os, sys

class _EastwindRecordManager:

    def __init__(self):
        self.current_file = None
        self.current_name = None
        if os.path.exists(utils.app_path('record_lock')):
            with open(utils.app_path('record_lock')) as f:
                self.current_name = r.read().rstrip()
            self.__generate_file()
            self.set = model.EastwindSet(self.current_file)

    def __generate_file(self):
        self.current_file = utils.app_path('record/%s' % self.current_name)

    def start(self, name):
        if self.current_name:
            # error handling...
            print >> sys.stderr, "There is a recording already."
            return
        with open(utils.app_path('record_lock')) as f:
            f.write(name)
        self.current_name = name
        self.__generate_file()

    def add(self, action):
        if not self.current_name:
            #TODO: maybe do something here?
            return
        self.set.actions.append(model.EastwindAction(action))
        self.set.dump()

    def stop(self):
        if not self.current_name:
            # error handling...
            print >> sys.stderr, "There is no record to be stopped."
            return
        os.remove(utils.app_path('record_lock'))

    def change(self, name):
        self.stop()
        self.start(name)

