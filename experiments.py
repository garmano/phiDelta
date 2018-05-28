# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 16:49:19 2018

@author: armano
"""

import matplotlib.pyplot as plt

from utils import np_abs

from statistics import cStatistics

from model import model

from view import view


if __name__ == '__main__':
  
  print("\nEXPERIMENTS\n")
  
  # working_dir = '/Users/armano/python/phidelta/'
  
  # os.chdir(working_dir)
  
  datasets    = '../datasets/UCI datasets/'
  
  # STATISTICS

  stats = cStatistics(path=datasets)
  
  #stats = cStatistics('SPECT-full',path=datasets, sep=';',index=0)

  #stats = cStatistics('SPECT-binary', path=datasets, sep=',', index=0, header=True,
  #                     classes=('1','0'))

  #stats = cStatistics('simple',path=datasets,sep=';', index=0,header=False)

  #stats = cStatistics('balloons',path=datasets,sep=',',index=-1,header=False,classes=('T','F'))

  #stats = cStatistics('balloons2',path=datasets,sep=',',index=-1,header=False,classes=('T','F'))

  #stats = cStatistics('lymphography',path=datasets,sep=',',index=-1,header=True,
  #                    classes=(('normal','fibrosis'),('metastases','malign_lymph')))

  #stats = cStatistics('lymphography',path=datasets,sep=',',index=-1,header=True,
  #                    classes=('normal',('metastases','malign_lymph','fibrosis')))

  #stats = cStatistics('breast-cancer',path=datasets,sep=',',index=-1,header=True,
  #                    classes = ('recurrence-events', 'no-recurrence-events'))

  stats.load(filename='flare.csv', sep=',', index=-1,
             header=True, classes = (('B','C','D'),('E','H','F')))
             
  stats.make()

  #stats = cStatistics('splice',path=datasets,sep=',',index=-1,header=True,
  #                     classes = ('EI',('IE', 'N')))

  #draw = 'draw'
  #win = 'zero, one, two, three, four, five, six, seven, eight, nine, ten, \
  #       eleven, twelve, thirteen, fourteen, fifteen, sixteen'.split(',')
  #stats = cStatistics('kr-vs-k',path=datasets,sep=',',index=-1,header=True,
  #                     classes = (draw,win))

  #stats = cStatistics('mushroom',path=datasets,sep=',',index=-1,header=True,
  #                     classes = ('e','p'))

  # injury = 'Incapaciting_Injury,Fatal_Injury'.split(',')
  # other  = 'No_Injury,Possible_Injury,Nonincapaciting_Evident_Injury, \
  #          Injured_Severity_UDisplaying fnknown,Died_Prior_to_Accident,Unknown'.split(',')
  #stats = cStatistics('fars',path=datasets,sep=',',index=-1,header=True,
  #                     classes = (injury,other))

  #stats = cStatistics('chess',path=datasets,sep=',',index=-1,header=True,
  #                     classes = ('won','nowin'))

  #stats = cStatistics('census',path=datasets,sep=',',index=-1,header=True,
  #                     classes = ('50000+.','-_50000.'))
         
  #stats = cStatistics('arrhythmia',path=datasets,sep=',',index=-1,header=False)
  #stats = cStatistics('autos',path=datasets,sep=',',index=0,header=False)

  # NB 'balloons2' is NOT a standard UCI ML dataset ...

  #cmats = stats.score()

  #stats.displayStatistics(mode='normalized')

  # RANKING
  
  stats.display_ranking()

  # VISUALIZATION

  v = view(model=model(ratio=1.),title= stats.name)
  
  v << ('axes', 'borders', 'crossings', 'fill')
  
  v.options(s=4,linewidth=2,cmap=plt.get_cmap('jet')) # try: plasma, rainbow, jet
  
  nmats, fhooks = stats.flatten_nmats()

  phi, delta = v.model.coords(nmats=nmats)
  
  v.plot_data(phi,delta,colors=np_abs(delta))

