# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 23:10:48 2017

@author: cristinamenghini
"""

import pickle
from collections import defaultdict


# Get dictionary (lab,school)
def school_lab(dict_lab_site, name_school):
    
    school = pickle.load(open(name_school + '.p', 'rb')) # Recall 
    lab_school = {}
    for i in list(dict_lab_site.keys()):
        for nodes in list(school.keys()):
            list_node = school[nodes]
            if i in list_node:
                lab_school[i] = name_school
                break
            else:
                continue   
    
    return lab_school
    
    
def school_publication(school, name_school, dict_lab_years, dict_school_pub):
    
    # Get dictionary (school, dict(year,list numb papers))
    
    dict_school_pub[name_school] = defaultdict(list)
    for lab in school:   
        for year in list(dict_lab_years[lab].keys()):
            dict_school_pub[school[lab]][year] += [dict_lab_years[lab][year]]
            
    for year in dict_school_pub[name_school]:
        dict_school_pub[name_school][year] = sum(dict_school_pub[name_school][year])

    return dict_school_pub
    
    
def school_author(school, name_school, dict_author_year, dict_school_pub):
    
    # Get dictionary (school, dict(year,list numb papers))
    
    dict_school_pub[name_school] = defaultdict(list)
    for lab in school:   
        for year in list(dict_author_year[lab].keys()):
            dict_school_pub[school[lab]][year] += [dict_author_year[lab][year]]
            
    for year in dict_school_pub[name_school]:
        dict_school_pub[name_school][year] = sum(dict_school_pub[name_school][year])

    return dict_school_pub