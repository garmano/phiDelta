#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:43:23 2018

@author: giuliano
"""


from utils import conditional_eval, strip_multiple


# -----------------------------------------------------------------------------
# ------------------------ DATASET --------------------------------------------
# -----------------------------------------------------------------------------

class datainfo(object):
  
  "Dataset information"
  
  __defaults__ = { 'name': (str,''), 'description': (str,''),
                   'sep': (str,','), 'index': (int,-1), 'header': (bool,True), 
                   'filename': (str,''), 'ext': (str,'csv'),
                   'classes': (tuple,('1','0')), 'fnames': (list,[]) }

  __slots__ = tuple([slot for slot in __defaults__ ])
                   
  __dict__  = property(lambda sf: { s : getattr(sf,s) for s in sf.__slots__ })

# --------------------- PUBLIC SECTION ----------------------------------------
 
  def __init__(self,**kwargs):
    "Init a dataset using keyworded parameters and default values"
    for slot, (stype, default) in self.__defaults__.items():
      setattr(self,slot,kwargs.get(slot,default))
    if not kwargs: return # Allow instance creation with defaults only ...
    name, filename, ext = self.name, self.filename, self.ext
    assert name or filename, "Dataset name or filename must be specified!"
    if not filename: filename = name if type(name) == str else name[0]
    if not name: name = filename
    if filename.find('.') == -1: filename = filename + '.' + ext
    self.name, self.filename = name, filename

  def __getitem__(self,key): return getattr(self,key,None)

  def __setitem__(self,key,value): return setattr(self,key,value)

  def __lshift__(self,textinfo):
    "Init a dataset using a text content"
    if textinfo: self.__init__(**self.parse_slots(textinfo))
    return self
  
  def check_class(self,c):
    assert self.classes, "Dataset does not contain information on classes ..."
    pcat, ncat = self.classes
    return c in pcat if type(pcat) in [list,tuple] else c == pcat
  
  def display(self,comment='',verbose=False):
    print()
    if comment: print(comment)
    print("Name: {}".format(self.name))
    if verbose: print("Description: {}".format(self.description))
    print("Classes: {}".format(self.classes))
    if verbose: print("Class index: {}".format(self.index))
    if verbose: print("Header: {}".format(self.header))
    print("File name: {}".format(self.filename))
    if verbose: print("File extension : {}".format(self.ext))
    if len(self.fnames) == 0: return
    sfnames = " ,".join(self.fnames)
    if len(sfnames) > 80: sfnames = sfnames[:80] + " ..."
    print("Feature names: {}".format(sfnames))
    print("Number of features: {}".format(len(self.fnames)))

# --------------------- PRIVATE SECTION ---------------------------------------

  def parse_slots(self,textinfo):
    kwargs = dict()
    void, name = textinfo[0].split()
    kwargs['name'] = eval(name.strip())
    for line in textinfo[1:]:
      slot, value = self.parse_slot(line)
      if slot in self.__slots__: kwargs[slot] = value
    return kwargs
  
  def parse_slot(self,line):
    slot, value = line.split('=')
    slot, value = strip_multiple(slot,value)
    if not slot in self.__slots__: return None, None # Not a valid slot
    stype, default = self.__defaults__[slot]
    value = conditional_eval(value,stype)
    return slot, value
    

# -----------------------------------------------------------------------------
# ------------------------ MAIN PROGRAM (for testing) -------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':

  UCIpath = '../datasets/UCI datasets/'
  
  textdata  = [ "@dataset ('lymphography',2)",
                "  description = 'Lymphography dataset'",
                "    header   = True",
                "    classes  = 'normal', ('metastases','malign_lymph','fibrosis')",
                "    filename = 'lymphography'",
                "    ext      = 'dat'" ]

  D1 = datainfo() << textdata

  D1.display(verbose=True)

  D2 = datainfo(name=('lymphography',2), header = True,
                classes = ('normal', ('metastases','malign_lymph','fibrosis')),
                ext = 'dat')

  D2.display(verbose=True)
  
# -----------------------------------------------------------------------------
