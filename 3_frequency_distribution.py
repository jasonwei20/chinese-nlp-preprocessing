#Author: Jason Wei
#Date: Dec. 20, 2017
#This generates a frequency distribution from a folder of chinese text files.

import pickle
import os
from collections import Counter

# combine all processed token data and build vocabulary
data_path = ['./processed1/processed_tokens.p']
PROCESSED_PATH = './processed2/'

fraction = 3

############################# METHODS WRITTEN BY CHENGYU #############################

def load_training_data(train_token_path):
    train_enc_tokens, train_dec_tokens, test_enc_tokens, test_dec_tokens = pickle.load(open(train_token_path, 'rb'))
    return train_enc_tokens, train_dec_tokens, test_enc_tokens, test_dec_tokens

def combine_pickles(data_path):
    train_enc, train_dec, test_enc, test_dec = [], [], [], []
    for p in data_path:
        train_enc_tokens, train_dec_tokens, test_enc_tokens, test_dec_tokens = load_training_data(p)
        train_enc.extend(train_enc_tokens)
        train_dec.extend(train_dec_tokens)
        test_enc.extend(test_enc_tokens)
        test_dec.extend(test_dec_tokens)
        #print(len(train_enc), len(train_dec))

    assert len(train_enc) == len(train_dec)
    assert len(test_enc) == len(test_dec)

    save_file_path = os.path.join(PROCESSED_PATH, 'processed_tokens.p')
    pickle.dump((train_enc, train_dec, test_enc, test_dec), open(save_file_path, 'wb'))
    return train_enc, train_dec, test_enc, test_dec

########################
## Now build vocabulary
########################
CODES = {'<PAD>': 0, '<EOS>': 1, '<UNK>': 2, '<GO>': 3}

## a recursive function to flatten nested lists
def _flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in _flatten(i):
                yield j
        else:
            yield i

## ideally we want to drop those lines with low frequency words #modified by Jason
def build_vocab(pickle_file_path, CODES):
    tokens = pickle.load(open(pickle_file_path, 'rb'))
    all_words = []
    for t in tokens:
        all_words.extend(list(_flatten(t)))
    print('Finished flattening tokens.')


    #begin Jason's edits.

    all_words = Counter(all_words)
    print("Total vocabulary size:", len(all_words))

    # i want to get rid of half of the words so find the middle word
    vocab = sorted(all_words, key=all_words.get, reverse=True)
    vocab_to_int = {word: ii for ii, word in enumerate(vocab, len(CODES))}
    vocab_to_int = dict(vocab_to_int, **CODES)
    int_to_vocab = {v_i: v for v, v_i in vocab_to_int.items()}
    middle_word = int_to_vocab[int(len(int_to_vocab)/fraction)]
    one_half_threshold = all_words[middle_word]
    print("Frequency of the top 1/" + str(fraction) + " of words: " + str(one_half_threshold))

    good_words = {x: all_words[x] for x in all_words if all_words[x] > one_half_threshold} # vocab words that are in the upper half of the frequency distribution
    print("Filtered vocabulary size:", len(good_words))

    print("Frequency of _人名_", all_words["_人名_"])

    vocab = sorted(good_words, key=good_words.get, reverse=True)
    vocab_to_int = {word: ii for ii, word in enumerate(vocab, len(CODES))}
    vocab_to_int = dict(vocab_to_int, **CODES)
    int_to_vocab = {v_i: v for v, v_i in vocab_to_int.items()}

    bad_words = {x for x in all_words if all_words[x] <= one_half_threshold} #lower half of the frequency distribution

    save_file_path = os.path.join(PROCESSED_PATH, 'vocab.p')
    pickle.dump((vocab_to_int, int_to_vocab, bad_words), open(save_file_path, 'wb'))

    return vocab_to_int, int_to_vocab, bad_words

############################# END METHODS WRITTEN BY CHENGYU #############################

# main

_ = combine_pickles(data_path)
print('Finished combining data.')
del _  # clear memory
print('Memory Cleared.')

print('Building vocabulary...')
vocab_to_int, int_to_vocab, bad_words = build_vocab(os.path.join(PROCESSED_PATH, 'processed_tokens.p'), CODES)
print("Input from:", data_path)
print("Output from", PROCESSED_PATH)

#print(bad_words)


