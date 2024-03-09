from time import time

cpoint = time()

import csv
from spacy import load
import re
from spacy.tokenizer import Tokenizer 
from token_exceptions import TOKENIZER_EXCEPTIONS
# from language_components.custom_tokenizer import *

def split_sentences(texts, nlp):
    sents = []
    for text in texts:
        tokens = [t for t in nlp(text)]
        curr_sent = []
        for t in tokens:
            if(t.is_sent_start):
                curr_sent.append(t)
            elif(t.is_sent_end):
                curr_sent.append(t)
                sents.append(curr_sent)
                curr_sent = []
            else:
                curr_sent.append(t)
        break
    print(sents)

print((time() - cpoint))

def read_csv_one_row_at_a_time(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Assuming the first row is a header

        for row in csv_reader:
            yield dict(zip(header, row))

data = []

        
nova = './src/backend/style_classification/data/news/csv/nova_articles.csv'
for row in read_csv_one_row_at_a_time(nova):
    data.append(row['content'])



def custom_tokenizer(nlp):
    prefix_re = re.compile(r'''^[\[\("'“„]''')
    suffix_re = re.compile(r'''[\]\)"'\.\?\!,:%$€“„]$''')
    infix_re = re.compile(r'''[~]''')
    simple_url_re = re.compile(r'''^https?://''')

    return Tokenizer(nlp.vocab, 
                     rules=TOKENIZER_EXCEPTIONS,
                     prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                    url_match=simple_url_re.match, 
                     )


nlp = load("bg_bg")
nlp.tokenizer = custom_tokenizer(nlp)

split_sentences(data, nlp)


# for t in nlp('а ти какъв си'):
#     for attr in t.__dir__():
#         print(attr, getattr(t, attr))

