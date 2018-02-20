#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:58:35 2018

@author: huang
"""

### helper.py, process data, and batch data 
#import os,sys,inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir) 
import os 
#import random 
import re 
#import pickle 
#from collections import Counter
import  user_replace
import jieba
USER_DICT = 'userdict.txt'
jieba.load_userdict(USER_DICT)

LINE_FILE = 'xiaohuangji50w_nofenci.conv'
OUT_FILE = '../xiaohuangji.txt'

filter_words = ['=','mmmmmmmmmmmm','***','^','T_T','，，，','╭(╯ε╰)╮','。。。。','xxx','鸡']
#%%
#########################################
## process cornell movie - dialogs data #
#########################################


def replace_tokens(text,replace_dict):
    for k,v in replace_dict.items():
        pattern = re.compile("|".join(v)) 
        text = pattern.sub(k,text)
    
    return text

def check_filter(filter_words,text):
    for f in filter_words:
        if f in text:
            return False

    return True ## keep if no filter words 

def clear_convs(filter_words,convs):
    # clear all answers with filter words 
    convs = [c for c in convs if check_filter(filter_words,c[1])]
    #convs = [c for c in convs if c[1][0] != "="]
    # clear if ask sentence is only one word
    convs = [c for c in convs if len(c[0]) != 1]
    
    return convs

def get_lines():
    #id2line = {}
    file_path = os.path.join(LINE_FILE)
    with open(file_path, 'r',encoding='utf-8',errors='replace') as f:
        text = f.read()
        text = replace_tokens(text,user_replace.replace_dict)
        lines = text.split('\nE')
        convs = [l.split('\nM') for l in lines]
        convs = [[s.strip() for s in conv if s != '' and s!= 'E'] for conv in convs]
        convs = clear_convs(filter_words,convs)
        #convs = [[list(jieba.cut(s)) for s in conv] for conv in convs]
    return convs



#%%
## write to txt file 
convs = get_lines()
with open(OUT_FILE,'w') as f:
    for c in convs:
        for s in c:
            f.write(s+'\n')
        f.write('\n')

