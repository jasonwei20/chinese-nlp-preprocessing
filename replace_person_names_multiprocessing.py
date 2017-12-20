#Author: Jason Wei
#Date: Dec. 20, 2017
#This code processes chinese text data by replacing names of people with a replacement word. Attempts to use multiprocessing.

import os
from os import listdir
from os.path import isfile, join
import jieba
jieba.initialize()
import jieba.posseg as pseg
import time
from multiprocessing import Pool

def replace_names(line, replacement_word): # replace name of person with a replacement word, i.e. "_人名_"
    words = pseg.cut(line)
    no_names = ""
    for word in words:
        if word.flag == "nr":
            no_names += replacement_word
        else:
            no_names += word.word
    return no_names

def process(file): #process one text file

    print("Start processing", file)
    writefile = os.path.expanduser(no_names_location + file)
    writer = open(writefile, "w")

    with open(data_location + "/" + file, 'r', encoding='utf-8', errors='replace') as f:

        line = f.readline()
        while line is not "": # loop through lines
            new_line = replace_names(line, replacement_word)
            writer.write(new_line) # replace person's names
            line = f.readline()

    print("End processing", file)
    writer.close()


# begin main

replacement_word = "_人名_"
print("Changing person names to " + replacement_word + "...")

# open folders, etc.
data_location = "./data"
no_names_location = "./no_names_data/"
data_folder = os.path.expanduser(data_location)
new_data_folder = os.path.expanduser(no_names_location)

data_files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]

if '.DS_Store' in data_files: # delete this file, but might not exist
    data_files.remove('.DS_Store')


# process data

print("Processing the following files:", data_files)
start = time.time()

cores = len(data_files)
p = Pool(cores)
p.map(process, data_files)

print("Done processing text.")
print("Processing time: ", time.time() - start)


















# test code
# replace_names("快乐女生, 谁是冠军?洪辰?刘昕失常啦!小段差点。刘昕明显后劲不足, 小段倒是爆发力十足, 洪辰和魏晨怎么感觉夜店味这么浓呢 我倒没看好段, 出乎意料她进了二强, 可惜了刘昕 最后就看段林希和洪辰了, 洪辰得冠军的可能性大点感觉", replacement_word)

# text = f.read()
# new_text, num_replacements = replace_names(text, replacement_word, num_replacements)
# writer.write(new_text)