"""
    Handler for eastwind atomic actions.
"""

from pkgmanager.manager import EastwindPkgManager

class EastwindHandler:
    """ Handler logic for actions """
    #TODO: maybe this should be a singleton

    def __init__(self):
        self.manager = EastwindPkgManager()

    def react(self, action, arg):
        if action == 'source':
            pass
        elif action == 'install':
            pass
        elif action == 'config':
            pass
        elif action == 'exec':
            pass
        elif action == 'download':
            pass
        else:
            raise NoActionError

