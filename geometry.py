# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 15:11:22 2018

@author: armano
"""


from utils import numeric


# -----------------------------------------------------------------------------
# -------------------- PHI-DELTA GEOMETRY -------------------------------------
# -----------------------------------------------------------------------------

class Geometry(object):

  "Geometry of phidelta measures and diagrams"
  
  __borders__  = { 'top' : (0.,+1.), 'bottom': (0.,-1.), \
                   'left': (-1.,0.), 'right' : (+1.,0.) }

  limit_keys = border_keys = ('left','top','right','bottom')
  
  def __init__(self,ratio=1.):
    "Init a Geometry object (constrains a phidelta diagram, given the ratio)"
    ratio = float(ratio) if numeric(ratio) else 1.
    if ratio < 10**(-2): ratio = 10**(-2)
    if ratio > 10**(+2): ratio = 10**(+2)
    self.ratio = ratio
    self.neg, self.pos = ratio/(1+ratio), 1/(1+ratio)  
    self.borders = self.eval_borders()
    self.limits  = self.get_limits()

  def __call__(self):
    "Get ratio, borders and limits of a geometry object"
    return self.ratio, self.borders, self.limits

  def eval_borders(self):
    "Evaluate the borders of a geometry object"
    borders, standard_borders = dict(), self.__borders__
    for key, (x,y) in standard_borders.items():
      borders[key] = self.std2gen(x,y)
    return borders
    
  def get_limits(self):
    "Evaluate the limits of a geometry object"
    limits = dict()
    limits['top'] = self.borders['top'][1]
    limits['bottom'] = self.borders['bottom'][1]
    limits['left'] = self.borders['left'][0]
    limits['right'] = self.borders['right'][0]
    return limits

  def std2gen(self,phi,delta):
    "Conversion from phidelta standard to phidelta generalized"
    neg, pos = self.neg, self.pos
    return (neg - pos) * (1. - delta) + phi, delta - (neg-pos) * phi


# -----------------------------------------------------------------------------
# -------------------- MAIN PROGRAM (for testing) -----------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  

  geo = Geometry(ratio=3.)

  print("Borders: ", geo.borders)
  print("Limits:  ", geo.limits)
  
  #print("Ratio, borders and limits: ",geo())
  
# -----------------------------------------------------------------------------
