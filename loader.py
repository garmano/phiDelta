#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:43:23 2018

@author: giuliano
"""


import numpy as np

from utils import multiple_get, string_split

from datainfo import datainfo


# -----------------------------------------------------------------------------
# ------------------------ DATASET LOADER -------------------------------------
# -----------------------------------------------------------------------------

class Loader(object):

  "Handler for loading files"

# ------------------------ PUBLIC SECTION -------------------------------------

  def __init__(self,path='',source='datasets.info'):
    self.path = path
    self.source = source
    self.content = dict()
    self.dataset = None

  def get(self,name,version=None):
    "Get a dataset (file information retrieved from an *.info file)"
    name = (name,version) if version else name
    print("\n^^^ Loading dataset {} ^^^\n".format(name))
    if not self.content: self.content = self.read_datasets()
    info = self.content.get(name,None)
    assert info, "Dataset not found looking at {} ...".format(self.source)
    return self.load_dataset(info)

  def load(self,filename,**kwargs):
    "Load a dataset (file information given as kwargs)"
    kwargs['filename'] = filename
    info = datainfo(**kwargs)
    return self.load_dataset(info)
    
  def display(self,comment='',verbose=False):
    print()
    if comment: print(comment)
    for dname, dset in self.content.items():
      dset.display(verbose=verbose)

# ------------------------ PRIVATE SECTION ------------------------------------

  def load_dataset(self,info):
    "Load a dataset (file information given as dataset object)"
    keys = 'filename', 'classes', 'sep', 'index', 'header'
    filename, classes, sep, index, header = multiple_get(info.__dict__,keys)
    fnames, check = None, info.check_class
    content = self.load_content(filename)
    if header: fnames, content = content[0], content[1:]
    data = np.array([ string_split(ln,sep) for ln in content ],dtype=str)
    labels = np.array ( [ 1 if check(c) else -1 for c in data[:,index] ] )
    data = np.delete(data,index,1)
    nrows, ncols = data.shape
    assert len(data) > 0, "Failure while loading file {}".format(filename)
    info.fnames = self.parse_fnames(fnames,ncols=ncols,sep=sep,index=index)
    return data, labels, info

  def load_content(self,filename):
    with open(self.path + filename) as infile:
      content = [ line.strip() for line in infile ]
    return content

  def parse_fnames(self,fnames=None,ncols=0,sep=' ',index=-1):
    if fnames:
      fnames = string_split(fnames,sep=sep)
      del fnames[index]
    else:
      fnames = [ "F" + str(k+1) for k in range(ncols) ]
    return fnames

  def read_datasets(self):
    with open(self.path + self.source) as sourcefile:
      raw_content = [ ln.strip() for ln in sourcefile if ln.strip() != '' ]
    content = list()
    for at, line in enumerate(raw_content):
      if line.find('@dataset') == -1: continue
      content += [ datainfo() << self.parse_dataset(raw_content[at:]) ]
    return { dset.name : dset for dset in content }
  
  def parse_dataset(self,raw_content):
    outlist, multiline = list(), ''
    for k, line in enumerate(raw_content):
      if k > 0 and line.find('@dataset') != -1: break
      multiline += line
      mode = 'cat' if line.strip()[-1] == ',' else 'append'
      if mode == 'cat': continue
      outlist.append(multiline)
      multiline = ''
    return outlist

# -----------------------------------------------------------------------------
# ------------------------ MAIN PROGRAM (for testing) -------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':

  UCIpath = '../datasets/UCI datasets/'
  
  L = Loader(path=UCIpath)
  
  #data, labels, info = L.load(filename='flare.csv',header=True,classes=(('B','C','D'),('E','H','F')))
  
  data, labels, info = L.get('SPECT-full')

# -----------------------------------------------------------------------------
