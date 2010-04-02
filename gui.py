#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class EastWind:

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("EastWind")
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        table = gtk.Table(15,15,True)
        self.window.add(table)

        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0,15,0,14)
        notebook.show()
        table.show()
        self.show_tabs = True
        self.show_border = True

        table_list = ["install", "Backup", "recover"]
        for i in table_list:
            frame = gtk.Frame(i)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            #label = gtk.Label(i)
            #frame.add(label)
            #label.show()

            label = gtk.Label(i)
            notebook.append_page(frame, label)


        button = gtk.Button(stock=gtk.STOCK_QUIT)
        button.connect("clicked", lambda w: gtk.main_quit())
        table.attach(button, 14, 15, 14, 15)
        button.show()

        button = gtk.Button("GO!")
        table.attach(button, 13, 14, 14, 15)
        button.show()
            
#        self.window.add(table)
        self.window.show()
        self.show_tabs=True
        
    def main(self):
        gtk.main()

if __name__ == "__main__": # if this file is included then no gui.
    hello = EastWind()
    hello.main()
