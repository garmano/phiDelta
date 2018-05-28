# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 16:42:37 2018

@author: armano
"""


import model

from statistics import Statistics
from view       import View


# -----------------------------------------------------------------------------
# -------------------- PHI-DELTA MEASURES (as functions) ----------------------
# -----------------------------------------------------------------------------

def convert(spec,sens,ratio=1.):
  "Convert <spec,sens> data into <phi,delta> data"
  return model.phidelta_gen(spec,sens,ratio=ratio)

def stats(data,labels,info=None,verbose=False):
  "Make statistics on the given data and labels"
  return Statistics(data,labels,info=info).make(verbose=verbose)
  
def plot(phi,delta,ratio=1.,names=None,title=''):
  "Plot <phi,delta> in a phidelta diagram"
  View(phi,delta,names=names,ratio=ratio).plot(title=title)

# -----------------------------------------------------------------------------
# -------------------- MAIN PROGRAM (for testing) -----------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  from utils import runCtrl, settings
  
  import numpy as np

  from loader import Loader

  run = runCtrl() << settings(convert=True,stats=True)

  if run['convert']:
    spec, sens = np.random.random(100), np.random.random(100)
    phi, delta = convert(spec,sens,ratio=1/2.)
    plot(phi,delta,ratio=1/2.) # ratio = 1/2.
  
  if run['stats']:
    path = '../datasets/UCI datasets/'
    data, labels, info = Loader(path=path).get('breast-cancer')
    phi, delta, names, ratio = stats(data,labels,info=info)
    plot(phi,delta,ratio=ratio) # automatic ratio ...

