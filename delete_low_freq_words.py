#Author: Jason Wei
#Date: Dec. 20, 2017
#This code deletes lines containing words of low frequency.

import pickle
import os
from os import listdir
from os.path import isfile, join
import jieba
jieba.initialize()
import jieba.posseg as pseg
jieba.suggest_freq('_人名_', True)
import time
import multiprocessing
from multiprocessing import Pool


pickle_in = open("./processed2/vocab.p","rb")
vocab_to_int, int_to_vocab, bad_words = pickle.load(pickle_in)
print("Finish loading bad_words of size:", len(bad_words), "words.")

# methods

def no_bad_words(line): # replace name of person with a replacement word, i.e. "_人名_"
    words = pseg.cut(line)
    for word in words:
        if word.word in bad_words:
            return False
    return True

def process(file): #process one text file

    print("Start processing", file)
    writefile = os.path.expanduser(no_bad_words_location + file)
    writer = open(writefile, "w")

    with open(data_location + "/" + file, 'r', encoding='utf-8', errors='replace') as f:

        line = f.readline()
        while line is not "": # loop through lines
            if no_bad_words(line): # write the line if it doesn't have bad words
                writer.write(line)

            line = f.readline()

    print("End processing", file)
    writer.close()


# open folders, etc.
data_location = "./no_names_data"
no_bad_words_location = "./filtered_data/"
data_folder = os.path.expanduser(data_location)
new_data_folder = os.path.expanduser(no_bad_words_location)

data_files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]

if '.DS_Store' in data_files: # delete this file, but might not exist
    data_files.remove('.DS_Store')

# process data

num_cores = multiprocessing.cpu_count()
print("Begin multiprocessing with", num_cores, "cores.")

print("Processing the following files:", data_files)
start = time.time()

chunks = [data_files[x:x+num_cores] for x in range(0, len(data_files), num_cores)] #process the files in chunks of size equal to the number of cores on the cpu.
print("Processing", num_cores, "files at a time.")

p = Pool(num_cores)

for i in range(len(chunks)):
    print("Processing chunk", i+1, "of", len(chunks))
    chunk = chunks[i]
    p.map(process, chunk)

print("Done processing text.")
print("Processing time: ", time.time() - start)
