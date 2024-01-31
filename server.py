# server.py
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
from spacy import load
from spacy.tokenizer import Tokenizer 
from language_components.token_exceptions import TOKENIZER_EXCEPTIONS
import pickle
import pandas as pd
from collections import defaultdict
from transformers import pipeline

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq, Seq2SeqTrainer

from sklearn.model_selection import train_test_split

import pandas as pd

from datasets import Dataset, load_metric

import regex as re

import torch


app = Flask(__name__)
CORS(app)


@app.route('/preprocess_input', methods=['POST'])
def preprocess_input():
    data = request.get_json()
    text = data['parameter']

    # Execute the Python script
    result = tokenizer(text)
    result = [{"text": token.text,
               "is_sent_start": token.is_sent_start,
               "is_sent_end": token.is_sent_end,
               "pos": token.tag_} for token in result]
    response = jsonify({'output': result})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/classify_style', methods=['POST'])
def classify_style():
    data = request.get_json()
    function_name = data['function_name']
    parameter = data['parameter']

    # Execute the Python script
    result = subprocess.run(['python', 'src/backend/style_classification/runner.py', function_name, parameter], stdout=subprocess.PIPE, text=True)
    response = jsonify({'output': result.stdout})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/spell_check', methods=['POST'])
def spell_check():
    data = request.get_json()
    sents = data['parameter']

    spellCheckedSents = []

    for sentToCheck in sents:

        # Lower first letter if lowercase letter exists in dict
        print(sentToCheck)
        for i in range(len(sentToCheck)):
            currWord = sentToCheck[i]
            if(ord(currWord[0]) >= ord('А') and ord(currWord[0]) <= ord('Я')):
                sentToCheck[i] = currWord.lower()

        # Use NER model
        joinedSent = " ".join(sentToCheck)
        ner_output = ner_model(joinedSent)
        for entity in reversed(ner_output):
            joinedSent = joinedSent[:entity['start'] + 1] + 'NER_' + joinedSent[entity['start'] + 1:]
        sentToCheck = joinedSent.split(' ')

        # Add <s> and </s>
        sentToCheck.insert(0, '<s>')
        sentToCheck.append('</s>')
        probs = get_word_probabilities(sentToCheck, unigram_sum, unigram_count, trust_valid_word_is_correct, bigrams, valid_words_dict, CORRECT_NON_WORDS_ONLY=True)
        spellCheckedSents.append(probs)
    response = jsonify({'output': spellCheckedSents})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_word_pos', methods=['POST'])
def get_word_pos():
    data = request.get_json()
    word = data['parameter']

    if word not in valid_words.values:
        return None
    
    result = tokenizer(word)
    response = jsonify({'output': result})

    return response

@app.route('/grammar_check', methods=['POST'])
def grammar_check():
    data = request.get_json()
    sents = data['parameter']

    # print('i got gramar this', sents)

    checkedSents = []
    for sent in sents:
        checkedSents.append(grammar_check_sent(sent))
    
    # print('grammatikkakakka', checkedSents)
    
    response = jsonify({'output': " ".join(checkedSents)})

    return response



# Tokenizer code
def custom_tokenizer(tokenizer):
    prefix_re = re.compile(r'''^[\[\("'“„]''')
    suffix_re = re.compile(r'''[\]\)"'\.\?\!,:%$€“„]$''')
    infix_re = re.compile(r'''[~]''')
    simple_url_re = re.compile(r'''^https?://''')

    return Tokenizer(tokenizer.vocab, 
                     rules=TOKENIZER_EXCEPTIONS,
                     prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                    url_match=simple_url_re.match, 
                     )
tokenizer = load("bg_bg")
tokenizer.tokenizer = custom_tokenizer(tokenizer)

# Spellchecker code
# Load unigram and bigram objects from files
unigrams = None
bigrams = None
with open('C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/unigrams.pkl', 'rb') as file:
    unigrams = pickle.load(file)
with open('C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/bigrams.pkl', 'rb') as file:
    bigrams = pickle.load(file)
unigram_sum = sum(unigrams.values())
unigram_count = len(unigrams.keys())
trust_valid_word_is_correct = 0.99
valid_words = pd.read_csv(rf"C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/single_words_bg.csv",encoding='utf-8')
valid_words_dict = defaultdict(int)
for word in list(valid_words['word']):
    valid_words_dict[word] = word


# Grammar
    
DIR = 'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/slovcho_grammar'
ft_model_tokenizer = AutoTokenizer.from_pretrained(f"{DIR}")
ft_model = AutoModelForSeq2SeqLM.from_pretrained(f"{DIR}")
MAX_INPUT_LENGTH = 128


