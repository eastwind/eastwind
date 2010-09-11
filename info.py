"""
information I/O library

This library deals with I/O of information between files and program.
"""

import json, re

class Prompt:
    def __init__(self, output_method = None):
        self.method = output_method

    def put(self, s):
        if(self.method == None):
            print s
        else:
            self.method(s)

    def error(self, s):
        self.put("\033[1;31m%s\033[0m" % s)

    def section(self, s):
        self.put("\033[1;33m%s\033[0m" % s)

    def log(self, s):
        self.put("%s" % s)

class Entry:
    def __init__(self):
        self.data = {}
        self.children = []
        self.file = None

    def from_json(self, j):
        for i in ['pre_install', 'ppa', 'post_install', 'install']:
            if i in j:
                self.data[i] = j[i]
        for i in j['children']:
            e = Entry()
            self.children.append(e)
            e.from_json(i)

    def to_obj(self):
        d = dict(self.data)
        d['children'] = []
        for c in self.children:
            d['children'].append(c.to_obj())
        return d

class Info:
    def __init__(self):
        self.info = []

    def read(self, file):
        json_file = open(file, "r")
        e = Entry()
        self.info.append(e)
        e.from_json(json.load(json_file))
        e.file = file
        print "    Loaded %s" % file

    def read_files(self, prefix, dir_list):
        for f in dir_list:
            if re.match("[^.]*.conf$", f) == None:
                continue
            self.read("%s%s" % (prefix, f))

    def write(self):
        for i in self.info:
            if i.file != None:
                with open(i.file, "w") as f:
                    json.dump(i.to_obj(), f, sort_keys=True, indent=4)

log = Prompt()

