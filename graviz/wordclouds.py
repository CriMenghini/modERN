#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

def get_keywords_by_years(data, left, right):
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
