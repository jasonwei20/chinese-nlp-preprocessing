# chinese-nlp-preprocessing

Simple preprocessing for NLP in Chinese. Inputs a folder of txt files and outputs a folder of processed txt files.

Do the following:

1. Copy chinese text data into `/data`.

2. Run `python 1_replace_person_names_multiprocessing.py`. This processes all the txt files in the `/data` folder by replacing person names with "_ 人名 _", and outputs txt files in `/no_names_data`. This is very slow, even with multiprocessing. On my 8-core CPU it took ~45 seconds to process 6 MB of data, which translates to roughly 2 hours to process 1 GB of data. Try `python replace_person_names_multiprocessing_manual.py` if the above doesn't work. The manual version counts the number of cores and then processings chunks at a time based on the number of cores, compared to just letting the computer figure it out on its own. They took roughly the same amount of time on my test sample of text data.

Inputs `/data/`, outputs `/no_names_data/`

3. Run `python 2_weibo.py` (written by Chengyu) to create the pickle file in `/processed1`. Make sure the size of the file looks right, and that you're taking data from the right input folder.

Inputs `/no_names_data/`, outputs `/processed_1/`

4. Run `python 3_frequency_distribution.py` (slight modification of https://github.com/johnsonice/Chatbot_hred/blob/master/seq2seq/data_util/combine_datas.py) to generate a frequency distribution of the words and word groups. In particular, we are interested in `bad_words`, the set of words with less than median frequency. This reads in the txt files in `/no_names_data` and outputs `/processed2/vocab.p`.

Inputs `/processed_1/`, outputs `/processed_2/`

5. Run `python 4_delete_low_freq_words.py`. This reads in `bad_words` and deletes lines that contain any of them. Effectively, we reduced our vocabulary size by 50%. The input is the txt files `/no_names_data` and the output is txt files in `/filtered_data`. This probably has terrible runtime, worse than step 2. Took ~140 seconds to process 24 MB of data on one file, which translates to roughly 1.5 hours to process one gigabyte of data, but will probably be slower with a larger vocabulary.

Inputs `no_names_data` and `/processed_2/`, outputs `/filtered_data/`.

6. Run `python 5_create_new_pickle.py`. This reads in all the txt data from `/filtered_data` and outputs `/output_pickle/processed_tokens.p`. Also run `python 6_no_punctuation_create_new_pickle.py` to get the version with no punctuation.




So the final processed txt files are in the folder `/filtered_data`.

The final processed pickle files are in the folder `output_pickle/`

To run all lines of code, run `python 1_replace_person_names_multiprocessing.py; python 2_weibo.py; python 3_frequency_distribution.py; python 4_delete_low_freq_words.py; python 5_create_new_pickle.py; python 6_no_punctuation_create_new_pickle.py`

Total run time: terrible, but should be able to process 10 GB of data in a day or two if I had to guess.

Lots of code from https://github.com/johnsonice/Chatbot_hred.
