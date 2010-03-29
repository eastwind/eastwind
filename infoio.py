"""
information I/O library

This library deals with I/O of information between files and program.
"""
#!/usr/bin/env python

import json

class JsonInfo:
   """
This class read information from an json file. 
   """
   file = None
   info = None
   Apps = None
   def __inti__( self , _file = None ):
      self.file = _file
      if self.file != None:
         self.read()

   def read( self , _file = None ):
      if _file != None:
         self.file = _file

      if self.file == None:
         self.info = None
         self.Apps = None
         raise RuntimeError( 'You didn\'t specify a file.' )
      else:
         tmpfile = open( self.file , "r" )
         self.info = json.load(tmpfile)
         if self.info["Apps"] != None:
            #make a short cut for self.info["Apps"]
            self.Apps = self.info["Apps"]
            
         tmpfile.close()

   def write( self , _file = None ):
      if _file != None:
         self.file = _file

      if self.file == None:
         raise RuntimeError( 'You didn\'t specify a file.' )
      else:
         tmpfile = open( self.file , "w" )
         json.dump(self.info,tmpfile,sort_keys=True,indent=4)
         tmpfile.close()

