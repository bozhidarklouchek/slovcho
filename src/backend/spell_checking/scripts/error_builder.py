import csv
import requests
from bs4 import BeautifulSoup
import re
import random
from tqdm import tqdm
import pandas as pd
from collections import defaultdict

valid_words = pd.read_csv(rf"C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/single_words_bg.csv",encoding='utf-8')
valid_words_dict = defaultdict(int)
for word in list(valid_words['word']):
    valid_words_dict[word] = word


def get_zvuch_type(const):
    if(const in ['б', 'в', 'г', 'д', 'ж', 'з']):
        return 'zvuch'
    elif(const in ['п', 'ф', 'к', 'т', 'ш', 'с']):
        return 'non_zvuch'
    else:
        return 'na'
    

def get_char_twin(char):
    twin = None
    cap = False
    if(char.lower() != char):
        cap = True
    if(len(char) == 1):
        char = char.lower()
        if(char == 'а'):
            twin = 'ъ'
        elif(char == 'ъ'):
            twin = 'а'
        elif(char == 'е'):
            twin = 'и'
        elif(char == 'и'):
            twin = 'е'
        elif(char == 'о'):
            twin = 'у'
        elif(char == 'у'):
            twin = 'о'
        elif(char == 'б'):
            twin = 'п'
        elif(char == 'п'):
            twin = 'б'
        elif(char == 'в'):
            twin = 'ф'
        elif(char == 'ф'):
            twin = 'в'
        elif(char == 'г'):
            twin = 'к'
        elif(char == 'к'):
            twin = 'г'
        elif(char == 'д'):
            twin = 'т'
        elif(char == 'т'):
            twin = 'д'
        elif(char == 'ж'):
            twin = 'ш'
        elif(char == 'ш'):
            twin = 'ж'
        elif(char == 'з'):
            twin = 'с'
        elif(char == 'с'):
            twin = 'з'
    if(twin == None):
        return None
    
    if(cap):
        return twin.upper()
    else:
        return twin
          
    return None

def get_word_stress_index(word):
    url = f"https://rechnik.chitanka.info/w/{word}"
    starting_string = "name-stressed"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        span = soup.find('span', id=lambda id: id and id.startswith(starting_string))
        if span:
            for idx, char in enumerate(span.text.strip()):
                if(ord(char) == 768):
                    return idx - 1
            return None # Return the text content of the span
        else:
            return None  # If no matching span is found
        
    except requests.exceptions.RequestException as e:
        # print("Error fetching page:", e)
        return None

sents = set()
with open('C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/raw_sents.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
       sents.add(row['sent'])

def apply_type1(sent, count=1):
    target_word_indices = {}

    words = sent.split(' ')
    # We check for all vowels except for:
    # - 'е' and 'и' as they're not as common with this mistake type
    # - those under stress
    shuffled_words = [(word, idx) for idx, word in enumerate(words)]
    random.shuffle(shuffled_words)

    for word_idx in shuffled_words:
        word = word_idx[0]
        idx = word_idx[1]

        # Skip if word too short
        if(word == '' or len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        overlaps = []
        stress_index = get_word_stress_index(re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word))
        for id, char in enumerate(word):
            if(stress_index == id):
                continue
            if(char in ['а', 'ъ', 'о', 'у', 'А', 'Ъ', 'О', 'У']):
                overlaps.append(id)
        target_word_indices[idx] = overlaps
        if(len(target_word_indices.keys()) == 0):
            break

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            # Override if affix 'о' or 'у'
            if(word.startswith('о') or word.startswith('у') or word.startswith('О') or word.startswith('У')):
                broken_sent.append(f"{get_char_twin(word[0])}{word[1:]}")
            else:
                target_chars = target_word_indices[idx]
                chosen_charId = random.choice(target_chars)
                chosen_char = word[chosen_charId]
                twin_char = get_char_twin(chosen_char)
                broken_word = word[:chosen_charId] + twin_char + word[chosen_charId + 1:]
                broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)


def apply_type2(sent, count=1):
    target_word_indices = {}

    words = sent.split(' ')
    # We check for zvuch/non-zvuch pairs
    for idx, word in enumerate(words):
        # Skip if word too short
        if(len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        overlaps = []
        for id in range(len(word) - 1):
            char = word[id]
            subseq_char = word[id + 1]
            if(id == 0):
                continue

            first_char_type = get_zvuch_type(char)
            if(first_char_type != 'zvuch' and first_char_type != 'non_zvuch'):
                continue
            second_char_type = get_zvuch_type(subseq_char.lower())

            # Need zvuch and non_zvuch next to each other
            if(first_char_type == 'zvuch' and second_char_type == 'non_zvuch'):
                overlaps.append(id)
            elif(first_char_type == 'non_zvuch' and second_char_type == 'zvuch'):
                overlaps.append(id)
            else:
                continue
        target_word_indices[idx] = overlaps

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            target_chars = target_word_indices[idx]
            chosen_charId = random.choice(target_chars)
            chosen_char = word[chosen_charId]
            twin_char = get_char_twin(chosen_char)
            broken_word = word[:chosen_charId] + twin_char + word[chosen_charId + 1:]
            broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)

