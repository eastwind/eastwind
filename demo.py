#!/usr/bin/env python

'''
deeonstration of the basic usage of pkgmanager
'''

from pkgmanager.manager import EastwindPkgManager

mgr = EastwindPkgManager()
mgr.install(['gummi-beta gummi'])
