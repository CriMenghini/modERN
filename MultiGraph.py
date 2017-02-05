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
import pickle
from bs4 import BeautifulSoup

def get_collaborators(data):
    """ This function provides a dictionary (author, list of collabrators with information).
    It takes as input:
    @data: the load data"""
    
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


def cut_data(data, year=1993):
    """ This function return a reduce dataset according to the year we want to keep.
    It takes as input:
    @data: entire dataset
    @year: year to start from"""
    
    data_cut = {}
    # For each paper, keep it if the year is greater than..
    for paper in list(data.keys()):
        try:
            if int(data[paper]['Publication date']) >= year:
                data_cut[paper] = data[paper]
        except:
            continue

    return data_cut
    
def coauthorship_papers(dict_authors_epfl):
    """ This function returns the dictionary (author, dict(collaborator,list of common works)).
    It takes as input:
    @dict_authors_epfl: dictionary (author, list collaborators with info)"""
    
    dict_coautorship_papers = {}
    # For each EPFL author
    for author in list(dict_authors_epfl.keys()):

        dict_papers = defaultdict(list)
        
        # For each author who contibuted to the work
        for i in range(len(dict_authors_epfl[author])):

            coauthor = list(dict_authors_epfl[author][i].keys())[0]
            # Add instan in dict_papers
            dict_papers[coauthor] += [(dict_authors_epfl[author][i])[coauthor]]
        
        # Add the dictionary to the final dictionary
        dict_coautorship_papers[author] = dict_papers
    
    return dict_coautorship_papers
    
    
def paper_per_author(dict_coautorship_papers):
    """ This function returns (author, set of papers).
    It takes as input:
    @dict_coautorship_papers: dictionary (author, dict(collaborator,list of common works))"""
    
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
    """ This function returns two dictionaries - one (author, lab) and another (lab, website)"""
    
    
    author_lab = {}
    site_lab = {}
    
    # For each author
    for a in list(list_paper.keys()):
        
        try:
            # For each paper signed by the author
            for p in list_paper[a]:
                # If the number of labs that took part is 0 or 1
                if len(data[p]['Labs involved']) <= 1:
                    # Get connecte the author to the lab
                    author_lab[a] =  list(data[p]['Labs involved'][0].keys())[0]
                    # ANd break the loop
                    break
                
                # Otherwise
                else:
                    # Get the html page of the author 
                    req = requests.get(dict_author_site[a])
                    html = req.content
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    
                    # We should go throuhg two html pages since the People html doesn't provide the entire name of the lab
                    try:
                        # Get the link of the lab where he works
                        for i in soup.findAll('div', {'class':'topaccred'})[0]:

                            try:
                                author_lab[a] = site_lab[i]
                                break
                            
                            except:
                                # And parse the html page of the lab to get the entire name of the lab
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
    
prova = defaultdict(list)
    
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


def lab_year_pub(dict_labs_paper, data_cut):
    """Get the list of paper lab and year. Dictionary (lab, dict(year, list of papers))"""
    
    dict_lab_years_pub = {}#defaultdict(list)
    for lab in dict_labs_paper:
        dict_lab_years_pub[lab] = defaultdict(list)
        for pub in dict_labs_paper[lab]:
            dict_lab_years_pub[lab][data_cut[pub]['Publication date']] += [pub]
            
    return dict_lab_years_pub


def year_papers_(dict_lab_years_pub):
    """Dictionary (year, total number of papers)"""
    
    year_papers = defaultdict(list)
    for lab in list(dict_lab_years_pub.keys()):
        for year in list(dict_lab_years_pub[lab].keys()):
            year_papers[year] += dict_lab_years_pub[lab][year]
    for year in list(year_papers.keys()):
        year_papers[year] = len(set(year_papers[year]))
        
    return year_papers


def lab_year(dict_labs_paper, data_cut):
    """Get dictionary (lab, dict(year,num of pubblication))"""
    
    # Get the dictionary (lab, dict(year, number of papers))
    dict_lab_years = defaultdict(list)
    for lab in dict_labs_paper:
        for pub in dict_labs_paper[lab]:
            dict_lab_years[lab] += [data_cut[pub]['Publication date']]
        dict_lab_years[lab] = collections.Counter(dict_lab_years[lab])
        #dict_lab_years[lab]['Total'] = sum(list(dict_lab_years[lab].values()))

    return dict_lab_years


def year_auth(dict_author_year):
    """Dictionary (year, number of authors)"""
    year_authors = defaultdict(int)
    for lab in list(dict_author_year.keys()):
        for year in list(dict_author_year[lab].keys()):
            year_authors[year] += dict_author_year[lab][year]
            
    return year_authors


# Dictionary (lab, dict(year, num authors))
def lab_author_year(dict_lab_years_pub, data_cut):
    
    
    dict_author_year = {}
    #dict_author_num_year = {}
    for lab in dict_lab_years_pub:
        dict_author_year[lab] = defaultdict(list)
        for year in list(dict_lab_years_pub[lab].keys()):
            try:
                dict_author_year[lab][year] += [list(a.keys()) for p in dict_lab_years_pub[lab][year] for a in data_cut[p]['Epfl authors']]
            except:
                dict_author_year[lab][year] += []
                continue
        for year in list(dict_lab_years_pub[lab].keys()):
            list_authors = [i[0] for i in dict_author_year[lab][year]]
            dict_author_year[lab][year] = len(set(list_authors))
            
    return dict_author_year


def getKey_0(item):
    return item[0]

def get_sorted_array(dict_school_pub):
    
    tuples_pr = dict_school_pub.items()
    sort = sorted(tuples_pr, key = getKey_0)
    x = [int(i[0]) for i in sort[:-1]]
    y = [i[1] for i in sort[:-1]]
    
    return y,x

def get_sorted_array_scaled(dict_school_pub, school, total_year):
    
    tuples_pr = dict_school_pub[school].items()
    sort = sorted(tuples_pr, key = getKey_0)
    x = [int(i[0]) for i in sort[:-1]]
    y = [i[1]/total_year[i[0]] for i in sort[:-1]]
    
    return y,x

