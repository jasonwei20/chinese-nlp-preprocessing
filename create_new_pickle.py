#Author: Jason Wei
#Date: Jan. 3, 2017
#This creates the new pickle file.


#copy from weibo

import os
import pickle
import jieba

jieba.suggest_freq('_人名_', True)
import re
from multiprocessing import Pool

# parameters for processing the dataset
DATA_PATH = './filtered_data/'
USER_DICT = './userdict.txt'
PROCESSED_PATH = './processed3'
ENCODING = 'utf-8'
jieba.load_userdict(USER_DICT)

DELETE = ['\[.*?\]', '\u200b']
MULTI = True


# %%
def replace_tokens(text, replace_dict=None):
    #    for k,v in replace_dict.items():
    #        pattern = re.compile("|".join(v))
    #        text = pattern.sub(k,text)

    pattern = re.compile("|".join(DELETE))
    text = re.sub(pattern, '', text)
    return text


def read_txt(file_path, encoding):
    with open(os.path.join(DATA_PATH, file_path), 'r', encoding=encoding, errors='replace') as f:
        text = f.read()

        text = replace_tokens(text)  # ,user_replace.replace_dict
        convs = text.split('\n\n')
        lines = [c.split('\n') for c in convs]
        lines = [[i.strip() for i in c if i != ''] for c in lines]  ## get ride of empties sentences
        lines = [c for c in lines if len(c) > 1]
    return lines


def context_answers(convos):
    context, answers = [], []
    for convo in convos:
        for index, line in enumerate(convo[:-1]):
            context.append(line)
            answers.append(convo[index + 1])

    assert len(context) == len(answers)
    return context, answers


def _basic_tokenizer(line, normalize_digits=False):
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


def _tokenized_data(context, answers):
    train_enc_tokens = [_basic_tokenizer(t) for t in context]
    print('Train_enc_token done.')

    train_dec_tokens = [_basic_tokenizer(t) for t in answers]
    print('Train_dec_token done.')

    return train_enc_tokens, train_dec_tokens


def save_tokenized_data(train_enc_tokens, train_dec_tokens, save_file_name):
    save_file_path = os.path.join(PROCESSED_PATH, save_file_name)
    pickle.dump((train_enc_tokens, train_dec_tokens, [], []), open(save_file_path, 'wb'))
    print('Data saved')


# %%
data_files = os.listdir(DATA_PATH)[:]  ## just do two files for now, too many data
# %%
asks, ans = [], []
for idx, file_path in enumerate(data_files):
    # file_path = 'multi_1_4.data'
    convos = read_txt(file_path, ENCODING)
    context, answers = context_answers(convos)

    asks.extend(context)
    ans.extend(answers)
    print('finish {}'.format(file_path))

if MULTI:
    print('tokanizing, multi process')
    cores = 30
    p = Pool(cores)
    context = p.map(_basic_tokenizer, asks)
    print('Finish tokenizing ask sentences')
    answers = p.map(_basic_tokenizer, ans)
    print('Finish tokenizing answer sentences')
else:
    context, answers = _tokenized_data(asks, ans)

## save into pickles
save_tokenized_data(context, answers, 'processed_tokens.p')








import pickle
import os
from collections import Counter

# combine all processed token data and build vocabulary
data_path = ['./processed3/processed_tokens.p']
PROCESSED_PATH = './processed4/'


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

    print("Frequency of _人名_", all_words["_人名_"])

    save_file_path = os.path.join(PROCESSED_PATH, 'vocab.p')
    pickle.dump((vocab_to_int, int_to_vocab), open(save_file_path, 'wb'))

    return vocab_to_int, int_to_vocab

############################# END METHODS WRITTEN BY CHENGYU #############################

# main

_ = combine_pickles(data_path)
print('Finished combining data.')
del _  # clear memory
print('Memory Cleared.')

print('Building vocabulary...')
vocab_to_int, int_to_vocab = build_vocab(os.path.join(PROCESSED_PATH, 'processed_tokens.p'), CODES)

#print(bad_words)


