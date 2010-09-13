#!/usr/bin/env python

'''
demonstration of the basic usage of pkgmanager
'''

from pkgmanager.manager import EastwindPkgManager

mgr = EastwindPkgManager()
mgr.install(['gummi-beta gummi'])
