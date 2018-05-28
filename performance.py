# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 13:52:22 2018

@author: armano
"""


import numpy as np


# -----------------------------------------------------------------------------
# -------------------- PLAIN CONFUSION MATRIX --> cMatrix ---------------------
# -----------------------------------------------------------------------------

class cMatrix(object):

  "Confusion matrix (with TN, FN, FP, TP)"

  total = property(lambda self: self.neg+self.pos)

  accessor = { 'TN' : (0,0), 'FP' : (0,1), 'FN' : (1,0), 'TP' : (1,1) }

  def __init__(self, TN=0., FP=0., FN=0., TP=0.):
    "Initialize the confusion matrix"
    self.matrix = np.array([[TN,FP],[FN,TP]])
    self.neg, self.pos = TN + FP, FN + TP
    
  def __getitem__(self, selectors):
    "Get one or more components of the confusion matrix"
    if type(selectors) == str: selectors = (selectors,)
    items = tuple()
    for s in selectors:
      row, col = cMatrix.accessor[s]
      items = items + ( self.matrix[row,col], )
    return items if len(selectors) > 1 else items[0]
  
  def __lshift__(self,contents): # contents = (TN,FP,FN,TP)
    "Initialize the confusion matrix with other values"
    self.__init__(*contents)
    return self
  
  def __str__(self):
    "Confusion matrix as string"
    (TN, FP), (FN,TP) = self.matrix
    formatter = "( TN, FP, FN, TP = {5.2f}, {5.2f}, {5.2f}, {5.2f} )"
    return formatter.format(TN, FP, FN, TP)

  def display(self, comment = '', end='\n'):
    "Display the content of the confusion matrix"
    (TN,FP),(FN,TP) = self.matrix[:]
    formatter = "TN, FP, FN, TP = {5.2f}, {5.2f}, {5.2f}, {5.2f}"
    print(formatter.format(TN,FP,FN,TP),end=end)

# -----------------------------------------------------------------------------
# ---------------- NORMALIZED CONFUSION MATRIX --> nMatrix --------------------
# -----------------------------------------------------------------------------

class nMatrix(object):
  
  "Normalized confusion matrix (with tn, fp, fn, tp)"

  accessor = { 'tn' : (0,0), 'fp' : (0,1), 'fn' : (1,0), 'tp' : (1,1) }

  @staticmethod
  def specificity(nmats): # exports specificity from a list of nMatrix items
    "Get the specificity (tn) from a list of normalized confusion matrices"
    return np.array([ nm['tn'] for nm in nmats ])
    
  @staticmethod
  def sensitivity(nmats): # exports sensitivity from a list of nMatrix items
    "Get the sensitivity (tp) from a list of normalized confusion matrices"  
    return np.array([ nm['tp'] for nm in nmats ])

  def __init__(self, cm): # type(cm) = cMatrix
    "Initialize the normalized confusion matrix"
    matrix, neg, pos, total = cm.matrix, cm.neg, cm.pos, cm.total
    self.matrix = np.array([matrix[0]/float(neg),matrix[1]/float(pos)])
    self.probs  = np.array([[neg/float(total), 0.],[0., pos/float(total)]])
    
  def __getitem__(self, selectors):
    "Get one or more components of the normalized confusion matrix"
    if type(selectors) == str: selectors = (selectors,)
    items = tuple()
    for s in selectors:
      row, col = nMatrix.accessor[s]
      items = items + ( self.matrix[row,col], )
    return items if len(selectors) > 1 else items[0]
  
  def __str__(self):
    "Normalized confusion matrix as string"
    (tn, fp), (fn,tp) = self.matrix
    return "( tn, tp, fn, tp = {5.2f}, {5.2f}, {5.2f}, {5.2f} )".format(tn, fp, fn, tp)

  def display(self, comment = '', end='\n'):
    "Display the content of the normalized confusion matrix"
    (tn,fp),(fn,tp) = self.matrix[:]
    formatter = "tn, fp, fn, tp = {:5.2f}, {:5.2f}, {:5.2f}, {:5.2f}"
    print(formatter.format(tn,fp,fn,tp))
    
# -----------------------------------------------------------------------------
