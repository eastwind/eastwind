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
        self.install_tmp = None
        self.backup_tmp = None
        self.recover_tmp = None
        self.info = EastWind()
        self.info.load()
        self.builder = gtk.Builder()
        #self.builder  = gtk.Builder()
        self.builder.add_from_file("window.glade")
        #self.builder.add_from_file("builder.glade")
        self.builder.connect_signals({
            "window_destroy": self.destroy,
            #"addSwitchPage" : self.addSwitchPage,
            "show_add_notebook": self.toggle_add_notebook
        })
        #self.builder.connect_signals({
            #"closebuilder": self.closebuilder,

            #"netGetClick"   : self.netGetClick
        #})
        self.builder.get_object('ok').connect('clicked', self.go)

        self.builder.get_object('install_cell_toggle').connect( 'toggled', self.toggled, self.builder.get_object('install_treestore'))
        self.builder.get_object('backup_cell_toggle').connect( 'toggled', self.toggled, self.builder.get_object('backup_treestore'))
        self.builder.get_object('recover_cell_toggle').connect( 'toggled', self.toggled, self.builder.get_object('recover_treestore'))
        self.builder.get_object('new_add_button').connect( 'clicked' , self.new_add_clicked ) ;
        self.install_model()
        self.backup_model()
        self.recover_model()
        self.type_list_model()
        self.window = self.builder.get_object("EastWind")
        #self.builder = self.builder.get_object("builder")
        self.add_notebook = self.builder.get_object('add_notebook')
        self.window.show_all()
        self.add_notebook.hide_all()

    def type_list_model(self):
        self.type_list = self.builder.get_object("type_list")
        self.type_list.append( ["Install"] )
        self.type_list.append( ["Backup"] )
        self.type_list.append( ["Recover"] )

    #def addSwitchPage(self, notebook , page , page_num ):
    #    print page_num
    def new_add_clicked( self , data ):
        combo = self.builder.get_object("type_combo_box").get_active()
        if combo == 0: #type == install
            self.add_install( self.builder.get_object("value_text").get_text())
        if combo == 1: #type == backup
            self.add_backup( self.builder.get_object("value_text").get_text())
        if combo == 2: #type == recover
            self.add_recover( self.builder.get_object("value_text").get_text())

    #def netGetClick( self, button ):
    #    print "%s is clicked!" % button.get_label()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def toggle_add_notebook( self, button ):
        if self.add_notebook.get_property('visible') == True:
            self.add_notebook.hide_all()
        else:
            self.add_notebook.show_all()
        self.builder.get_object("value_text").set_text("")
        self.builder.get_object("type_combo_box").set_active(-1)
        self.add_notebook.set_current_page(0)
        # set_current_page must after show_all, I don't know why...

    def add_install( self , text ):
        if self.install_tmp == None :
            self.install_tmp = self.install_tree.append(None,( "This time only" , None ))
        self.install_tree.append( self.install_tmp , (text,None)) ;

    def add_backup( self , text ):
        if self.backup_tmp == none :
            self.backup_tmp = self.backup_tree.append(None,( "This time only" , None ))
        self.backup_tree.append( self.backup_tmp , (text,None)) ;

    def add_recover( self , text ):
        if self.recover_tmp == None :
            self.recover_tmp = self.recover_tree.append(None,( "This time only" , None ))
        self.recover_tree.append( self.recover_tmp , (text,None)) ;

    def install_model(self):
        self.install_tree = self.builder.get_object("install_treestore")
        for n,p in self.info.data.parsers.items():
            parent = self.install_tree.append(None, (n, None))
            for s in p.sections():
                subparent = self.install_tree.append(parent, (s, None))
                for i in p.items(s):
                    if i[0] == 'install':
                        for t in i[1].split(' '):
                            self.install_tree.append(subparent, (t, None))

    def backup_model(self):
        self.backup_tree = self.builder.get_object("backup_treestore")
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
        self.recover_tree = self.builder.get_object("recover_treestore")
        for d in dirs:
            conf = Info()
            conf.read("backup/%s/backup.conf" % d)
            parent = self.recover_tree.append(None, (d, None, None))
            for s,t in conf.info.items():
                self.recover_tree.append(parent, (s, None, t[0]))

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

    def go(self, data):
        for mode in ['install', 'backup', 'recover']:
            self.info.data.info[mode] = []
            self.builder.get_object('%s_treestore' % mode).foreach(self.add_list, mode)
        self.terminal_exec([self.info.install])
        # FIXME: backup and recover are needed
        # TODO: add the pre/post install action

    def add_list(self, model, path, iter, mode):
        if mode == "recover" and model.iter_depth(iter) == 1 and model.get_value(iter, 1) == True:
            self.info.data.info[mode].append([model.get_value(iter, 0), model.get_value(iter, 2)])
        elif model.iter_depth(iter) == 2 and model.get_value(iter, 1) == True:
            self.info.data.info[mode].append(model.get_value(iter, 0))

    def terminal_exec(self, funcs):
        self.term = vte.Terminal()
        self.termwin = gtk.Window()
        #TODO: make the window uncloasable
        self.termwin.add(self.term)
        self.termwin.show_all()
        #FIXME: do something with sudo
        #self.info.cmd = lambda x: self.term.fork_command(x.split(' ')[0], ['']+x.split(' ')[1:])
        self.info.cmd = self.fork_cmd
        log.method = lambda x: self.term.feed("%s\n\r" % x)
        #self.term.feed( "ls\n" )
        for i in funcs:
            i()
        #TODO: do something when finish

    def fork_cmd(self,x):
        print x
        self.term.fork_command(x.split(' ')[0], ['']+x.split(' ')[1:])


if __name__ == '__main__':
    e = EastWindGUI()
    gtk.main()

