"""
    Singleton classes
"""
import pkgmanager
from configmanager import EastwindConfigManager
from recordmanager import EastwindRecordManager

class EastwindPkgManager:
    singleton = pkgmanager._EastwindPkgManager()
    def __init__(self):
        self.__dict__ = EastwindPkgManager.singleton.__dict__
        self.__class__ = EastwindPkgManager.singleton.__class__

class EastwindPkgManager:
    singleton = pkgmanager._EastwindPkgManager()
    def __init__(self):
        self.__dict__ = EastwindPkgManager.singleton.__dict__
        self.__class__ = EastwindPkgManager.singleton.__class__

