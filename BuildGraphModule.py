# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 10:08:44 2017

@author: cristinamenghini
"""

from collections import defaultdict
import networkx as nx
import collections
import csv


def get_authors(data, kind_authors):
    """ This function returns the list of authors of the publication
    taken into account.
    
    It takes as inputs:
    @data: all the papers data
    @kind_authors: the name of the attribute to look for"""
    
    # Initialize the list
    authors = []
    
    # For each publication
    for i in list(data.keys()):
        
        # Verify whether the attribute is present
        try:
            # Add the list of authors of the paper into the 
            # overall list
            authors += [j for j in data[i][kind_authors]]
        # If the attribute isn't present continue the loop
        except:
            continue
    
    return authors
    
    
def create_authors_id(authors, kind_author):
    """ This function returns a dictionaries (key,value)=(ID, author) and (key,value)=(author, ID) 
    and saves this information in a .csv file.
    
    It takes as input:
    @authors: the list of authors
    @kind_author: 'epfl' or 'all'"""
    
    # Initialize the dictionaries
    dictionary_a_id = {}
    dictionary_id_a = {}
    
    # Create the new file 
    with open('author_id_'+ kind_author +'.csv', 'a') as f:
    
        # For each element in author
        for id_,author in enumerate(set(authors)):
            # Define the id for the author
            dictionary_a_id[author] = id_
            
            # Reverse the dictionary
            dictionary_id_a[id_] = author
            
            # Create the tuple (key, values) to store in the file
            author_dict = {'ID': id_, 'Author': author}
            
            # Define the dictwriter
            w = csv.DictWriter(f, author_dict.keys())
            
            # Then write the dictionary in the file
            w.writerow(author_dict)
            
    
    return dictionary_a_id, dictionary_id_a
    
    
def list_coauthors(data):
    """ This function returns a dictionary (key,value)=(author, [list of coauthors]).
    
    It takes as input:
    @data:  all the papers data"""
    
    # Define the dictionary
    dict_authors = defaultdict(list)
    
    # For each publication
    for p in list(data.keys()):
        # Check the presence of information related to the authors    
        try:
            # Get the list of authors
            list_authors = data[p]['Authors']
            
            # For each element in the list
            for a in list_authors:
                # Create an instance of the dictionary appending as values the list of authors except him/her
                dict_authors[a] += [j for j in list_authors if j != a]
        
        # If there is not continue the loop 
        except:
            continue

                    
    return dict_authors
    

def list_coauthors_epfl(data):
    """ This function returns a dictionary (key,value)=(author, [list of coauthors]).
    
    It takes as input:
    @data:  all the papers data"""
    
    # Initialize the dictionary
    dict_authors_epfl = defaultdict(list)
    
    # For each pubblication
    for p in list(data.keys()):
        # If present
        try:
            # Extracte the list of epfl authors
            list_authors_raw = data[p]['Epfl authors']
            # Unpack the list
            list_authors_list = [list(i.keys()) for i in list_authors_raw]
            
            # Whether the list of authors contains more than one element
            if len(list_authors_list) > 1:
                # Get the final list unpacking elements
                list_authors = [i[0] for i in list_authors_list]
            else:
                # Just get the element as the list
                list_authors = list_authors_list[0]
            
            # For each author create an instance in the dictionary
            for a in list_authors:
                dict_authors_epfl[a] += [j for j in list_authors if j != a]
        
        # If there re not epfl authors continue the loop
        except:
            continue
            
    return dict_authors_epfl
    
    
def number_collaborations(dict_authors):
    """ This function create a dictionary (key,value)=(author, {coauthor:number of collaborations}).
    
    It takes as input:
    @dict_authors: dictionary of coauthorships"""
    
    # Initialize the dictionary
    dict_numb_coll = {}
    
    # for each author
    for key in list(dict_authors.keys()):
        # Obtain the count of collaborations wiht each co-author
        dict_numb_coll[key] = collections.Counter(dict_authors[key])
        
    return dict_numb_coll
    
    
def set_coauthors(dict_authors):
    """ This function define the same dictionary as list_coauthors, considering the set 
    of coauthors instead."""
    
    # Inizialize the dictionary
    dict_authors_set = {}
    
    # For each author
    for key in list(dict_authors):
        # Get the set of co-authors
        dict_authors_set[key] = list(set(dict_authors[key]))
        
    return dict_authors_set
    

def create_edges(dict_authors_set, dictionary_a_id):
    """ This function treturn the set of edges of our graph.
    
    It takes as inputs:
    @dict_authors_set: the dictionary (author, set(coauthors))
    @dictionary_a_id: the dictionary (author,ID)"""
    
    # Define an epty set of edges
    edges = set()
    
    # For each author
    for key in list(dict_authors_set.keys()):       
        # If the list of co-authors is not empty
        if len(dict_authors_set[key]) != 0:
            # Create sorted tuples between the author and his coauthors
            new_edges = [tuple(sorted((dictionary_a_id[key], dictionary_a_id[co]))) for co in dict_authors_set[key]]
            
            # Update the set in order to not have the double arches
            edges.update(new_edges)
      
    return edges
    
    
def create_simple_graph(dictionary_id_a, edges):
    """This function returns a simple graph.
    
    It takes as inputs:
    @dictionary_id_a: dictionary (ID, author)
    @edges: set of edges"""
    
    # Initialize the graph
    G=nx.Graph()
    
    # Add nodes to the graph
    G.add_nodes_from(list(dictionary_id_a.keys()))
    
    # Get the list of edges
    edges_list = list(edges)
    
    # Add edges to the graph
    G.add_edges_from(edges_list)
    
    print (nx.info(G))
    
    return G
    


        