"""
information I/O library

This library deals with I/O of information between files and program.
"""

import ConfigParser, re

class Info:
    parsers = {}
    info = {}

    def read(self, file):
        config = ConfigParser.ConfigParser()
        config.read(file)
        for i in config.sections():
            for j in config.items(i):
                if j[0] in self.info:
                    self.info[j[0]].append(j[1])
                else:
                    self.info[j[0]] = [j[1]]
        print "    Loaded %s" % file
        self.parsers[file] = config

    def read_files(self, prefix, dir_list):
        for f in dir_list:
            if re.match("[^.]*.conf$", f) == None:
                continue
            self.read("%s%s" % (prefix, f))

    def new_parser(self, file):
        c = ConfigParser.ConfigParser()
        self.parsers[file] = c
        return c

    def write(self):
        for f,p in self.parsers.items():
            with open(f, 'wb') as configfile:
                p.write(configfile)

