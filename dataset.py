# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 13:53:37 2018

@author: armano
"""


pass


# -----------------------------------------------------------------------------
# -------------------- DATASET ------------------------------------------------
# -----------------------------------------------------------------------------

class Dataset(object):

  "Dataset for ML data (embeds: data, instances, and data information)"

  def __init__(self, data=None, labels=None, info=None):
    "Initialize an handler for making statistics on ML data"
    self.data, self.labels, self.info = data, labels, info
    self.nrows, self.ncols = self.data.shape if data is not None else None,None
    
  def __lshift__(self,data,labels,info=None):
    "Setting the content of a dataset with data, labels, and info"
    self.__init__(data,labels,info)
    
  def display(self, comment='', mode='plain'):
    "Display the dataset"
    for k, (instance, label) in enumerate(zip(self.data,self.labels)):
      print("[{:3d}] instance: {} label: {}".format(k,instance,label))


# -----------------------------------------------------------------------------
# -------------------- MAIN PROGRAM (for testing) -----------------------------
# -----------------------------------------------------------------------------
      
if __name__ == '__main__':

  from loader import Loader

  UCIpath = '../datasets/UCI datasets/'
  
  csv = Loader(path=UCIpath)
  
  data, labels, info = csv.load(filename='SPECT-full.csv',index=0,sep=';')
  
  dataset = Dataset(data=data,labels=labels,info=info)
  
  #dataset.display()