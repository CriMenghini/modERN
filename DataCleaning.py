# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 08:20:10 2017

@author: cristinamenghini
"""

import os 
import json
import threading
import time
from sys import argv
from ParseInfoscience import *

# When you want to run that file you need to insert the path of the folder which contains the html sources
script, path_data = argv

PATH = path_data
list_file = os.listdir(PATH)[1:]

def save_JSON(file_name, new_data):
    """ This function updates a JSON file appending new elements.
    
    It takes as input:
    @file_name: the name of the file to update
    @new_data: the new data to append
    """
    
    # Here we load the already present content in the file and then we update it
    with open(file_name, 'r') as f:
        data = json.load(f)
        
    data.update(new_data)
    
    # Storing it back in the file
    with open(file_name, 'w') as outfile:
        # The input data are stored in such a way that the JSON is readable
        json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'))
            
    
    
def create_dictionary(list_file, PATH, thread):
    """This fuction add to a dictionary, the info related to the publication and puts them into a JSON file.
    
    It takes as inputs:
    @list_file: list of html pages
    @PATH: path of html folder
    @thread: id of the thread"""
    
    # Initialize the dictionary to store in the JSON
    paper_data = {}
    
    # For the element in the list
    for i,j in enumerate(list_file):
        
        # Get the information of the publication by the class InfoscienceParser
        info = InfoscienceParser(PATH, i, list_file).parse_html()
        
        # Whether the return of the parser is not a string
        if type(info) != str:
            # We store into the dictionary the information related to the publication (using as key the id of the page)
            paper_data[j[:-5]] = InfoscienceParser(PATH, i, list_file).parse_html()
        
        # When 1000 elements have been inspected (that's in order to be sure to have saved something if something in 
        # the process goes wrong)
        if i % 1000 == 0:
            # We put them in the JSON file
            save_JSON('paper.json', paper_data)
            
            # Printing check
            print (i,' file THREAD:', thread, 'saved in JSON.')
            
            # Bring the dictionary back to the initial form
            paper_data = {}
    
    # After having inspected all the elements be sure to store in the JASON also the last inspected elements
    save_JSON('paper.json', paper_data)
  
    print ('FINISH THREAD:', thread)
    

def html_chunks(n, html_list):
    """This function returns the list of chunks that will be used during the multi-threading.
    @n: is the number of threads;
    @html_list: is the list of user to split."""
    
    # Get the number of elements in each chunk
    num = float(len(html_list))/n 
    
    # Compute the lists-1
    html_lists = [ html_list [i:i + int(num)] for i in range(0, (n-1)*int(num), int(num))]
    
    # Append the last list composed by remaining elements
    html_lists.append(html_list[(n-1)*int(num):])
    
    return html_lists


def worker(list_file, PATH, thread):
    """This function define the work that each thread is going to do.
    The inputs of the function are the arguments of create_dictionary function."""
    
    # Define the function the threads will work with
    create_dictionary(list_file, PATH, thread)
    
# Parallelize the work on four threads    
for j in range(len(chunks)):
    # Initialize each thread
    t = threading.Thread(target = worker, args = (chunks[j], PATH, j)) # That's the function that each thread will execute
    
    # Let it work after 20 seconds respect the previous
    time.sleep(20)
    
    # And start it
    t.start()
       
