# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:49:19 2018

@author: armano
"""

pass # TESTING ONLY ...

# ------------------------- MAIN PROGRAM --------------------------------------

if __name__ == '__main__':
  
  from statistics import Statistics
  from loader import Loader
  from view import View

  print("\nEXPERIMENTS\n")
  
  # SETTING A DATASET LOADER

  # The path to datasets may be optionally changed ...
  loader = Loader(path='../datasets/UCI datasets/')
  
  # SETTING DATASETS

#  datasets = ( 'arrhythmia', ('balloons', 1), ('balloons', 2), \
#               'breast-cancer', 'census', 'chess', 'fars', 'flare', \
#               'kr-vs-k', ('lymphography', 1), ('lymphography', 2), \
#               'mushroom', 'SPECT-binary', 'SPECT-full', 'splice' )

#  datasets = ( 'arrhythmia', ('balloons', 1), ('balloons', 2), \
#               'breast-cancer', 'chess' )

#  datasets = ( 'arrhythmia', ('balloons', 1), ('balloons', 2), 'flare' )

#  datasets = ( 'flare', )

  # Try changing the list of datasets

  # However, please consider that the 'census' datasets takes several minutes
  # [ due to the dataset size AND to the presence of many nominal features ]

  datasets = ( 'arrhythmia', ('balloons', 1), ('balloons', 2), 'flare' )

  # SETTING THE CLASS RATIO

  # Standard phidelta diagram: ratio = 1.
  ratio = 1. # Try changing the class ratio to a fixed value (e.g., 2., 1/5.)

  # You may also change the class ratio randomly ... (see below)

  # from random import randint

  # The option 'crossings' is not required when ratio == 1.
  # You may not want to remove 'crossings' when ratio <> 1.
  
  for k, dname in enumerate(datasets):    
    # ratio = float(randint(1,6))  # ratio > 1 means --> neg than pos
    # if randint(0,1): ratio = 1. / ratio # ratio < 1 --> more pos than neg
    data, labels, info = loader.get(dname)
    stats = Statistics(data=data,labels=labels,info=info)
    phi, delta, fnames, dratio = stats.make()
    view = View(phi,delta,ratio=ratio)
    view >> 'crossings' # remove the 'crossings' option, as ratio == 1.
    view.plot(title=dname)

# -----------------------------------------------------------------------------
