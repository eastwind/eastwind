#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk, gobject, os, re
from info import *
from eastwind import *

class InfoModel:
    """ The model class holds the information we want to display """

    info = None

    def __init__(self, mode):
        """ Sets up and populates our gtk.TreeStore """
        self.tree_store = gtk.TreeStore( gobject.TYPE_STRING,
                                         gobject.TYPE_BOOLEAN )
        # places the global people data into the list
        # we form a simple tree.
        self.info = EastWind()
        if mode == "recover":
            dirs = self.info.load_recover()
            for d in dirs:
                conf = Info()
                conf.read("backup/%s/backup.conf" % d)
                parent = self.tree_store.append(None, (d, None))
                for s,t in conf.info.items():
                    self.tree_store.append(parent, (s, None))
        else:
            self.info.load()
            for n,p in self.info.data.parsers.items():
                parent = self.tree_store.append(None, (n, None))
                for s in p.sections():
                    subparent = self.tree_store.append(parent, (s, None))
                    for i in p.items(s):
                        if i[0] == mode:
                            self.tree_store.append(subparent, (i[1], None))
        return

    def get_model(self):
        """ Returns the model """
        if self.tree_store:
            return self.tree_store
        else:
            return None

class DisplayModel:
    """ Displays the Info_Model model in a view """
    def make_view( self, model ):
        """ Form a view for the Tree Model """
        self.view = gtk.TreeView( model )
        # setup the text cell renderer and allows these
        # cells to be edited.
        self.renderer = gtk.CellRendererText()
        self.renderer.set_property( 'editable', False )
        #self.renderer.connect( 'edited', self.col0_edited_cb, model )

        # The toggle cellrenderer is setup and we allow it to be
        # changed (toggled) by the user.
        self.renderer1 = gtk.CellRendererToggle()
        self.renderer1.set_property('activatable', True)
        self.renderer1.connect( 'toggled', self.col1_toggled_cb, model )
        # a column for some information about the option.
        self.renderer2 = gtk.CellRendererText()
        self.renderer2.set_property( 'editable', False)
        # Connect column0 of the display with column 0 in our list model
        # The renderer will then display whatever is in column 0 of
        # our model .
        self.column0 = gtk.TreeViewColumn("Name", self.renderer, text=0)

        # The columns active state is attached to the second column
        # in the model.  So when the model says True then the button
        # will show as active e.g on.
        self.column1 = gtk.TreeViewColumn("Select", self.renderer1 )
        self.column1.add_attribute( self.renderer1, "active", 1)

        self.column2 = gtk.TreeViewColumn("Information", self.renderer2)


        self.view.append_column( self.column0 )
        self.view.append_column( self.column2 )
        self.view.append_column( self.column1 )
        return self.view

    #def col0_edited_cb( self, cell, path, new_text, model ):
        """
        Called when a text cell is edited.  It puts the new text
        in the model so that it is displayed properly.
        """
        #print "Change '%s' to '%s'" % (model[path][0], new_text)
     #   model[path][0] = new_text
     #   return
    def col1_toggled_cb( self, cell, path, model ):
        """
        Sets the toggled state on the toggle button to true or false.
        """
        model[path][1] = not model[path][1]
        '''toggle children too '''
        iter = model.get_iter(path)
        for i in range(model.iter_n_children(iter)):
            model.set_value(model.iter_nth_child(iter,i), 1,model[path][1])
        #print "Toggle '%s' to: %s" % (model[path][0], model[path][1],)
        return

class EastWindGui:
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

        ''' functions for making widget'''

    def make_button(self,table):
        button = gtk.Button(stock=gtk.STOCK_QUIT)
        button.connect("clicked", lambda w: gtk.main_quit())
        button.set_size_request(70,35)
        table.attach(button, 14, 15, 14, 15,gtk.FILL,
            gtk.SHRINK, 1, 1)
        button.show()
        ''' make GO button'''
        button = gtk.Button("GO!")
        button.set_size_request(70,35)
        table.attach(button, 13, 14, 14, 15,gtk.FILL,
            gtk.SHRINK, 1, 1)
        button.show()

        #tabs
    def make_notebook(self,table):
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.set_size_request(400,400)
       
        table.attach(notebook, 0,15,0,14)
       
        notebook.show()
        table.show()
        self.show_tabs = True
        self.show_border = True

        store_list = ["install", "backup", "recover"]

        for i in store_list:
            #CellRendererText
            # Get the model and attach it to the view
            self.mdl = InfoModel(i).get_model()
            self.view = Display.make_view( self.mdl )
            # Add our view into the main window

            frame = gtk.Frame(i)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            vbox = gtk.VBox(False ,5)
            hbox = gtk.HBox(True ,3)
            valign = gtk.Alignment(0,1,0,0)
            vbox.pack_start(valign)
            vbox.pack_start(self.view)
            halign = gtk.Alignment(1,0,0,0)
            halign.add(hbox)
            vbox.pack_start(halign,False,False,3)
            
            add = gtk.Button("add")
            delete = gtk.Button("delete")
#            vbox.pack_start(hbox)
            hbox.pack_start(add)
            hbox.pack_start(delete)
            add.show()
            delete.show()
            hbox.show()
            vbox.show()
            halign.show()
            #table.attach(notebook, 0,13,0,14)
#            table.attach(vbox, 0,15,0,13)

            '''label on notbook tab'''
            label = gtk.Label(i.title())
            
            notebook.append_page(vbox, label)
            notebook.show()
            self.view.show()
            '''
            The explanation area on the right of the window.
            TODO: should use something other than textview.
            '''
    def make_explanation(self,table):
        wins = gtk.TextView()
        wins.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(5140, 5140, 5140))
        wins.set_cursor_visible(False)
        table.attach(wins, 13, 15, 0, 14,
            gtk.FILL | gtk.EXPAND,gtk.FILL | gtk.EXPAND, 1, 1)
        wins.show()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("EastWind")
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        #makeing table to put widgets
        table = gtk.Table(15,15,False)
        table.set_col_spacings(3)
        self.window.add(table)

        self.make_notebook(table)
        self.make_button(table)
        #self.make_explanation(table)

        self.window.show()
        self.show_tabs=True

    def main(self):
        gtk.main()

if __name__ == "__main__": # if this file is included then no gui.
    Display = DisplayModel()
    e = EastWindGui()
    e.main()

