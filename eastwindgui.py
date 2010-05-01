#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Eastwind GUI with glade.
"""

import gtk, vte
from eastwind import *
from info import *

class EastWindGUI:
    def __init__(self):
        self.info = EastWind()
        self.info.load()
        self.builder = gtk.Builder()
        #self.builder  = gtk.Builder()
        self.builder.add_from_file("window.glade")
        #self.builder.add_from_file("builder.glade")
        self.builder.connect_signals({
            "window-destroy": self.destroy,
            #"addSwitchPage" : self.addSwitchPage,
            "showAddWindow": self.toggle_install_notebook
        })
        #self.builder.connect_signals({
            #"closebuilder": self.closebuilder,

            #"netGetClick"   : self.netGetClick
        #})

        self.builder.get_object('install-cell-toggle').connect( 'toggled', self.toggled, self.builder.get_object('install-treestore'))
        self.builder.get_object('backup-cell-toggle').connect( 'toggled', self.toggled, self.builder.get_object('backup-treestore'))
        self.builder.get_object('recover-cell-toggle').connect( 'toggled', self.toggled, self.builder.get_object('recover-treestore'))
        self.install_model()
        self.backup_model()
        self.recover_model()
        self.typeList_model()
        self.window = self.builder.get_object("EastWind")
        #self.builder = self.builder.get_object("builder")
        self.install_notebook = self.builder.get_object('install-add-notebook')
        self.window.show_all()
        self.install_notebook.hide_all()

    def typeList_model(self):
        self.typeList = self.builder.get_object("typeList")
        self.typeList.append( ["Install"] )
        self.typeList.append( ["Backup"] )
        self.typeList.append( ["Recovery"] )

    #def addSwitchPage(self, notebook , page , page_num ):
    #    print page_num

    #def netGetClick( self, button ):
    #    print "%s is clicked!" % button.get_label()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def toggle_install_notebook( self, widget , data = None ):
        if self.install_notebook.get_property('visible') == True:
            self.install_notebook.hide_all()
        else:
            self.install_notebook.show_all()
        self.builder.get_object("valueText").set_text("")
        self.builder.get_object("typeComboBox").set_active(-1)
        self.install_notebook.set_current_page(0)
        # set_current_page must after show_all, I don't know why...

    def install_model(self):
        self.install_tree = self.builder.get_object("install-treestore")
        for n,p in self.info.data.parsers.items():
            parent = self.install_tree.append(None, (n, None))
            for s in p.sections():
                subparent = self.install_tree.append(parent, (s, None))
                for i in p.items(s):
                    if i[0] == 'install':
                        for t in i[1].split(' '):
                            self.install_tree.append(subparent, (t, None))

    def backup_model(self):
        self.backup_tree = self.builder.get_object("backup-treestore")
        for n,p in self.info.data.parsers.items():
            parent = self.backup_tree.append(None, (n, None))
            for s in p.sections():
                subparent = self.backup_tree.append(parent, (s, None))
                for i in p.items(s):
                    if i[0] == 'backup':
                        for t in i[1].split(' '):
                            self.backup_tree.append(subparent, (t, None))

    def recover_model(self):
        dirs = self.info.load_recover()
        self.recover_tree = self.builder.get_object("recover-treestore")
        for d in dirs:
            conf = Info()
            conf.read("backup/%s/backup.conf" % d)
            parent = self.recover_tree.append(None, (d, None))
            for s,t in conf.info.items():
                self.recover_tree.append(parent, (s, None))

    def toggled( self, cell, path, model ):
        """ Sets the toggled state on the toggle button to true or false. """
        model[path][1] = not model[path][1]
        # toggle children too
        iter = model.get_iter(path)
        self.toggle_recursive(model, iter, model[path][1])
        return

    def toggle_recursive(self, model, iter, value):
        model.set_value(iter, 1, value)
        if model.iter_n_children(iter) != 0:
            for i in range(model.iter_n_children(iter)):
                self.toggle_recursive(model, model.iter_nth_child(iter, i), value)

    def terminal_exec(self, funcs):
        self.term = vte.Terminal()
        self.termwin = gtk.Window()
        #TODO: make the window uncloasable
        self.termwin.add(self.term)
        self.termwin.show_all()

        self.info.cmd = self.term.fork_command
        self.info.log.method = self.term.feed
        #FIXME: not sure here
        for i in funcs:
            i()

if __name__ == '__main__':
    e = EastWindGUI()
    gtk.main()