def grammar_check_sent(sent):

    ft_prediction = []

    encoded_text = ft_model_tokenizer(" ".join(sent), return_tensors='pt', max_length=MAX_INPUT_LENGTH,
                            padding='max_length')
    translated = ft_model.generate(**encoded_text, max_length=MAX_INPUT_LENGTH)

    ft_prediction.append([ft_model_tokenizer.decode(t, skip_special_tokens=True) for t in translated][0])
    print('res,', ft_prediction[0])
    return ft_prediction[0]


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'абвгдежзийклмнопрстуфхцчшщъьюя'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def get_word_probabilities(words_to_check, unigram_sum, unigram_count, trust_valid_word_is_correct, bigrams, valid_words_dict, CORRECT_NON_WORDS_ONLY=True):
    sent_probs = []
    # print('SENT', words_to_check)
    for i in range(len(words_to_check)):
        marked_ner = False
        word = words_to_check[i]
        # If marked by NER remove temporarily
        if('NER_' in word):
            marked_ner = True
            word = word.replace('NER_', '')
        
        # Skip if start or end of sentence
        if word != '<s>' and word != '</s>':
            prev_token = words_to_check[i - 1]
            next_token = words_to_check[i + 1]
            candidates = edits1(word)

            # Non-word errors
            if word not in valid_words.values:
                print(word, 'not in dict')
                # Get candidates which are valid words
                valid_candidates = []
                for candidate in candidates:
                    if(valid_words_dict[candidate] != 0):
                        valid_candidates.append(candidate)

                # Calculate probabilty distribution
                prob_distr = []
                for valid_candidate in valid_candidates:
                    # [MISSING] = P(prob of making mistake)

                    # P(candidate) with smooting = probability of word appering
                    # candidate count in word unigram + 1 / count of all words + |V|
                    pc = unigrams[valid_candidate] + 1 / float(unigram_sum + unigram_count)

                    # P(candidate|prev_token) with smoothing = probability of findging candidate followed by prev_token
                    # count of bigrams (prev_token, candidate) + 1 / count of prev_token + |V|
                    pcp = bigrams[prev_token][valid_candidate] + 1 / float(unigrams[prev_token] + unigram_count)

                    # P(next_token|candidate) with smoothing = probability of findging next_token followed by candidate
                    # count of bigrams (candidate, next_token) + 1 / count of candidate + |V|
                    pnc = bigrams[valid_candidate][next_token] + 1 / float(unigrams[valid_candidate] + unigram_count)

                    prob_distr.append(pc * pcp * pnc)
                words_with_probs = [(word, prob) for word, prob in zip(valid_candidates, prob_distr)]
                words_with_probs.sort(key = lambda x: x[1], reverse=True)
                sent_probs.append((words_with_probs, marked_ner))

            # Real world errors
            else:
                if(CORRECT_NON_WORDS_ONLY):
                    sent_probs.append(([(word, 1)], marked_ner))
                    continue
                # Calculate probabilty distribution

                # Get candidates which are valid words
                valid_candidates = []
                for candidate in candidates:
                    if(valid_words_dict[candidate] != 0):
                        valid_candidates.append(candidate)

                prob_distr = []
                # valid_candidates.append(word)
                for valid_candidate in valid_candidates:
                    # [MISSING] = P(prob of making mistake)

                    # P(candidate) with smooting = probability of word appering
                    # candidate count in word unigram + 1 / count of all words + |V|
                    pc = unigrams[valid_candidate] + 1 / float(unigram_sum + unigram_count)

                    # P(candidate|prev_token) with smoothing = probability of findging candidate followed by prev_token
                    # count of bigrams (prev_token, candidate) + 1 / count of prev_token + |V|
                    pcp = bigrams[prev_token][valid_candidate] + 1 / float(unigrams[prev_token] + unigram_count)

                    # P(next_token|candidate) with smoothing = probability of findging next_token followed by candidate
                    # count of bigrams (candidate, next_token) + 1 / count of candidate + |V|
                    pnc = bigrams[valid_candidate][next_token] + 1 / float(unigrams[valid_candidate] + unigram_count)

                    trust = 0
                    # Apply trust for valid word
                    if(word == valid_candidate):
                        trust = trust_valid_word_is_correct
                    else:
                        trust = 1 - trust_valid_word_is_correct / len(valid_candidate)
                    prob_distr.append(pc * pcp * pnc * trust)
                words_with_probs = [(word, prob) for word, prob in zip(valid_candidates, prob_distr)]
                words_with_probs.sort(key = lambda x: x[1], reverse=True)
                sent_probs.append((words_with_probs, marked_ner))
    return sent_probs


ner_model = pipeline(
    'ner',
    model='rmihaylov/bert-base-ner-theseus-bg',
    tokenizer='rmihaylov/bert-base-ner-theseus-bg',
    device=0,
    revision=None)



if __name__ == '__main__':
    app.run(debug=True)
