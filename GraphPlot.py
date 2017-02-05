# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:53:22 2017

@author: cristinamenghini
"""

import matplotlib.pyplot as plt

def plot_measures(sorted_values, title, xlabel, ylabel, name_file):
    
    """ This function returns the plot of the input values.
    It takes as inputs:
    @sorted_values: vales to plot
    @title: plt title
    @xlabel: plt x title
    @ylabel: plt y title
    @name_file: name of the file to save the plt"""
    
    
    plt.figure(figsize=(15,8), dpi=80)
    plt.loglog(sorted_values,'o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(name_file + '.png', dpi=100)
    plt.show()
    
    
def getKey(item):
    """ This function, given a tuple, hust return the second element."""
    
    return item[1]