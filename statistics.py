# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 13:53:37 2018

@author: armano
"""


import numpy as np
import model

from utils       import settings, flatten, unzip3
from performance import nMatrix
from features    import new_feature
from dataset     import Dataset


# -----------------------------------------------------------------------------
# -------------------- HANDLER FOR EVALUATING STATISTICS ----------------------
# -----------------------------------------------------------------------------

class Statistics(Dataset):

  "Handler for making statistics on ML data"

  cmats     = property(lambda self: self.get_cmats())
  nmats     = property(lambda self: self.get_nmats())
  
  # --------------- PUBLIC METHODS --------------------------------------------
  
  def __init__(self, data, labels, info):
    "Initialize a handler for making statistics on ML data"
    super().__init__(**settings(data=data,labels=labels,info=info))
    self.kneg, self.kpos = None, None
    self.neg, self.pos = None, None
    self.features = list()
    self.scores = list()
    
  def __lshift__(self,kwargs):
    "Initialize a handler for making statistics on ML data"
    self.__init__(**kwargs)
    
  def make(self,features=None,verbose=False):
    "Make statistics on the selected dataset"
    print("Making statistics on dataset {} ... ".format(self.info.name))
    self.scores = None
    self.kneg, self.kpos = self.kron_delta(-1), self.kron_delta(+1)
    self.neg, self.pos = sum(self.kneg), sum(self.kpos)
    self.nrows, self.ncols = self.data.shape
    self.features = self.new_features(self.info.fnames,self.data)
    self.scores = self.score(features=features,verbose=verbose)
    fnames, ftypes, nmats = self.flatten_nmats()
    spec, sens = nMatrix.specificity(nmats), nMatrix.sensitivity(nmats)
    phi, delta = model.phidelta_std(spec,sens)
    ratio = self.neg / self.pos if self.pos > 0. else None
    return phi, delta, fnames, ratio

  def score(self,features=None,verbose=False):
    "Score some/all features according to the given data"
    features = features if features else self.features
    outscores, labels = list(), self.labels
    print()
    for feature in features:
      scores = feature.score(labels,self.kneg,self.kpos)
      if type(scores) != list: scores = [ scores ]
      outscores += scores
      if verbose: self.display_scores(feature,scores)
    return outscores
    
  def find_features(self,fnames):
    if type(fnames) == str: fnames = [ fnames ]
    return [ feature for feature in self.features if feature.fname in fnames ]

  def export_features(self):
    outlist = list()
    for nmat_info in self.nmats:
      outlist += self.export_feature(nmat_info)
    return outlist

  def export_feature(self,nmat_info):
    fname, ftype, subs, fnum, fhook = nmat_info
    fnames = self.build_names(fname,subs) if ftype == 'nominal' else [ fname ]
    return [ (name,nmat) for name, nmat in zip(fnames,fhook) ]
    
  def build_names(self,fname,subs):
    print(fname)
    print(subs)
    fnames = list()
    #strip_string("{}({})".format(fname,sub),"{}' ") ]

  def best_features(self):
    "Evaluate the ranking for the given features"
    #print("Evaluating best features ...")
    nmats = flatten([ item[-1] for item in self.nmats ])
    spec, sens = nMatrix.specificity(nmats), nMatrix.sensitivity(nmats)
    phi, delta = model.phidelta_std(spec,sens)
    unsorted = [ (k,p,d) for k, (p,d) in enumerate(zip(phi,delta)) ]
    return sorted ( unsorted, key=lambda triple: abs(triple[2]), reverse=True )

  def display(self,which='statistics',*args,**kwargs):
    "Dispatcher for various 'display' methods"
    method_name, default_method = 'display_' + which,self.display_statistics
    getattr(self,method_name,default_method)(*args,**kwargs)

  # --------------- PRIVATE METHODS -------------------------------------------

  def new_features(self, fnames, data):
    "Create new feature handlers (by means of the new_feature hook function)"
    nrows, ncols = data.shape
    return [ new_feature(fnames[k],'auto',data[:,k]) for k in range(ncols) ]

  def get_cmats(self): # for non normalized matrices
    "Get info about feature statistics (fname, ftype, hook_len, hook_list)"
    cmats = list()
    for feature in self.features:
      hook = feature.hook if feature.ftype_measuree == 'nominal' else [ feature ]
      cmats_hook = [ feat.cmat for feat in hook ]
      cmats += [ (feature.fname, feature.ftype, len(hook), cmats_hook)  ]
    return cmats

  def get_nmats(self): # for normalized matrices
    "Get info about feature statistics (fname, ftype, hook_len, hook_list)"
    nmats = list()
    for feature in self.features:
      hook = feature.hook if feature.ftype == 'nominal' else [ feature ]
      nmats_hook = [ feat.nmat for feat in hook ]
      subs = getattr(feature,'subsets',list())
      nmats += [ (feature.fname, feature.ftype, subs, len(hook), nmats_hook)  ]
    return nmats
  
  def flatten_nmats(self):
    "Extract actual data from normalized matrices"
    nmats = list()
    for feature in self.features:
      hook = feature.hook if feature.ftype == 'nominal' else [ feature ]
      for fh in hook: nmats.append((fh.fname,fh.ftype,fh.nmat))
    fnames, ftypes, nmats = unzip3(nmats)
    return fnames, ftypes, nmats
  
  def get_features_info(self,nmats=None):
    "Get feature hook descritors"
    if not nmats: nmats = self.nmats
    info = list()
    for mat_info in nmats:
      fname, ftype, subs, fnum = mat_info[:4]
      info.append((fname, ftype, subs, fnum))
    return info

  def kron_delta(self,reference):
    "Kronecker delta between actual labels and a reference label"
    return np.array([1 if v == reference else 0 for v in self.labels])

  def eval_backIndex(self):
    "Link (phi,delta) values to the corresponding features" 
    back_index, index = {}, 0
    for k, item in enumerate(self.nmats):
      fname, ftype, subs, numfeat, hook = item
      for ndx, nmat in enumerate(hook):
        back_index[index] = (fname, ftype, (k, ndx))
        index += 1
    return back_index

  def display_statistics(self, mode='normalized', comment=''):
    "Display statistics for all features"
    if comment: print(comment)
    for feature in self.features:
      print("\nDetails on feature: {:<10}".format(feature.fname))
      feature.display_statistics(mode=mode)

  def display_scores(self,feature,scores,comment=''):
    "Print scores (two decimals by default)"
    if comment: print(comment)
    header = "Scoring feature: {:<20}".format(feature.fname)
    print(header,end='')
    for k, (phi,delta) in enumerate(scores):
      if k > 0: print(" " * len(header),end='')
      if len(scores) == 1: print('      ',end='')
      else: print(" [{:2d}] ".format(k),end='')
      print("{:>10.2f} {:>10.2f}  ".format(phi,delta),end='')
      if feature.ftype == 'nominal': print(feature.subsets[k])
      else: print()

  def display_ranking(self, comment='', ranking=None):
    "Display the ranking of the given features"
    print("\nFeature ranking is ...")
    if ranking is None: ranking = self.best_features()
    back_index = self.eval_backIndex()
    if comment: print(comment)
    for h,p,d in ranking:
      fname, ftype, (k,ndx) = back_index[h]
      formatter  = "Feature ({:3d},{:2d}) {:<20} ({:})\t"
      formatter += "-->\t (phi,delta) = ( {:7.4f}, {:7.4f} )"
      print(formatter.format(k,ndx,fname,ftype,p,d))
    print()
    
  def display_features(self, features=None, comment=''):
    "Display the embedded features"
    features = self.features if features is None else features
    if comment: print(comment)
    for feature in features: feature.display()
      
  def display_features_by_name(self, fnames=None, comment=''):
    if not fnames: fnames = [ feat.fname for feat in self.features ]
    if type(fnames) == str: fnames = [ fnames ]
    if comment: print(comment)
    for feature in self.find_features(fnames):
      feature.display()


# -----------------------------------------------------------------------------
# -------------------- MAIN PROGRAM (for testing) -----------------------------
# -----------------------------------------------------------------------------
      
if __name__ == '__main__':

  from loader import Loader

  UCIpath = '../datasets/UCI datasets/'
  
  csv = Loader(path=UCIpath)
  
  #data, labels, info = csv.load(filename='SPECT-full.csv',index=0,sep=';')
  data, labels, info = csv.get('flare')
  
  stats = Statistics(data=data,labels=labels,info=info)
  
  phi, delta, fnames, dratio = stats.make()
  
  stats.display('statistics')
  
  stats.display('ranking')
  
# -----------------------------------------------------------------------------
