# chinese-nlp-preprocessing

Simple preprocessing for NLP in Chinese. Inputs a folder of txt files and outputs a folder of processed txt files.

Do the following:

`python replace_person_names_multiprocessing`

This processes all the txt files in the `data` folder by replacing person names with "_ 人名 _", and outputs txt files in `no_names_data`. This is very slow, even with multiprocessing. On my 8-core CPU it took ~45 seconds to process 6 MB of data, which translates to roughly 2 hours to process 1 GB of data. Try `python replace_person_names_multiprocessing_manual` if the above doesn't work. The manual version counts the number of cores and then processings chunks at a time based on the number of cores, compared to just letting the computer figure it out on its own. They took roughly the same amount of time on my test sample of text data.

Some code from https://github.com/johnsonice/Chatbot_hred
