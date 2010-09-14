#!/usr/bin/env python

'''
demonstration of the basic usage of pkgmanager
'''

from pkgmanager.manager import EastwindPkgManager

mgr = EastwindPkgManager()
mgr.add_external_sources(['ppa:gummi/gummi-nightly', 'ppa:gummi/gummi'])
mgr.install(['gummi-beta gummi'])

