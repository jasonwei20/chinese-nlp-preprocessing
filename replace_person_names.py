#Author: Jason Wei
#Date: Dec. 19, 2017
#This code processes chinese text data by replacing names of people with a replacement word.

import os
from os import listdir
from os.path import isfile, join
import jieba.posseg as pseg
import time

def replace_names(line, replacement_word, num_replacements): # replace name of person with a replacement word, i.e. "_人名_"
    words = pseg.cut(line)
    no_names = ""
    for word in words:
        if word.flag == "nr":
            no_names += replacement_word
            num_replacements += 1
        else:
            no_names += word.word
    return no_names, num_replacements


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


###################### PROCESS TEXT ###########################################
print("Processing the following files:", data_files)
counter = 0
num_replacements = 0
start = time.time()

# loop through all the files in the dataset
for file in data_files:

    print("Processing", file)
    writefile = os.path.expanduser(no_names_location + file)
    writer = open(writefile, "w")

    with open(data_location + "/" + file, 'r', encoding='utf-8', errors='replace') as f:

        line = f.readline()
        while line is not "": # loop through lines
            new_line, num_replacements = replace_names(line, replacement_word, num_replacements)
            writer.write(new_line) # replace person's names
            line = f.readline()
            counter += 1
            if counter % 100000 == 0:
                print(counter, "lines processed.")

    writer.close()

print("Done processing text.")
print("Processing time: ", time.time() - start, "seconds for", counter, "lines with", num_replacements, "replacements.")


# test code
# replace_names("快乐女生, 谁是冠军?洪辰?刘昕失常啦!小段差点。刘昕明显后劲不足, 小段倒是爆发力十足, 洪辰和魏晨怎么感觉夜店味这么浓呢 我倒没看好段, 出乎意料她进了二强, 可惜了刘昕 最后就看段林希和洪辰了, 洪辰得冠军的可能性大点感觉", replacement_word)

# text = f.read()
# new_text, num_replacements = replace_names(text, replacement_word, num_replacements)
# writer.write(new_text)