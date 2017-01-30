# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 23:10:47 2017

@author: cristinamenghini
"""
# MULTIGRAPH
import json
from BuildGraphModule import *
from UniformData import *
import requests
from bs4 import BeautifulSoup

def get_collaborators(data):
    """ This function provides a dictionary (author, list of collabrators with information)"""
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
                dict_authors_epfl[a] += [{j:p} for j in list_authors if j != a]

        # If there re not epfl authors continue the loop
        except:
            continue
            
    return dict_authors_epfl
    
def coauthorship_papers(dict_authors_epfl):
    """ This function """
    dict_coautorship_papers = {}
    for author in list(dict_authors_epfl.keys()):

        dict_papers = defaultdict(list)
        for i in range(len(dict_authors_epfl[author])):

            coauthor = list(dict_authors_epfl[author][i].keys())[0]

            dict_papers[coauthor] += [(dict_authors_epfl[author][i])[coauthor]]

        dict_coautorship_papers[author] = dict_papers
    
    return dict_coautorship_papers
    
def paper_per_author(dict_coautorship_papers):
    """ This function"""
    
    # Get list of paper for author
    list_paper = defaultdict(list)
    # For each paper get the list of papers
    for author in list(dict_coautorship_papers.keys()):
        list_paper[author] += [dict_coautorship_papers[author][i] for i in dict_coautorship_papers[author]]
    
    # Take the set to avoid duplicates
    for a in list(list_paper.keys()):
        list_paper[a] = set([j for i in list_paper[a] for j in i])
        
    return list_paper
    

def lab_site(data):
    """ This function .."""
    
    # (lab,website)
    dict_author_site = {}
    for paper in list(data.keys()):
        try:
            # Whether there is only one lab in the page
            if len(data[paper]['Epfl authors']) == 1:
                dict_author_site[list(data[paper]['Epfl authors'][0].keys())[0]] = list(data[paper]['Epfl authors'][0].values())[0]
            
            # Otherwise
            else:
                #print ('else')
                for lab in data[paper]['Epfl authors']:
                    dict_author_site[list(lab.keys())[0]] = list(lab.values())[0]  
        except:
            continue
        
    return dict_author_site
    
    
def get_authors_lab(list_paper, data):
    """ This function ..."""
    
    
    author_lab = {}
    site_lab = {}
    for a in list(list_paper.keys()):
        try:
            for p in list_paper[a]:
                if len(data[p]['Labs involved']) <= 1:
                    author_lab[a] =  list(data[p]['Labs involved'][0].keys())[0]

                    break
                else:
                    print ('else')
                    req = requests.get(dict_author_site[a])
                    html = req.content
                    soup = BeautifulSoup(html, 'html.parser')
                    #print (soup)
                    try:
                        #print ('try')
                        for i in soup.findAll('div', {'class':'topaccred'})[0]:

                            try:
                                author_lab[a] = site_lab[i]
                                break
                            except:
                                print (i.get('href'))
                                req = requests.get(i.get('href'))
                                html = req.content
                                soup = BeautifulSoup(html, 'html.parser')
                                author_lab[a] = soup.findAll('h2')[0].text.replace('\n',' ').split('  ')[0]
                                site_lab[i] = soup.findAll('h2')[0].text.replace('\n',' ').split('  ')[0]
                                break


                    except:
                        continue

        except:
            continue
            
    return author_lab, site_lab
    
    
def lab_dictionaries(data_cut):
    
    # (lab,website)
    dict_lab_site = {}
    # (lab, num publications)
    dict_labs = defaultdict(int)
    # (lab, list of papers)
    dict_labs_paper = defaultdict(list)
    
    for paper in list(data_cut.keys()):
        try:
            if len(data_cut[paper]['Labs involved']) == 1:
                dict_lab_site[list(data_cut[paper]['Labs involved'][0].keys())[0]] = list(data_cut[paper]['Labs involved'][0].values())[0]
                dict_labs[list(data_cut[paper]['Labs involved'][0].keys())[0]] += 1
                dict_labs_paper[list(data_cut[paper]['Labs involved'][0].keys())[0]] += [paper]

            else:
                #print ('else')
                for lab in data_cut[paper]['Labs involved']:
                    dict_lab_site[list(lab.keys())[0]] = list(lab.values())[0]     
                    dict_labs[list(lab.keys())[0]] += 1
                    dict_labs_paper[list(lab.keys())[0]] += [paper]
        except:
            continue
    
    return dict_lab_site, dict_labs, dict_labs_paper
    
    
def traverse_epfl_tree(root):
    global prova
    
    #Request root url
    request = requests.get(root)
    html = request.content
    #get the soup
    soup = BeautifulSoup(html, 'html.parser')
    
    #find eventual children
    children = soup.findAll("div", { "class" : "unit_name" })
    #check if node is a leaf
    
    is_leaf = (len(children) == 0)
    #print (is_leaf)
    #parse and add node to the db (see def of create_node)
    
    #create_node(soup, is_leaf) # save data 
    
    if is_leaf == False:
        #continue exploring the tree
        for elem in children:
            print (soup.findAll('h2')[0].text.replace('\n',' ').split('  ')[0])
            prova[soup.findAll('h2')[0].text.replace('\n',' ').split('  ')[0]] += [elem.findAll('a')[0].text.strip()]
            #print (elem)
            traverse_epfl_tree("https://search.epfl.ch" + elem.find('a').get('href'))


#dictionary = {}
#dictionary_occ = {}
#for i in list(dict_coautorship_papers.keys()):
#    dictionary[i] = {}
#    dictionary_occ[i] = {}
#    for j in list(dict_coautorship_papers[i].keys()):
#        dates = defaultdict(list)
#        for l in range(len(dict_coautorship_papers[i][j])):
#            try:
#                dates[data[sorted(dict_coautorship_papers[i][j])[l]]['Publication date']] += [sorted(dict_coautorship_papers[i][j])[l]]
#            except:
#                continue
#        if len(dates) != 0:
#            dictionary[i][j] = dates
#            dictionary_occurences = {}
#            for k,m in dictionary[i][j].items():
#                dictionary_occurences[k] = len(m)
#            dictionary_occ[i][j] = dictionary_occurences
#            
            
## Define an epty set of edges
#edges = set()
#
## For each author
#for key in list(dict_authors_set_epfl.keys()):       
#    # If the list of co-authors is not empty
#    if len(dict_authors_set_epfl[key]) != 0:
#        # Create sorted tuples between the author and his coauthors
#        new_edges = [tuple(sorted((dictionary_a_id_epfl[key], dictionary_a_id_epfl[co]))) for co in dict_authors_set_epfl[key]]
#
#        # Update the set in order to not have the double arches
#        edges.update(new_edges)
#        
#        
#G_epfl = nx.MultiGraph()
#G_epfl.add_nodes_from(list(dictionary_id_a_epfl.keys()))
#G_epfl.add_edges_from(list(edges_epfl))
#
#new_edges = []
#to_remove = []
#for i,j in list(edges_epfl):
#    
#    try:    
#        for k in list(dictionary_occ[dictionary_id_a_epfl[i]][dictionary_id_a_epfl[j]].keys()):
#        #print (list(dictionary_occ[dictionary_id_a_epfl[i]][dictionary_id_a_epfl[j]].keys()))
#        #print (i,j)
#            new_edges += [(i, j, dict(year = k))]
#            to_remove += [(i,j)]
#    except:
#        continue
#    
#G_epfl.add_edges_from(new_edges)
##G_epfl.remove_edges_from(set(to_remove))
#
#
#for i,j in G_epfl.edges():
#    for k in G_epfl[i][j]:
#        #print (k)
#        if k == 0:
#            G_epfl[i][j][k]['weight'] = dict_numb_coll_epfl[dictionary_id_a_epfl[i]][dictionary_id_a_epfl[j]]
#        else:
#            #print (G_epfl[i][j][k]['year'])
#            G_epfl[i][j][k]['weight'] = dictionary_occ[dictionary_id_a_epfl[i]][dictionary_id_a_epfl[j]][G_epfl[i][j][k]['year']]
#    
#    
#for i,j in G.edges():
#    for k in G[i]:
#        #print (k)
#        
#        G[i][j]['weight'] = dict_numb_coll_epfl[dictionary_id_a_epfl[i]][dictionary_id_a_epfl[j]]
#            
