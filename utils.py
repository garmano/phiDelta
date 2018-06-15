# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:36:08 2018

@author: armano
"""


import numpy as np



# -----------------------------------------------------------------------------
# ------------------------ FILES R/W ------------------------------------------
# -----------------------------------------------------------------------------

def load_csv_data(filename, path='',sep=','):
  print("Loading file {} ...".format(path+filename))
  with open(path+filename) as infile:
    return [ line.strip().split(sep) for line in infile ]
    
def save_csv_data(content, filename, path='',sep=','):
  print("Saving data to file {} ...".format(path+filename))
  with open(path+filename,"w") as outfile:
    for items in content:
      # assert type(items) in (tuple,list,set)
      for k, item in enumerate(items):
        if k > 0: outfile.write(", ")
        outfile.write(str(item))
      outfile.write("\n")

# -----------------------------------------------------------------------------
# ------------------------ LISTS, TUPLES, DICTS -------------------------------
# -----------------------------------------------------------------------------

def unzip2(values):
  "Unzip a list of pairs (accepts also arrays)"
  to_array = type(values) == np.ndarray
  X, Y = [ x for x, y in values ], [ y for x, y in values ]
  return (np.array(X), np.array(Y)) if to_array else (X, Y)

def unzip3(values):
  "Unzip a list of triples (accepts also arrays)"
  to_array = type(values) == np.ndarray
  X = [ x for x, y, z in values ]
  Y = [ y for x, y, z in values ]
  Z = [ z for x, y, z in values ]
  return (np.array(X), np.array(Y), np.array(Z)) if to_array else (X, Y, Z)

def flatten(L):
  "Unfold the content of a list (outputs a flat list)"
  outlist = list()
  for item in L:
    if type(item) in (tuple, list): outlist += flatten(item)
    else: outlist.append(item)
  return outlist

def multiple_get(dictionary,keywords,default=None):
  if not type(default) in (tuple,list): default = [ default for k in keywords ]
  return [ dictionary.get(key,value) for key, value in zip(keywords,default) ]

# -----------------------------------------------------------------------------
# ------------------------ STRINGS, etc. --------------------------------------
# -----------------------------------------------------------------------------

def string_split(line, sep=' '):
  "Split a string according to the given separator (blanks are removed first)"
  if sep != ' ': line = "".join([c for c in line if c != ' ']) # remove blanks
  return line.split(sep)

def values_as_string(vslice,truncate_at=10,ftype=None):
  "Turn values (from a slice) into strings"
  if ftype == 'float': vslice = [ toNumeric(x) for x in vslice ]
  tup = tuple(set(vslice))
  if len(tup) < truncate_at: return str(tup)
  stup = tup[:truncate_at] # truncating the tuple ...
  return str(stup)[:-1] + " ... )" # removing the trailing round bracket, etc.

def strip_multiple(*strings):
  "Multiple strip"
  return [ s.strip() if type(s) == str else s for s in strings ]
  
def strip_string(string,blacklist):
  return "".join([ ch for ch in string if not ch in blacklist ])
    
def conditional_eval(string,stype=str):
  "Conditionally evaluates a string"
  if stype == str:
    if len(string) == 0: return string
    if string[0] == "'": return eval(string)
    if string[0] == '"': return eval(string)
  if stype in (tuple,list): return eval(string)
  if stype == bool: return string == 'True'
  return stype(string)

# -----------------------------------------------------------------------------
# ------------------------ NUMBERS, etc. --------------------------------------
# -----------------------------------------------------------------------------

def numeric(item):
  if type(item) == str: return False
  try: float(item)
  except: return False
  return True
  
def toNumeric(item):
  try: return float(item)
  except: return item

# -----------------------------------------------------------------------------
# ------------------------ CONVERSIONS ----------------------------------------
# -----------------------------------------------------------------------------

np_hex = np.vectorize(hex) # Vectorized int --> hex conversion

np_abs = np.vectorize(abs) # Vectorized int --> hex conversion

np_int = np.vectorize(int) # Vectorized int --> hex conversion

# -----------------------------------------------------------------------------
# ------------------------ PARAMETERS' HANDLING -------------------------------
# -----------------------------------------------------------------------------

options  = lambda *args: args
services = lambda *args: args

settings = lambda **kwargs: kwargs
store    = lambda **kwargs: kwargs

# -----------------------------------------------------------------------------
# ------------------------ PRINT UTILS ----------------------------------------
# -----------------------------------------------------------------------------

def linefeed(num=1):
  "Print a number of linefeeds (default one)"
  print('\n' * (num-1))

def remove_quoting(item):
  "Remove quoting from a string (basic version)"
  string = item if type(item) == str else str(item)
  return "".join([ ch for ch in string if ch != "'" ])

# -----------------------------------------------------------------------------
# ------------------------ META PROGRAMMING -----------------------------------
# -----------------------------------------------------------------------------

class singleton(object):
  
  "An implementation of the singleton design pattern"
  
  def __init__(self,cls):
    "Init the singleton"
    self.cls, self.obj = cls, None

  def __call__(self,*args,**kwargs):
    "Call the singleton (only one object is created, at the first call)"
    if not self.obj: self.obj = self.cls(*args,**kwargs)
    return self.obj

# -----------------------------------------------------------------------------
# ------------------------ DEBUGGING ------------------------------------------
# -----------------------------------------------------------------------------

@singleton
class Debug(object):

  "Debug control (singleton)"
  
  def __init__(self,level=99):
    "Init debug"
    self.debug_level = level # range(0,100), with 0 = debug-all, 99 = no-debug

  def __call__(self,level=1,mode = 'inc'):
    "Debug update (allowed modes are 'inc', 'dec', 'set')"
    if   mode == 'inc': self.debug_level += level
    elif mode == 'dec': self.debug_level -= level
    elif mode == 'set': self.debug_level  = level
    self.print_level()
    return self.level

  def print_debug_level(self):
    "Print current debug level"
    print("Debugging level is {:2d}".format(self.level))


class runCtrl(object):
  
  "Utility for selecting which SW procedures should be run"
  
  def __init__(self,*args,**kwargs):
    if not hasattr(self,'runDict'): self.runDict = dict()
    for key, val in kwargs.items():
      self.runDict[key] = bool(val)
    for arg in args: self.runDict[arg] = True
    return
    
  def __call__(self,*args,**kwargs):
    self.__init__(*args,**kwargs)
    
  def __lshift__(self,kwargs):
    if not kwargs: return
    if type(kwargs) is str: kwargs = { kwargs : True }
    if type(kwargs) in [tuple,list]: kwargs = { key : True for key in kwargs }
    self.__init__(**kwargs)
    return self
    
  def __getitem__(self,key):
    return self.runDict.get(key)
    
  def __delitem__(self,key):
    if key in self.runDict: del self.runDict[key]
      
  def __str__(self):
    return str(self.runDict)

 
def debug(comment,*args,**kwargs):
  print("{} : ".format(comment),end='')
  print(*args,**kwargs)

# -----------------------------------------------------------------------------
