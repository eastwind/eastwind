#!/usr/bin/env python

import xml.dom.minidom
from xml.dom.minidom import Node

class App:
   """
This class is used for storage information of Applications

There are two class members:
   str self.name
   str self.ppa
   """
   def __init__( self , _name , _ppa ):
      self.name = _name
      self.ppa  = _ppa

class List:
   """
This class is used to read in a xml files 

class member:
   self.list
      a list of Applications
   self.file
      a string indicate the file name of xml file.
class method:
   self.makeList
      this method is used to read in an xml file and 
      storage the information in self.list.
   """
   def __init__( self , _filename=None ):
      self.list = []
      if _filename != None:
         self.file = _filename
         self.makeList()
      else:
         self.file = None

   def makeList( self , _filename=None ):
      if _filename != None :
         self.file = _filename

      if self.file == None :
         raise RuntimeError('self.file should not be "None"')
         self.list = []
      else:
         doc = xml.dom.minidom.parse(self.file)
         for node in doc.getElementsByTagName("App"):
            name = node.getAttribute("name")
            ppa  = node.getAttribute("ppa")
            self.list.append( App( name , ppa ) )

         return self.list


