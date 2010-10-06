#!/usr/bin/env python

from distutils.core import setup
#from DistUtilsExtra.command import *

setup(
	name = 'eastwind',
	version = '0.1.2',
	description = 'Tool to make Ubuntu installation easier.',
	author = 'Andrew Liu',
	author_email = 'andrewliu33@gmail.com',
        url = 'http://github.com/eastwind/eastwind',
	license = 'GPL',
    	packages = ['eastwind', 'eastwind.pkgmanager', 'eastwind.configmanager'],
	scripts = ['bin/ew'],
        #cmdclass = { "build": build_extra.build_extra,
        #             "build_i18n": build_i18n.build_i18n }
)
