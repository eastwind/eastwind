"""
    Singleton classes
"""
import pkgmanager
import recordmanager
from configmanager import EastwindConfigManager

class EastwindPkgManager:
    singleton = pkgmanager._EastwindPkgManager()
    def __init__(self):
        self.__dict__ = EastwindPkgManager.singleton.__dict__
        self.__class__ = EastwindPkgManager.singleton.__class__

class EastwindRecordManager:
    singleton = recordmanager._EastwindRecordManager()
    def __init__(self):
        self.__dict__ = EastwindRecordManager.singleton.__dict__
        self.__class__ = EastwindRecordManager.singleton.__class__

