"""
    Handler for eastwind atomic actions.
"""

from pkgmanager.manager import EastwindPkgManager

class EastwindHandler:
    """ Handler logic for actions """
    #TODO: maybe this should be a singleton

    def __init__(self):
        self.pkg_manager = EastwindPkgManager()

    def react(self, action, arg):
        """
            React to different operations
            action: atomic action name, ex: source, install ...
            args: argument(s) for each atomic actions
        """
        if action == 'source':
            pass
        elif action == 'install':
            self.pkg_manager.install([arg])
        elif action == 'config':
            pass
        elif action == 'exec':
            pass
        elif action == 'download':
            pass
        else:
            raise ValueError

