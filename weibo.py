#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 21:06:55 2017

@author: chengyu
"""


import os 
import pickle 
#from collections import Counter
#import user_replace
import jieba
import re
from multiprocessing import Pool 

#%%

# parameters for processing the dataset
DATA_PATH = './no_names_data/'
USER_DICT = './userdict.txt'
PROCESSED_PATH = './processed1'
ENCODING = 'utf-8'
jieba.load_userdict(USER_DICT)

DELETE = ['\[.*?\]','\u200b']
MULTI = False

#%%
def replace_tokens(text,replace_dict=None):
#    for k,v in replace_dict.items():
#        pattern = re.compile("|".join(v)) 
#        text = pattern.sub(k,text)
    
    pattern = re.compile("|".join(DELETE)) 
    text = re.sub(pattern,'',text)
    return text

def read_txt(file_path,encoding):
    with open(os.path.join(DATA_PATH,file_path), 'r',encoding=encoding,errors='replace') as f:
        text = f.read()
        
        text = replace_tokens(text) #,user_replace.replace_dict
        convs = text.split('\n\n')
        lines = [c.split('\n') for c in convs]
        lines = [[i.strip() for i in c if i != ''] for c in lines] ## get ride of empties sentences
        lines = [c for c in lines if len(c)>1]
    return lines

def context_answers(convos):
    context,answers = [],[]
    for convo in convos:
        for index,line in enumerate(convo[:-1]):
            context.append(line)
            answers.append(convo[index+1])
        
    assert len(context) == len(answers)
    return context,answers

def _basic_tokenizer(line,normalize_digits=False):
    """
    A basic tokenizer to tokenize text into tokens
    """    
    _DIGIT_RE = re.compile(r"\d+")  ## find digits 
    
    words = []
    tokens = list(jieba.cut(line.strip().lower()))
    if normalize_digits:
        for token in tokens:
            m = _DIGIT_RE.search(token)
            if m is None:
                words.append(token)
            else:
                words.append('_数字_')
    else:
        words = tokens 
    
    return words 

def _tokenized_data(context,answers):
    
    train_enc_tokens = [_basic_tokenizer(t) for t in context]
    print('Train_enc_token done.')
    
    train_dec_tokens = [_basic_tokenizer(t) for t in answers]
    print('Train_dec_token done.')
    
    return train_enc_tokens, train_dec_tokens

def save_tokenized_data(train_enc_tokens,train_dec_tokens,save_file_name):
    save_file_path = os.path.join(PROCESSED_PATH,save_file_name)
    pickle.dump((train_enc_tokens, train_dec_tokens,[],[]),open(save_file_path,'wb'))
    print('Data saved')
#%%
data_files = os.listdir(DATA_PATH)[:]  ## just do two files for now, too many data
#%%
asks,ans = [],[]
for idx,file_path in enumerate(data_files):
    #file_path = 'multi_1_4.data'
    convos = read_txt(file_path,ENCODING)
    context,answers = context_answers(convos)
    
    asks.extend(context)
    ans.extend(answers)
    print('finish {}'.format(file_path))

if MULTI:
    print('tokanizing, multi process')
    cores = 30 
    p = Pool(cores)
    context = p.map(_basic_tokenizer,asks)
    print('Finish tokenizing ask sentences')
    answers = p.map(_basic_tokenizer,ans)
    print('Finish tokenizing answer sentences')
else:
    context,answers = _tokenized_data(asks,ans) 

## save into pickles
save_tokenized_data(context,answers,'processed_tokens.p')
    
#%%
#print(context[:50])
#print(answers[:50])