def apply_type3(sent, count=1):
    target_word_indices = {}

    words = sent.split(' ')
    # We check for zvunch ends of words
    for idx, word in enumerate(words):
        # Skip if word too short
        if(len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        overlaps = []
        cleaned_word = re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word)
        last_char = cleaned_word[-1]
        if(get_zvuch_type(last_char) == 'zvuch'):
            target_word_indices[idx] = [True]

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            chosen_char_id = -1
            for index in range(len(word) - 1, -1, -1):  # Iterate from end of string to beginning
                if word[index].isalpha():
                    chosen_char_id = index
                    break
            chosen_char = word[chosen_char_id]
            twin_char = get_char_twin(chosen_char)
            broken_word = word[:chosen_char_id] + twin_char + word[chosen_char_id + 1:]
            broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)


def apply_type4(sent, count=1):
    target_word_indices = {}

    words = sent.split(' ')
    # We check for double 'т' and double 'н' at second half of word
    for idx, word in enumerate(words):
        # Skip if word too short
        if(len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        overlaps = []
        for id in range(len(word)//2, len(word) - 1, 1):
            char = word[id]
            subseq_char = word[id + 1]

            if(char == subseq_char):
                if(char == 'н' or char == 'т'):
                    overlaps.append(id)
        target_word_indices[idx] = overlaps

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            target_chars = target_word_indices[idx]
            chosen_charId = random.choice(target_chars)
            broken_word = word[:chosen_charId] + word[chosen_charId + 1:]
            broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)


def apply_type5(sent, count=1):
    target_word_indices = {}
    problematic_clusters = {
        'стн',
        'стк',
        'стл',
        'нтск',
        'здн',
        'ждн',
        'щн',
        'щт'
    }

    words = sent.split(' ')
    # We check for list of problematic suffixes
    for idx, word in enumerate(words):
        # Skip if word too short
        if(len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        for cluster in problematic_clusters:
            if(cluster in word):
                target_word_indices[idx] = cluster

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            target_cluster = target_word_indices[idx]
            if(target_cluster == 'щт' or target_cluster == 'щн'):
                id = word.index(target_cluster)
                broken_word = word[:id] + 'ш' + word[id+1:]
                broken_sent.append(broken_word)
            else:
                id = word.index(target_cluster)
                broken_word = word[:id+1] + word[id+2:]
                broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)


def apply_type6(sent, count=1):
    target_word_indices = {}

    words = sent.split(' ')
    shuffled_words = [(word, idx) for idx, word in enumerate(words)]
    random.shuffle(shuffled_words)

    for word_idx in shuffled_words:
        word = word_idx[0]
        idx = word_idx[1]
        # print(word)

        # Skip if word too short
        if(word == '' or len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        word_valid = False
        for char in word.lower():
            if(char in [
                    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
                    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                    'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я'
                ]):
                word_valid = True
                break
        if(not word_valid): continue

        overlaps = []
            
        char_is_alpha = False
        while not char_is_alpha:
            id = random.randint(1, len(word) - 1)
            # print(id)
            # print(word)
            # print(sent)
            if(word.lower()[id] in [
                    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
                    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                    'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я'
                ]):
                char_is_alpha = True
        overlaps.append(id)

        target_word_indices[idx] = overlaps
        if(len(target_word_indices.keys()) == 0 or
           len(target_word_indices.keys()) > count):
            break

    # Select words
    word_prone_to_error = [wordId for wordId, charIds in target_word_indices.items() if len(charIds) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            target_chars = target_word_indices[idx]
            chosen_charId = random.choice(target_chars)
            chosen_char = word[chosen_charId]
            cap = False
            if(chosen_char.lower() != chosen_char):
                cap = True
            twin_char = chosen_char
            while(twin_char == chosen_char):
                twin_char = random.choice([
                    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
                    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                    'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я'
                ])
            if(cap): twin_char = twin_char.upper()
            broken_word = word[:chosen_charId] + twin_char + word[chosen_charId + 1:]
            broken_sent.append(broken_word)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'абвгдежзийклмнопрстуфхцчшщъьюя'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
def apply_type7(sent, count=1):
    target_word_indices_with_word_twins = {}

    words = sent.split(' ')
    shuffled_words = [(word, idx) for idx, word in enumerate(words)]
    random.shuffle(shuffled_words)

    for word_idx in shuffled_words:
        word = word_idx[0]
        idx = word_idx[1]

        # Skip if word too short
        if(word == '' or len(word) <= 3):
            continue

        # Skip if unknown word with capital letter
        if(word.lower() != word and re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word).lower() not in valid_words_dict.keys()):
            continue

        word_valid = False
        for char in word.lower():
            if(char in [
                    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
                    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                    'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я'
                ]):
                word_valid = True
                break
        if(not word_valid): continue

        if(re.sub(r'[.^$*+?,!\[\]\(\)\|]', '', word) == word):
            candidates = edits1(word.lower())
            valid_candidates = []
            for candidate in candidates:
                if(valid_words_dict[candidate] != 0 and candidate != word):
                    valid_candidates.append(candidate)
                
            target_word_indices_with_word_twins[idx] = valid_candidates
            if(len(target_word_indices_with_word_twins.keys()) == 0 or
            len(target_word_indices_with_word_twins.keys()) > count):
                break

    # Select words
    word_prone_to_error = [wordId for wordId, candidates in target_word_indices_with_word_twins.items() if len(candidates) != 0]
    if(count > len(word_prone_to_error)):
        count = len(word_prone_to_error)
    wordsIds_to_change = random.sample(word_prone_to_error, count)

    # Change sent with number of errors
    broken_sent = []
    for idx, word in enumerate(words):
        if(idx not in wordsIds_to_change):
            broken_sent.append(word)
        else:
            cap = False
            if(word[0].lower() + word[1:] != word): cap = True
            candidates = target_word_indices_with_word_twins[idx]
            chosen_candidate = random.choice(target_word_indices_with_word_twins[idx])
            if(cap): chosen_candidate = chosen_candidate[0].upper() + chosen_candidate[1:]
            broken_sent.append(chosen_candidate)

    # If no change return None
    if(" ".join(broken_sent) == sent):
        return None
    
    return (" ".join(broken_sent), sent)

tyep1_pairs = set()
tyep2_pairs = set()
tyep3_pairs = set()
tyep4_pairs = set()
tyep5_pairs = set()
tyep6_pairs = set()
tyep7_pairs = set()

sents = [sent for sent in list(sents) if len(sent.split(' ')) >= 3]

# type 1
for sent in tqdm(sents):
    t1_sent = apply_type1(sent, 3)
    if(t1_sent is not None):
        tyep1_pairs.add(t1_sent)
# print(tyep1_pairs)

# type 2
for sent in tqdm(sents):
    t2_sent = apply_type2(sent, 3)
    if(t2_sent is not None):
        tyep2_pairs.add(t2_sent)
# print(tyep2_pairs)

# type 3
for sent in tqdm(sents):
    t3_sent = apply_type3(sent, 3)
    if(t3_sent is not None):
        tyep3_pairs.add(t3_sent)
# print(tyep3_pairs)

# type 4
for sent in tqdm(sents):
    t4_sent = apply_type4(sent, 3)
    if(t4_sent is not None):
        tyep4_pairs.add(t4_sent)
# print(tyep4_pairs)

# type 5
for sent in tqdm(sents):
    t5_sent = apply_type5(sent, 3)
    if(t5_sent is not None):
        tyep5_pairs.add(t5_sent)
# print(tyep5_pairs)
        
# type 6
for sent in tqdm(sents):
    t6_sent = apply_type6(sent, 3)
    if(t6_sent is not None):
        tyep6_pairs.add(t6_sent)
# print(tyep6_pairs)
        
# type 7
for sent in tqdm(sents):
    t7_sent = apply_type7(sent, 3)
    if(t7_sent is not None):
        tyep7_pairs.add(t7_sent)
# print(tyep7_pairs)

print(len(tyep1_pairs))
print(len(tyep2_pairs))
print(len(tyep3_pairs))
print(len(tyep4_pairs))
print(len(tyep5_pairs))
print(len(tyep6_pairs))
print(len(tyep7_pairs))

with open('C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/spell_errors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['error_type', 'errorneous', 'correct'])  # Write header

    # type1
    for pair in tyep1_pairs:
        writer.writerow([1, pair[0], pair[1]])

    # type2
    for pair in tyep2_pairs:
        writer.writerow([2, pair[0], pair[1]])

    # type3
    for pair in tyep3_pairs:
        writer.writerow([3, pair[0], pair[1]])

    # type4
    for pair in tyep4_pairs:
        writer.writerow([4, pair[0], pair[1]])

    # type5
    for pair in tyep5_pairs:
        writer.writerow([5, pair[0], pair[1]])

    # type6
    for pair in tyep6_pairs:
        writer.writerow([6, pair[0], pair[1]])

    # type7
    for pair in tyep7_pairs:
        writer.writerow([7, pair[0], pair[1]])