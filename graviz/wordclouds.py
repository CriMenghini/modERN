#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

def get_keywords_by_years(data, left, right):
    """
    	Retrives the list of keywords used in the publications from `data`
    	dataset between the years `left` and `right`.
    """

    keywords = []
    for key in data.keys():
        try:
            pub_date = int(data[key]['Publication date'])
        except:
            continue
        if pub_date < left or pub_date > right:
            continue
        try:
            keywords += data[key]['Keywords']
        except:
            continue

    return keywords

def get_keywords_by_school(data, lab_school, school):
    """
    	Retrives the list of keywords used in the publications from `data`
    	dataset published by `school`.
    	In order to determine the school from the `data` dataset it needs to use
    	`lab_school` dictionary.
    """

    keywords = []
    for key in data.keys():
        try:
            sch = lab_school[list(data[key]['Labs involved'][0].keys())[0]]
        except:
            continue
        if sch != school:
            continue
        try:
            keywords += data[key]['Keywords']
        except:
            continue

    return keywords

if __name__ == "__main__":
    print('This is wordclouds library. Meant to be imported rather than\
    run directly')
