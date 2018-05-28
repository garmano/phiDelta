# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:54:02 2018

@author: armano
"""


import numpy as np

from utils import unzip2
from itertools import product

# -------------------- PHI-DELTA MODEL ----------------------------------------

def phidelta_std(spec,sens):
  "Evaluate phi, delta from sens, spec (standard version)"
  return -spec + sens, spec + sens - 1
  
def phidelta_std2gen(phi,delta,ratio=1.):
  "Conversion from phidelta standard to phidelta generalized"
  neg, pos = ratio/(1+ratio), 1/(1+ratio)  
  return (neg - pos) * (1. - delta) + phi, delta - (neg-pos)*phi

# --------------------- TESTING ONLY ----------------------------------------

def make_grid(size=50):
  "Evaluate a phidelta grid --virtually, a square grid (testing only)"
  xlim = ylim = np.linspace(0.,+1.,size)
  grid = np.zeros ( shape=(size*size,), dtype = tuple )
  for k, (spec, sens) in enumerate(product(xlim,ylim)): grid[k] = (spec,sens)
  phi, delta = phidelta_std(*unzip2(grid))
  return phi, delta

def random_samples(nsamples=100):
  "Generate random samples in a phidelta space (testing only)"
  spec, sens = np.random.rand(nsamples), np.random.rand(nsamples)
  phi, delta = phidelta_std(spec,sens)
  return phi, delta

# -----------------------------------------------------------------------------
# -------------------- MAIN PROGRAM (for testing) -----------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':

  pass     

# -----------------------------------------------------------------------------
