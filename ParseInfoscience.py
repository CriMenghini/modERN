# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:31:50 2017

@author: cristinamenghini
"""
 
from bs4 import BeautifulSoup
import codecs

# Define a class to parse infoscience html pages
# Define a class to parse infoscience html pages
class InfoscienceParser():
    
    """-------------------------------------------------------------------------------------------
    This class define the parser for Infoscience html pages.
    
    Each inspected page is related to a publication signed EPFL. The aim is to store the gathered in
    significant information into JSON file that can be helpful in the construction of the graph."""
    
    
    def __init__(self, path, html, list_file):
        """ An instance created by that class is characterized by the following 
        attributes:
        
        @path: path of html folder
        @title: title of the publication
        @kind: kind of publication
        @date_publication: date of publication
        @authors: authors of the work
        @event: event the work has been published in
        @abstract: abstract of the paper
        @keywords: words which describe the publication
        @labs: labs the work has been developed in
        @epfl_authors: authors in EPFL
        @html: index of the file
        @list_file: list of html pages"""
        
        self.title = ""
        self.kind = ""
        self.date_publication = ""
        self.authors = []
        self.abstract = ""
        self.keywords = ""
        self.labs = []
        self.epfl_authors = ""
        self.path = path
        self.html = html
        self.list_file = list_file
        
    
    def import_html(self):
        """ This fuction open the html source to parse, create the soup and returns it."""
        
        # Open the source html
        html_source = codecs.open(self.path + self.list_file[self.html], 'r')
        
        # Create the soup
        soup = BeautifulSoup(html_source, 'html.parser')
        
        return soup
    
    
    def get_kind_publication(self, soup):
        """ This function get the kind of publication and returns it.
        
        It takes as input:
        @soup: the source html code"""
        
        # Verify whether the page is empty or not
        try:
            self.kind = soup.findAll("div", { "class" : "doctype local-color" })[0].contents
        
        except IndexError:
            return ('The page is empty.')
        
        # Exclude the publication whether it is a book or  deleted publication
        if self.kind[0] == 'Book' or  self.kind[0] == 'Record':                     
            return 'The publication is a book or an deleted pubication. Thus, we discard it.'              
        
        # Return it whether it's the kind of publication we are interested in
        else:
            return self.kind[0]
        
    def get_title_publication(self, soup):
        """ This function returns the title of the publication.
        
        It takes as input:
        @soup: the source html code"""
        
        # Get the title
        self.title = soup.findAll("h1", { "class" : "h2" })[0].contents
        
        return self.title[0]
    
    def get_authors(self, soup):
        """ This function returns the list of authors of the work.
        
        It takes as input:
        @soup: the source html code"""
        
        # Get the list of authors        
        raw_authors = soup.findAll("div", { "class" : "authors" })[0].findAll("a")
        
        # For each author replace the comma with blank space and strip
        self.authors = [author.contents[0].replace(",", "").strip() for author in raw_authors]
        
        return self.authors
    
    def get_publication_date(self, soup):
        """ This function returns the year of the publication.
        
        It takes as input:
        @soup: the source html code"""
        
        # Check whether extra information is reported
        try:
            meta_data = soup.findAll("ul", { "class" : "record-metadata" })[0].findAll('li')
            
            # Go through the extra information and keep the date
            for i in meta_data:
                # Split the string
                split_info = i.text.split(':')
                
                # If there is the publication date
                if split_info[0].strip() == 'Publication date':                    
                    # Add to the dictionary
                    self.date_publication = split_info[1].strip()
                    # Return it
                    return self.date_publication
                
                # Otherwise define the variable as empty
                else:
                    self.date_publication = None
            
            # Whether no date is present
            if self.date_publication == None:
                return 'The publication date is not specified.'
        
        except IndexError:
            return 'The publication date is not specified.'
        
    def get_abstract(self, soup):
        """ This function returns the abstract of the publication.
        
        It takes as input:
        @soup: the source html code"""
        
        # Check the presence of the article
        try:
            self.abstract = soup.findAll("div", { "class" : "record-container" })[0].findAll('p')[0].text
            return self.abstract
            
        except:
            return ('The abstract is not present in the page.')
        
    def get_keywords(self, soup):
        """ This function returns the keywords of the work.
        
        It takes as input:
        @soup: the source html code"""
        
        # For the elements in 'p' class
        for i,j in list(enumerate(soup.findAll("p"))):
            
            # Whether the class is present
            try:
                is_keyword = j.findAll('span')[0].text
                # If it contains the keywords
                if is_keyword == 'Keywords:':
                    # Get them
                    raw_keywords = soup.findAll("p")[i].findAll('a')
                    # And add create the list
                    self.keywords = [i.text.strip() for i in raw_keywords]
                    return self.keywords
                # Otherwise define the variable as empty  
                else:
                    self.keywords = None
                    
            except:
                continue
        
        if self.keywords == None:
            return ('The page doesn"t mention keywords.')
        
    def get_labs_epfl_authors(self, soup):
        """ This function returns the lists of epfl authors and labs which are involved in the publication.
        
        It take as input:
        @soup: the source html code"""
        
        # Get the a part of content of the right box of the page
        right_box = soup.findAll("div", { "class" : "box" })[-1]
        
        # If it contains informations about the labs and epfl authors
        if right_box.h3.text.strip() == 'Contacts' or right_box.h4.text.strip() == 'EPFL authors':
            # Initialize the list to store the information
            epfl_authors_list = []
            labs_list = []
            
            # For each element of interest
            for link in right_box.findAll('a'):
                # If the provided link refers to a person who works at epfl 
                if link.get('href')[7:13] == 'people':
                    # Add it to the list (both the name and the reference link)
                    epfl_authors_list += [{link.text.replace(',','') : link.get('href')}]
                # Otherwise we get the labs information
                else:
                    # And add them to the list (storing both the name and the reference link)
                    labs_list += [{link.text: link.get('href')}]
        
            return epfl_authors_list, labs_list
        
        else:
            return ('The page doesn"t contain addictional information.')
        
           
    def parse_html(self):
        """ This function return a dictionary which contains all the relevant information related to the publication
        that is mentioned in the web page."""
        
        # Get the soup to parse
        soup = self.import_html()
        
        # Initialize the dictionary which will contains information related to the publication
        paper = {}
        
        # Get kind of publication
        kind = self.get_kind_publication(soup)
        
        # Check whether the kind of publication is interesting
        if kind[:3] != 'The':
            paper['Kind of pubblication'] = kind
        else:
            return kind
       
        # Get the title 
        paper['Title'] = self.get_title_publication(soup)
        
        # Get the list of authors        
        paper['Authors'] = self.get_authors(soup)
        
        # Get the publication date
        date = self.get_publication_date(soup)
        # Check whether the date is present
        if date[:3] != 'The':
            paper['Publication date'] = date
        
        # Get the abstract of the paper
        abstract_return = self.get_abstract(soup)
        # Check whether the abstract is present
        if abstract_return[:3] != 'The':
            paper['Abstract'] = abstract_return
        
        
        # Get the keywords
        keywords = self.get_keywords(soup)
        # check whether the keywords are inserted
        if keywords[:3] != 'The':
            paper['Keywords'] = keywords
        
        # Get epfl authors
        return_function = self.get_labs_epfl_authors(soup)
        len_return = len(return_function)
        
        # If the function has returned the lists of interest append them to the dictionary
        if len_return <= 2:            
            if len(return_function[0]) != 0:
                paper['Epfl authors'] = return_function[0]
            
            if len(return_function[1]) !=0:
                paper['Labs involved'] = return_function[1]
    
        return paper  