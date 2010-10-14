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
                self.current_name = f.read().rstrip()
            self.current_file = utils.record_path(self.current_name)
            try:
                self.set = model.EastwindSet(self.current_file)
            except IOError:
                os.remove(utils.app_path('record_lock'))

    def start(self, name):
        if self.current_name:
            # error handling...
            print >> sys.stderr, "There is a recording already."
            return
        with open(utils.app_path('record_lock'), 'w') as f:
            f.write(name)
        self.current_name = name
        self.current_file = utils.record_path(self.current_name)
        if not os.path.exists(self.current_file):
            model.EastwindSet.touch(self.current_file, self.current_name)
        self.set = model.EastwindSet(self.current_file)

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
        self.current_name = None

    def change(self, name):
        self.stop()
        self.start(name)

