# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:08:42 2016
@author: cristinamenghini
"""

""" This script stores the function used to crowl *infoscience*"""

import os
import time
import requests
from bs4 import BeautifulSoup



def create_dir(path_dir):
    """ This function create the directory to store files, whether it doesn't exist.
    
    It takes as inputs:
    @path_dir: the path of the directory to create"""
    
    os.makedirs(path_dir, exist_ok=True)



def fetch_html_infoscience(path_dir, delay=1, error=False):
    """ This function fetches the html files from infoscience. The files are stored in a dir.
    
    It takes as inputs:
    @path_dir: path of the dir that contains html pages
    @delay: seconds to wait between sequent requests
    @error: initial condition for fetching"""
    
    # Get the list of the already fetched html sources
    list_paper = os.listdir(path_dir)[1:]
    
    # In order to establish the starting value of the url attribute
    # Check whether the folder is empty or some files have already been fetched
    if len(list_paper) == 0:
        id_paper = 1
    else:
        id_paper = max([int(i.split('.')[0]) for i in os.listdir(path_dir)[1:]]) + 1

    # While there are pages to fetch
    while error == False:
        try:
            if id_paper % 100 == 0:
                print (id_paper)
            
            # Make the request
            req = requests.get('https://infoscience.epfl.ch/record/' + str(id_paper) + '?ln=en')
            html = (req.content).decode("utf-8")
        
            # Save the html 
            with open(path_dir + str(id_paper) + '.html', 'w') as html_source:
                html_source.write(html)       
            
            # Increment the iterator
            id_paper += 1
        
            # Wait *delay* seconds to retrieve the next page
            time.sleep(delay)
        
        # No more pages to download
        except:
            error = True
            print ('No file to retrieve')