# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:36:23 2017

@author: cristinamenghini
"""

from unidecode import unidecode


def uniform_authors(data):
    """ This function returns the data with uniformed authors.
    It takes as input:
    @data: data dictionary"""
    
    # For each paper
    for i in list(data.keys()):
        try:
            # Extract the authors
            for j in range(len(data[i]['Authors'])):
                # Encode them
                t = unidecode(data[i]['Authors'][j])
                t.encode("ascii")
                # Make them uniform 
                data[i]['Authors'][j] = t.lower().replace('.','')           
        except:
            continue
    
    return data
    
    
def uniform_epfl_authors(data):
    """ This function returns the data with uniformed authors.
    It takes as input:
    @data: data dictionary"""
    
    # Repeat the same operations to the Epfl authors according to the format they are stored
    for i in list(data.keys()):
        dic = []
        try:
            for j in range(len(data[i]['Epfl authors'])):
                string = list(data[i]['Epfl authors'][j].keys())[0]
                t = unidecode(string)
                t.encode("ascii")
                dic += [{t.lower().replace('.','') : list(data[i]['Epfl authors'][j].values())[0]}]
            data[i]['Epfl authors'] = dic
        except:
            continue
        
    return data