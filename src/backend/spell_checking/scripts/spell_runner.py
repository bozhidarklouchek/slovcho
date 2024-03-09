import csv, re
from transformers import pipeline
import pandas as pd
import pickle
from collections import defaultdict
from tqdm import tqdm

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'абвгдежзийклмнопрстуфхцчшщъьюя'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


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

valid_words = pd.read_csv(rf"C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/data/single_words_bg.csv",encoding='utf-8')
valid_words_dict = defaultdict(int)
for word in list(valid_words['word']):
    valid_words_dict[word] = word

def is_word_in_dict(word):
    return word in valid_words.values

def get_word_probabilities(words_to_check, unigram_sum, unigram_count, trust_valid_word_is_correct, bigrams, valid_words_dict, CORRECT_NON_WORDS_ONLY=True):
    sent_probs = []
    # print('SENT', words_to_check)
    for i in range(len(words_to_check)):
        capitalised = False
        marked_ner = False
        lower_version_valid = False
        word = words_to_check[i]

        # If marked by NER, remember
        if('NER_' in word):
            marked_ner = True
            word = word.replace('NER_', '')
        
        # Skip if start or end of sentence
        if word != '<s>' and word != '</s>':
            
            # If too small, return how it is
            if(len(word) < 4):
                sent_probs.append(([(word, 1)], '-'))
                continue

            # If numeric, return how it is
            pattern = f'^[0-9,.]+$'
            if(bool(re.match(pattern, word))):
                sent_probs.append(([(word, 1)], '-'))
                continue

            non_capitalised_word = word[0].lower() + word[1:]

            # Mark if capitalised
            if(word != non_capitalised_word):
                capitalised = True
                # ORIGINAL in dictionary, return how it is (ex: Божидар)
                if(is_word_in_dict(word)):
                    sent_probs.append(([(word, 1)], '-'))
                    continue
                # LOWER in dictionary, mark as lower valid (ex: Здравейте)
                elif(is_word_in_dict(non_capitalised_word)):
                    lower_version_valid = True
                # neither ORIGINAL or LOWER in dictionary, but marked by NER, return how it is
                elif(marked_ner):
                    sent_probs.append(([(word, 1)], True))
                    continue

            # If capitalised, temporally lower
            if(capitalised):
                word = non_capitalised_word

            prev_token = words_to_check[i - 1]
            next_token = words_to_check[i + 1]
            candidates = edits1(word)

            # Non-word errors
            if not is_word_in_dict(word):
                # print(word, 'not in dict')
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

                # If empty array, return same word
                if(len(words_with_probs) == 0):
                    words_with_probs = [(word, 0)]

                # Return capital words if capitalised
                if(capitalised):
                    words_with_probs = [(f'{word_prob[0][0].upper()}{word_prob[0][1:]}', word_prob[1]) for word_prob in words_with_probs]

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

                    # Apply trust for valid word
                    if(word == valid_candidate):
                        trust = trust_valid_word_is_correct
                    else:
                        trust = 1 - trust_valid_word_is_correct / len(valid_candidate)
                    prob_distr.append(pc * pcp * pnc * trust)
                words_with_probs = [(word, prob) for word, prob in zip(valid_candidates, prob_distr)]
                words_with_probs.sort(key = lambda x: x[1], reverse=True)

                # If empty array, return same word
                if(len(words_with_probs) == 0):
                    words_with_probs = [(word, 0)]

                # Return capital words if capitalised
                if(capitalised):
                    words_with_probs = [(f'{word_prob[0][0].upper()}{word_prob[0][1:]}', word_prob[1]) for word_prob in words_with_probs]

                sent_probs.append((words_with_probs, marked_ner))
    return sent_probs

ner_model = pipeline(
    'ner',
    model='rmihaylov/bert-base-ner-theseus-bg',
    tokenizer='rmihaylov/bert-base-ner-theseus-bg',
    device=0,
    revision=None)


grid_space = {
    'ner_model': [True, False],
    'trust': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99],
    'suggestion window': [1, 2, 3]
}

# trust_valid_word_is_correct = 0.99
# suggestion_window = 3
limit = 800
it = 1

for trust in reversed(grid_space['trust']):
    for should_add_ner_model in grid_space['ner_model']:
        for window in grid_space['suggestion window']:
            if it < 10:
                it += 1
                continue
            

            err_type_dict = defaultdict(int)
            print(should_add_ner_model, trust, window)

            with open('C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/data/spell_errors.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                with open(f'C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/data/results/spell_eval_NER-{str(should_add_ner_model)}_t-{str(trust)}_swindow-{str(window)}.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['error_type', 'errorenous', 'correct', 'prediction'])
                    chars_to_remove = r'[^a-zA-Zа-яА-Я0-9-]'

                    for row in tqdm(reader):

                        err_type = int(row['error_type'])
                        if(err_type_dict[err_type] >= limit):
                            continue
                        err_type_dict[err_type] += 1


                        inp = [word for word in row['errorenous'].split(' ') if(len(word) != 0)]
                        ref = [word for word in row['correct'].split(' ') if(len(word) != 0)]

                        # inp = ['Сдравейте', 'дами', 'и', 'господа']
                        # ref = ['Здравейте']

                        sentToCheck = inp

                        for i in range(len(sentToCheck)):
                            currWord = sentToCheck[i]
                            sentToCheck[i] = re.sub(chars_to_remove, '', currWord)

                        if(should_add_ner_model):
                            # Use NER model
                            joinedSent = " ".join(sentToCheck)
                            ner_output = ner_model(joinedSent)
                            for entity in reversed(ner_output):
                                joinedSent = joinedSent[:entity['start'] + 1] + 'NER_' + joinedSent[entity['start'] + 1:]
                            sentToCheck = joinedSent.split(' ')
                            # Remove _NER tag if word too short
                            sentToCheck = [word.replace('NER_', '') if len(word.replace('NER_', '')) < 4 else word for word in sentToCheck ]

                        # Add <s> and </s>
                        sentToCheck.insert(0, '<s>')
                        sentToCheck.append('</s>')
                        probs = get_word_probabilities(sentToCheck, unigram_sum, unigram_count, trust, bigrams, valid_words_dict, CORRECT_NON_WORDS_ONLY=False)
                        
                        chosen_sequence = []
                        for err, corr, pred in zip([word for word in row['errorenous'].split(' ') if(len(word) != 0)],
                                                    [word for word in row['correct'].split(' ') if(len(word) != 0)],
                                                    probs):

                            error = re.sub(chars_to_remove, '', err)
                            correct = re.sub(chars_to_remove, '', corr)

                            if(window == 1):
                                chosen_sequence.append(pred[0][0][0])
                            else:
                                top_predictions = [suggestion[0] for suggestion in pred[0][:window]]
                                chosen_prediction = top_predictions[0]

                                for prediction in top_predictions:
                                    if(prediction == correct):
                                        chosen_prediction = prediction
                                        break
                                
                                chosen_sequence.append(chosen_prediction)


                        # print()
                        # print(inp)
                        # print(ref)
                        # for p in probs:
                        #     print(p)

                        if(len(inp) != len(ref) and len(ref) != len(probs)):
                            print(inp)
                            print(ref)
                            print([word_prob[0][0][0] for word_prob in probs])
                            raise Exception
                        
                        writer.writerow([row['error_type'], row['errorenous'], row['correct'], " ".join(chosen_sequence)])
                        # break
                        it += 1

                        
