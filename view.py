# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:21:34 2018

@author: armano
"""

import numpy as np

import matplotlib.pyplot as plt

from utils import unzip2, options, settings

from utils import multiple_get, remove_quoting

from model import phidelta_std2gen

from geometry import Geometry


# -----------------------------------------------------------------------------
# ------------------------- VIEW OF PHI-DELTA MEASURES ------------------------
# -----------------------------------------------------------------------------

class View(Geometry):
 
  "Phidelta view (model, view, controller design pattern)"
 
  __settings__ = settings(s=12,linewidth=2,cmap='jet') # plot settings
  __options__  = options('axes','borders','crossings','fill') # plot options

# -------------------- PUBLIC SECTION -----------------------------------------

  def __init__(self, phi, delta, names=None, ratio=1.):
    "Initialize a view object for phidelta diagrams"
    super().__init__(ratio=ratio)
    self.phi, self.delta = phidelta_std2gen(phi,delta,ratio=ratio)
    self.names = names
    self.settings = self.__settings__
    self.options  = self.__options__
    self.figure, self.axes = None, None

  def plot(self, title=''):
    "Plot 2D data" # names not used yet ...
    if not self.figure: self.plot_shape(title=title)
    colors = 1. - np.abs(self.delta)
    self.axes.scatter(self.phi,self.delta,c=colors,**self.settings)
    plt.show()
    
  def __lshift__(self,items): # plot options/settings controller (add/update)
    "Activate phidelta 'plot' options or settings"
    if type(items) == str: items = (items,)
    if type(items) in (tuple,list,set): self.add_options(items)
    elif type(items) == dict: self.update_settings(items)
    else: print("{} are not valid options / settings ...".format(items))
    return

  def __rshift__(self,items): # plot options controller (del)
    "Deactivate phidelta 'plot' options"
    if type(items) == str: items = (items,)
    if type(items) in (tuple,list,set): self.del_options(items)
    else: print("{} are not valid options ...".format(items))
    return

# -------------------- PRIVATE SECTION: OPTIONS AND SETTINGS ------------------

  def add_options(self,optList):
    options = set(self.options)
    [ options.add(opt) for opt in optList if opt in self.__options__ ]
    self.options = list(options)
    return self

  def del_options(self,optList):
    options = set(self.options)
    [ options.discard(opt) for opt in optList ]
    self.options = list(options)
    return self

  def update_settings(self,kwargs): # scatter options controller (add)
    "Set options for pyplot.scatter"
    if not kwargs: self.settings = self.__settings__
    for k, v in kwargs.items():
      if not k in self.__settings__: continue
      self.settings[k] = self.__settings__[k] if v == None else v
    return self

# -------------------- PRIVATE SECTION: PLOTTING SHAPE ------------------------

  def plot_shape(self,title=''):
    "Shows a phidelta diagram"
    self.figure = plt.figure()
    self.axes   = self.figure.add_subplot(111, aspect = 'equal')
    self.set_title(title) ; self.set_limits()
    if 'axes' in self.options: self.draw_axes()
    if 'borders' in self.options: self.draw_borders()
    if 'crossings' in self.options: self.draw_crossings()
    if 'fill' in self.options: self.fill()

  def set_title(self,title=''):
    "Set the title of a plot (removing quotes if needed)"
    self.axes.set_title(remove_quoting(title))

  def set_limits(self):
    "Set limits of a phidelta diagram"
    xmin, ymax, xmax, ymin = multiple_get(self.limits,self.limit_keys)
    self.axes.set_xlim(xmin, xmax) ; self.axes.set_ylim(ymin, ymax)
    
  def draw_axes(self):
    "Draw axes of a phidelta diagram"
    xmin, ymax, xmax, ymin  = multiple_get(self.limits,self.limit_keys)
    self.axes.plot([0.,0.],[-1.,1.], color = 'b', zorder=1)
    self.axes.plot([xmin,xmax],[0.,0.], color = 'b', zorder=1)
    
  def draw_borders(self):
    "Draw borders of a phidelta diagram"
    X, Y = unzip2(multiple_get(self.borders,self.border_keys))
    self.axes.plot ( X + X[:1], Y + Y[:1], color='r', zorder=1 )

  def draw_crossings(self):
    "Draw crossings of a phidelta diagram"
    left, top, right, bottom = multiple_get(self.borders,self.border_keys)
    X, Y = zip(left,right)
    self.axes.plot ( X, Y, color='0.5', linestyle='dashed', zorder=1 )
    X, Y = zip(top,bottom)
    self.axes.plot ( X, Y, color='0.5', linestyle='dashed', zorder=1 )

  def fill(self,size=160):
    "Fill the background of a phidelta diagram"
    X, Y = unzip2(multiple_get(self.borders,self.border_keys))
    self.axes.fill ( X + X[:1], Y + Y[:1], color='lightgrey', zorder=0 )


# -----------------------------------------------------------------------------
# ------------------------- MAIN PROGRAM (for testing) ------------------------
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  from utils      import runCtrl
  from utils      import options, settings
  from loader     import Loader
  from statistics import Statistics
  
  import model

  run = runCtrl() << settings(grid=False,random=False,data=False,settings=True)
    
  if run['grid']:

    phi, delta = model.make_grid(size=10)
    view = View(phi,delta)
    view.plot()  

  if run['random']:

    phi, delta = model.random_samples(nsamples=100) 
    view = View(phi,delta)
    view.plot()
    
  if run['data']:
    
    dataset = 'breast-cancer'
    path = "../datasets/UCI datasets/"
    data, labels, info = Loader(path=path).get(dataset)
    phi, delta, names, ratio = Statistics(data,labels,info).make(verbose=True)
    view = View(phi,delta,names,ratio=ratio)
    view.plot(title=dataset)

  if run['settings']:
    
    phi, delta = model.make_grid(size=10)

    view = View(phi,delta,ratio=2.)
    view << options('fill','crossings','axes')
    view << settings(s=14,cmap='plasma') # jet, plasma, cool, ...
    view.plot(title='Testing view settings and options')

# -----------------------------------------------------------------------------
