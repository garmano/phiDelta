# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 13:34:51 2016

@author: armano
"""


import numpy as np
import itertools

from utils       import values_as_string, strip_string
from model       import phidelta_std
from performance import cMatrix, nMatrix


# -----------------------------------------------------------------------------
# ------------------------- FEATURE HANDLER (generic) -------------------------
# -----------------------------------------------------------------------------

class Feature(object):
  
  "Generic feature"
  
  __export__  = ( 'score', 'display', 'display_statistics' )

  def __init__(self, fname, ftype, vslice, **kwargs):
    "Initialize a feature (ftype in ['auto','binary','float','nominal'])"
    self.fname, self.ftype = fname, ftype
    self.vslice, self.data = vslice, None
    self.minV, self.meanV, self.maxV = None, None, None
    self.values = sorted(list(set(vslice)))
    self.index = 0 # index >= 0 only when expanding nominal features
    self.cmat, self.nmat = None, None

  def score(self, labels, kneg, kpos):
    "Evaluate the score of a feature according to the given labels"
    prod = (self.data * labels + 1.) / 2.
    TN = sum(kneg * prod) ; FP = sum(kneg) - TN
    TP = sum(kpos * prod) ; FN = sum(kpos) - TP
    self.cmat = cMatrix(TN,FP,FN,TP)
    self.nmat = nMatrix(self.cmat)
    spec, sens = self.nmat['tn','tp']
    return phidelta_std(spec,sens)

  def display(self, comment='', truncate_at = 10): # Violates subclassing schema ...
    "Display all relevant information of a feature"
    print(comment)
    print("Name:   {}".format(self.fname))
    print("Type:   {}".format(self.ftype))
    print("Min, mean, max: {}, {}, {}".format(self.minV, self.meanV, self.maxV))
    vstring = values_as_string(self.values,truncate_at=truncate_at)
    print("Values: {}".format(vstring))
    if len(vstring) > truncate_at: print(" ... etc ({}) ...".format(len(vstring)))
    else: print()

  def display_statistics(self, comment='', mode='normalized'):
    "Display the feature statistics (i.e., cmat or nmat)"
    if mode == 'normalized': self.nmat.display(comment)
    else: self.cmat.display(comment)

# -----------------------------------------------------------------------------
# -------------------- BINARY FEATURES ----------------------------------------
# -----------------------------------------------------------------------------

class binFeature(Feature):
  
  "Binary feature (inherits from Feature)"

  __export__  = ( 'eval_boundaries' )

  def __init__(self, fname, vslice, **kwargs):
    "Initialize a binary feature"
    super().__init__(fname,'binary',vslice,**kwargs)
    vneg, vpos = sorted(tuple(set(self.vslice)))
    self.data = np.array([ 1. if v == vpos else -1. for v in self.vslice ])
    self.minV, self.meanV, self.maxV = self.eval_boundaries(self.data)

  def eval_boundaries(self,vslice):
    return np.nanmin(vslice), np.nanmean(vslice), np.nanmax(vslice)

# -----------------------------------------------------------------------------
# -------------------- FLOATING POINT FEATURES --------------------------------
# -----------------------------------------------------------------------------

class fltFeature(Feature):
  
  "Float feature (inherits from Feature)"

  __export__  = ( 'normalize', 'eval_boundaries' )
  
  def __init__(self, fname, vslice, **kwargs):
    "Initialize a float feature"
    vslice = self.to_float(vslice)
    minV, meanV, maxV = self.eval_boundaries(vslice)
    vslice = self.remove_nan(vslice,default=meanV)
    super().__init__(fname,'float',vslice,**kwargs)
    self.minV, self.meanV, self.maxV = minV, meanV, maxV
    self.normalize()

  def normalize(self):
    "Normalize a feature in [-1,+1] (for binary and float features only)"
    self.data = self.vslice
    if abs(self.minV - self.maxV) == 0.: return
    self.data = -1. + 2. * (self.data - self.minV) / (self.maxV - self.minV)

  def eval_boundaries(self, vslice):
    "Evaluate min, mean and max of a data slice (ignoring 'nan')"
    return np.nanmin(vslice), np.nanmean(vslice), np.nanmax(vslice)

  def to_float(self, vslice, default=0.):
    "Convert a slice to float (unknown values are set to 'nan')" 
    rslice = np.zeros((len(vslice,)))
    for k,v in enumerate(vslice):
      try: rslice[k] = float(v)
      except: rslice[k] = float('nan')
    return rslice

  def remove_nan(self, vslice, default=0.):
    "Remove 'nan' from a slice"
    ndx = np.where(np.isnan(vslice))
    vslice[ndx] = default
    return vslice

# -----------------------------------------------------------------------------
# -------------------- NOMINAL FEATURES ---------------------------------------
# -----------------------------------------------------------------------------

class nomFeature(Feature):
  
  "Nominal feature (actually a hook for a group of binary features)"

  __export__  = ( 'normalize', 'score', 'display_statistics' )
  
  __maxValues__ = 8

  cmats = property(lambda self: [ f.cmat for f in self.hook ])
  nmats = property(lambda self: [ f.nmat for f in self.hook ])

# -------------------- PUBLIC SECTION -----------------------------------------

  def __init__(self, fname, vslice, **kwargs):
    "Initialize a nominal feature (needs a hook to a group of binary features)"
    super().__init__(fname,'nominal',vslice,**kwargs)
    self.subsets = self.expand(list(set(vslice)))
    self.hook = list()
    for k, sub in enumerate(self.subsets):
      rslice = np.array([ 1. if v in sub else -1. for v in vslice ])
      kwargs['index'] = k
      print("*",end='')
      bin_name = self.set_fname(fname,sub)
      self.hook += [ binFeature(bin_name,vslice=rslice,**kwargs) ]
    print()
    # if the nominal feature is in fact a bin feature just take one subset ...
    if len(self.hook) == 2: del self.hook[-1]

  def normalize(self):
    "Normalize a nominal feature (i.e., its binary group components)"
    for feature in self.hook: feature.normalize()

  def score(self, labels, kneg, kpos):
    "Score a nominal feature (i.e., its binary group components)"
    scores = list()
    for feature in self.hook:
      scores += [ feature.score(labels,kneg,kpos) ]
    return scores

  def display(self, *args,**kwargs): # Violates subclassing schema ...
    "Display all relevant information of a feature"
    truncate_at = kwargs.get('truncate_at',50)
    super().display(*args,**kwargs)
    print("Subsets: {}".format(self.subsets[:truncate_at]),end='')

  def display_statistics(self, comment='', mode='normalized'):
    "Display statistics for a nominal feature" 
    for k, feature in enumerate(self.hook):
      print("[{:2d}] ".format(k),end='')
      if mode == 'normalized': feature.nmat.display(comment)
      else: feature.cmat.display(comment)

# -------------------- PRIVATE SECTION -----------------------------------------

  def expand(self, values): # when len(values) > 8 only singletons ...
    "Expand a nominal feature (into a group of corresponding binary features)"
    subsets, values = list(), set(self.values)
    maxsize = 1 if len(values) > self.__maxValues__ else int(len(values)/2)
    for k in range(1,maxsize+1):
      for kcomb in itertools.combinations(values,k):
        kcomb = set(kcomb)
        if not self.xmember(kcomb,subsets,values): subsets += [ kcomb ]
    return subsets
    
  def xmember(self, subset, subsets, values):
    "Check if a subset (or its complement) is member of the selected subsets"
    csubset = values - subset
    return True in [ s == subset or s == csubset for s in subsets ]
    
  def set_fname(self,fname,sub):
    return strip_string("{}({})".format(fname,sub),"{}' ")
    
# -----------------------------------------------------------------------------
# --------------- FEATURE CREATION (with automatic type detection) ------------
# -----------------------------------------------------------------------------

def new_feature(fname, ftype, vslice, **kwargs):
  "Hook function for selecting the proper constructor for a feature"
  # Allowed ftypes: 'auto', 'binary', 'float', 'nominal'
  if ftype == 'auto': ftype = get_feature_type(vslice)
  values = values_as_string(vslice,truncate_at=5,ftype=ftype)
  formatter = "Processing feature: {:<15} type = {:<8} values = {:<15}"
  print(formatter.format(fname,ftype,values))
  if   ftype == 'binary'  : return binFeature(fname,vslice,**kwargs)
  elif ftype == 'float'   : return fltFeature(fname,vslice,**kwargs)
  elif ftype == 'nominal' : return nomFeature(fname,vslice,**kwargs)
  raise Exception

def get_feature_type(vslice,unknown=('-','?')):
  "Identifies the feature type (as 'binary','float', or 'nominal')"
  values = set(vslice)
  for item in values:
    try:
      if not item in unknown: float(item)
    except:
      return 'binary' if len(values) == 2 else 'nominal'
  return 'float'

# -----------------------------------------------------------------------------
# ------------------------- MAIN PROGRAM (for testing) ------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  pass

# -----------------------------------------------------------------------------
