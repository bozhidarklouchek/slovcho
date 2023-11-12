import os, csv, re
from word_checker import get_word_derivs

# Building the error dataset used for grammar error handling task for Slovcho
cwd = 'C:/Users/klouc/Desktop/slovcho/grammar_checking/data/errors2_oscar'

# Results in approx. times 4 sents
REPLACE_ARTICLE_PAIR_COUNT_MAX = 0
# Results in approx. times 74 sents
REPLACE_PRONOUN_PAIR_COUNT_MAX = 1
# Results in approx. times 1 sents
REPLACE_V1P_PAIR_COUNT_MAX = 0
# Results in approx. times 12 sents
REPLACE_ADJ_NOUN_AGREEMENT_COUNT_MAX = 0

# ERROR TYPES



# 1. article_misuse: Using a full article when a short one is required and vice versa for masculine gender;
# Includes nouns, adjectives, some pronouns, some numerals and some verbs

# NOUNS:
# N(oun), c(ommon) - no propers!, m/f/n, s(ingular) p(lural) l(forever plural) - no counts!
# i (no article)
# d (definite f/n/plurals)
# h & f (short and full for m)
# i <-> h is impossible as both are valid, depends on context

# Ncmsi -> Ncmsf
# Ncmsf -> Ncmsi
# Ncmsh -> Ncmsf
# Ncmsf -> Ncmsh
# Ncfsi -> Ncfsd
# Ncfsd -> Ncfsi
# Ncnsi -> Ncnsd
# Ncnsd -> Ncnsi
# Nc(m/f/n)pi -> Nc(m/f/n)pd
# Nc(m/f/n)pd -> Nc(m/f/n)pi
# Nc-li -> Nc-ld
# Nc-ld -> Nc-li


# ADJECTIVE:
# A(djective), m/f/n, s(ingular) p(lural)
# i (no article)
# d (definite f/n/plurals)
# h & f (short and full for m)
# i <-> h is impossible as both are valid, depends on context

# Amsi -> Amsf
# Amsf -> Amsi
# Amsh -> Amsf
# Amsf -> Amsh
# Afsi -> Afsd
# Afsd -> Afsi
# Ansi -> Ansd
# Ansd -> Ansi
# A-pi -> A-pd
# A-pd -> A-pi

article_replacement_tags = {
    "N": [
        ['Ncmsf', 'Ncmsh'],
        # ['Ncmsh', 'Ncmsi'], does not always lead to error
        # ['Ncfsi', 'Ncfsd'],
        # ['Ncnsi', 'Ncnsd'],
        # ['Ncmpi', 'Ncmpd'],
        # ['Ncfpi', 'Ncfpd'],
        # ['Ncnpi', 'Ncnpd'],
        # ['Nc-li', 'Nc-ld']
    ],
    "A": [
        ['Amsf', 'Amsh'],
        # ['Amsh', 'Amsi'], does not always lead to error
        # ['Afsi', 'Afsd'],
        # ['Ansi', 'Ansd'],
        # ['A-pi', 'A-pd']
    ],
}
# Make an collection of articled tags that will be indexed over
indexed_article_tags = set()
for role_group in article_replacement_tags.values():
    for tag_group in role_group:
        for tag in tag_group:
            indexed_article_tags.add(tag)
# Init inverse artciel tag index collection
inv_sent_article_tags_index = dict()
for index_tag in list(indexed_article_tags):
    inv_sent_article_tags_index[index_tag] = set()



# 2. pronoun_misue: Use of the wrong pronoun depending on gender agreement or case
# case: 
    # лични: аз/мен, аз/мене, ти/теб, ти/тебе, той/него, тя/нея, то/него, ние/нас, вие/вас, те/тях
    # притежателни: -
    # възвратни (лични и притежателни): -
    # показателни: -
    # въпросителни: кой/кого, кое/кого
    # относителни: който/когото
    # неопрелени: някой/някого
    # отрицателни: никой/никого
    # обобщителни: -
# gender & plural/singular:
    # лични: -
    # притежателни: -
    # възвратни (лични и притежателни): -
    # показателни: -
    # въпросителни: чий/чия/чие/чии
    # относителни: чийто/чиято/чието/чиито
    # неопрелени: -
    # отрицателни: -
    # обобщителни: -
# possessive extras:
    # притежателни vs. възвратно притежателни:
        # негов/свой, неговия/своя, неговият/своят, неин/свой, нейния/своя, нейният/своят
        # негова/своя, неговата/своята, нейна/своя, нейната/своята
        # негово/свое, неговото/своето, нейно/свое, нейното/своето
        # негови/свои, неговите/своите, нейни/свои, нейните/своите
        # му/си, й/си
# demonstrative extras:
    # лични vs. показателни:
        # този/него, тази/нея, това/него
pronoun_replacement_words = [
    ["аз", "мен"],
    ["аз", "мене"],
    ["ти", "теб"],
    ["ти", "тебе"],
    ["той", "него"],
    ["тя", "нея"],
    ["то", "него"],
    ["ние", "нас"],
    ["вие", "вас"],
    ["те", "тях"],

    ["кой", "кого"],
    ["кое", "кого"],

    ["който", "когото"],
    ["някой", "някого"],
    ["никой", "никого"],
    ["чий", "чия", "чие", "чии"],
    ["чийто", "чиято", "чието", "чиито"],

    ["негов", "свой"],
    ["неин", "свой"],
    ["неговия", "своя"],
    ["нейния", "своя"],
    ["неговият", "своят"],
    ["нейният", "своят"],

    ["негова", "своя"],
    ["нейна", "своя"],
    ["неговата", "своята"],
    ["нейната", "своята"],

    ["негово", "свое"],
    ["нейно", "свое"],
    ["неговото", "своето"],
    ["нейното", "своето"],

    ["негови", "свои"],
    ["нейни", "свои"],
    ["неговите", "своите"],
    ["нейните", "своите"],

    ["му", "си"],
    ["й", "си"],

    ["този", "него"],
    ["тази", "нея"],
    ["това", "него"]
]
# Make an collection of pronouns that will be indexed over
indexed_pronouns = set()
for group in pronoun_replacement_words:
    for word in group:
        indexed_pronouns.add(word)
# Init inverse sentence index collection
inv_sent_pronoun_index = dict()
for index_word in list(indexed_pronouns):
    inv_sent_pronoun_index[index_word] = set()



# 3. 1p_plural_verb_form: Incorrect adding of 'e' to some verbs of 1st person plural form
# Хайде да пишем -> Хайде да пишеме
# V(*)1p are the ones we want, if they with 'м' add 'е'
# Make an collection of V1p that will be indexed over
inv_sent_V1p_index = {
    'V_1p' : set()
}

# 4. word_disagreement
# 4.1 word_disagreement_object_verb
# gender: Тя беше излязла с приятелки. → Тя беше излязъл с приятелки.
# number: Музикалната банда реши да свирят в Созопол. → Музикалната банда решиха да свирят в Созопол.
# 4.2 word_disagreement_adjective_noun
# gender: Силният мъж вдигна тежестта. → Силната мъж вдигна тежестта.
# number: Силният мъж вдигна тежестта. → Силните мъж вдигна тежестта.
word_disagreement_replacement_tags = {
    "word_disagreement_adjective_noun": [
        ["Amsi", "Afsi", "Ansi", "A-pi"],
        ["Amsh", "Afsd", "Ansd", "A-pd"],
        ["Amsf", "Afsd", "Ansd", "A-pd"]
    ]
}
# Make an collection of tags that will be indexed over
indexed_word_disagreement_tags = set()
for role_group in word_disagreement_replacement_tags.values():
    for tag_group in role_group:
        for tag in tag_group:
            indexed_word_disagreement_tags.add(tag)
# Init inverse artciel tag index collection
inv_sent_word_disagreement_tags_index = dict()
for index_tag in list(indexed_word_disagreement_tags):
    inv_sent_word_disagreement_tags_index[index_tag] = set()



# NOT_PROTOTYPE
# 9. invalid_imperative: Creating an invalid imperative.



# NOT_PROTOTYPE
# 10. invalid_gerund: Creating an invalid gerund.



# NOT_PROTOTYPE
# 11. word_disagreement: Disagreement before adjective and noun genders and plural/singular



# NOT_PROTOTYPE
# 11.2. subject_verb_disagreement: Disagreement between actor and action



# NOT_PROTOTYPE
# 12. invalid_verb_combo: Using two verbs that require different sentence roles words
# Той предпочита и се вдъхновя от волйебола (Предпочита изисква пряко допълнение, а не съюз)

# 2. multiple_adjective_agreement: Using a full article on all adjectives when they're referring to
# the same object or using it only on the first one when referring to multiple ones
# Single Object: Големият и силен мъж вдигна тежестта -> Големият и силниЯТ мъж вдигна тежестта
# Multiple Objects -> full Руските и полските волейболисти минаха на финал -> Руските и полски() волейболисти минаха на финал



# 5. multiple_vs_numeral: Using the multiple form of a noun instead of the numeral form



# NOT_PROTOTYPE
# 6. formality: Mistakes when using formal form





def clean_sent(sent):
    # Clean pos tags in beginning/middle and end of sentence (keeps underscores)
    tokenised_sent = sent.split("___")
    clear_sent = ""
    for token in tokenised_sent:
        if(token == '<s>' or token == '</s>'): continue
        tagged_token = token.split('///')
        if(tagged_token[1] == 'punct'): clear_sent += tagged_token[0]
        else: clear_sent += " " + tagged_token[0]
    return clear_sent[1:]

with open(f'{cwd}/errors.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'sentId', 'class', 'correct', 'erroneous'])

    with open(f'{cwd}/sents_tagged.csv', 'r', newline='', encoding="utf-8") as target:
        sent_pairs = 0
        reader = csv.DictReader(target) 

        # Populate sents dict and all inverse dicts
        all_sents = {}
        for row in reader:
            all_sents[row["id"]] = row["sent"]

            # article inverse dict
            for index_tag in list(indexed_article_tags):
                if(f'///{index_tag}' in row['sent']):
                    inv_sent_article_tags_index[index_tag].add(row['id'])

            # pronoun inverse dict
            for index_word in list(indexed_pronouns):
                if(f'___{index_word}///' in row['sent']):
                    inv_sent_pronoun_index[index_word].add(row['id'])

            # v1p inverse dict
            tagged_tokens = row['sent'].split('___')
            for tt in tagged_tokens:
                if('///' in tt):
                    word = tt.split('///')[0]
                    tag = tt.split('///')[1]
                    if(len(tag) >= 3 and tag[0]=='V' and tag[-2:]=='1p' and word[-1:] == 'м'):
                        inv_sent_V1p_index["V_1p"].add(row['id'])
            
            # noun_adj inverse dict
            for index_tag in list(indexed_word_disagreement_tags):
                if(f'///{index_tag}' in row['sent']):
                    inv_sent_word_disagreement_tags_index[index_tag].add(row['id'])

        # ARTICLE_MISUSE
        if(REPLACE_ARTICLE_PAIR_COUNT_MAX):
            for word_role in article_replacement_tags.keys():
                tag_groups = article_replacement_tags[word_role]
                for group in tag_groups:
                    for i in range(len(group)):
                        curr_tag_to_replace = group[i]
                        replacement_tags = [tag for tag in group if tag != curr_tag_to_replace]
                        sent_ids_with_tag = list(inv_sent_article_tags_index[curr_tag_to_replace])

                        replace_curr_pair_count = 0
                        for sent_id in sent_ids_with_tag:
                            correct_sent = all_sents[sent_id]
                            if(replace_curr_pair_count >= REPLACE_ARTICLE_PAIR_COUNT_MAX): break
                            
                            for replacement_tag in replacement_tags:
                                tokenised_sent = [tagged_token.split('///') for tagged_token in correct_sent.split('___')]
                                tokenised_sent = tokenised_sent[1:-1]

                                curr_word_to_replace = ""
                                for tagged_token in tokenised_sent:
                                    if(tagged_token[1] == curr_tag_to_replace):
                                        curr_word_to_replace = tagged_token[0]
                                        break
                                
                                # Deal with най- and по- for A
                                comparative_prefix = ""
                                if(len(curr_word_to_replace) > 4 and curr_word_to_replace[:4] == "най-"):
                                    comparative_prefix = "най-"
                                    curr_word_to_replace = re.sub(r'\bнай-', "", curr_word_to_replace)
                                elif(len(curr_word_to_replace) > 4 and curr_word_to_replace[:4] == "Най-"):
                                    comparative_prefix = "Най-"
                                    curr_word_to_replace = re.sub(r'\bНай-', "", curr_word_to_replace)
                                elif(len(curr_word_to_replace) > 3 and curr_word_to_replace[:4] == "по-"):
                                    comparative_prefix = "по-"
                                    curr_word_to_replace = re.sub(r'\bпо-', "", curr_word_to_replace)  
                                elif(len(curr_word_to_replace) > 3 and curr_word_to_replace[:4] == "По-"):
                                    comparative_prefix = "По-"
                                    curr_word_to_replace = re.sub(r'\bПо-', "", curr_word_to_replace)                                

                                # If any error, skip
                                derivs = get_word_derivs(curr_word_to_replace, curr_tag_to_replace)
                                if(not derivs or derivs[replacement_tag] == '-'):
                                    continue

                                # If replaced word is capitalised, capitaise replacement word
                                if(f'{curr_word_to_replace[0].lower()}{curr_word_to_replace[1:]}' != curr_word_to_replace):
                                    derivs[replacement_tag] = f'{derivs[replacement_tag][0].capitalize()}{derivs[replacement_tag][1:]}'

                                if(comparative_prefix):
                                    curr_word_to_replace = comparative_prefix + curr_word_to_replace
                                    derivs[replacement_tag] = comparative_prefix + derivs[replacement_tag]
                                clear_sent = clean_sent(correct_sent)
                                errornous_sent = clear_sent.replace(f'{curr_word_to_replace} ', f'___{derivs[replacement_tag]}___ ', 1)
                                writer.writerow([sent_pairs, sent_id, 'article_misuse', clear_sent.replace(f'{curr_word_to_replace} ', f'___{curr_word_to_replace}___ ', 1), errornous_sent])
                                sent_pairs += 1
                                replace_curr_pair_count += 1
                                if(replace_curr_pair_count >= REPLACE_ARTICLE_PAIR_COUNT_MAX): break
                            if(replace_curr_pair_count >= REPLACE_ARTICLE_PAIR_COUNT_MAX): break
        

        # PRONOUN_MISUSE
        if(REPLACE_PRONOUN_PAIR_COUNT_MAX):
            for group in pronoun_replacement_words:
                for i in range(len(group)):
                    curr_word_to_replace = group[i]
                    replacements = [word for word in group if word != curr_word_to_replace]
                    sent_ids_with_word = list(inv_sent_pronoun_index[curr_word_to_replace])

                    replace_curr_pair_count = 0
                    for sent_id in sent_ids_with_word:
                        clear_sent = clean_sent(all_sents[sent_id])
                        
                        for replacement in replacements:
                            errornous_sent = clear_sent.replace(f'{curr_word_to_replace} ', f'___{replacement}___ ', 1)
                            writer.writerow([sent_pairs, sent_id, 'pronoun_misuse', clear_sent.replace(f'{curr_word_to_replace} ', f'___{curr_word_to_replace}___ ', 1), errornous_sent])
                            sent_pairs += 1
                            replace_curr_pair_count += 1
                            if(replace_curr_pair_count >= REPLACE_PRONOUN_PAIR_COUNT_MAX): break
                        if(replace_curr_pair_count >= REPLACE_PRONOUN_PAIR_COUNT_MAX): break


        # 1P_PLURAL_VERB_FORM
        if(REPLACE_V1P_PAIR_COUNT_MAX):
            replace_curr_pair_count = 0
            for sent_id in list(inv_sent_V1p_index["V_1p"]):
                word_to_replace = ""
                replacement = ""
                tokenised_sent = all_sents[sent_id].split('___')
                for tt in tokenised_sent:
                    if('///' in tt):
                        tt = tt.split('///')
                        if(len(tt[1]) >= 3 and tt[1][0]=='V' and tt[1][-2:]=='1p' and tt[0][-1:] == 'м'):
                            word_to_replace = tt[0]
                            replacement = f'{tt[0]}е'
                clear_sent = clean_sent(all_sents[sent_id])
                errornous_sent = clear_sent.replace(f'{word_to_replace} ', f'___{replacement}___ ', 1)
                writer.writerow([sent_pairs, sent_id, '1p_plural_verb_form', clear_sent.replace(f'{word_to_replace} ', f'___{word_to_replace}___ ', 1), errornous_sent])
                sent_pairs += 1
                replace_curr_pair_count += 1
                if(replace_curr_pair_count >= REPLACE_V1P_PAIR_COUNT_MAX): break

        # WORD_DISAGREEMENT
        if(REPLACE_ADJ_NOUN_AGREEMENT_COUNT_MAX):
            for disagreement_type in word_disagreement_replacement_tags.keys():
                tag_groups = word_disagreement_replacement_tags[disagreement_type]
                for group in tag_groups:
                    for i in range(len(group)):
                        curr_tag_to_replace = group[i]
                        replacement_tags = [tag for tag in group if tag != curr_tag_to_replace]
                        sent_ids_with_tag = list(inv_sent_word_disagreement_tags_index[curr_tag_to_replace])

                        replace_curr_pair_count = 0
                        for sent_id in sent_ids_with_tag:
                            correct_sent = all_sents[sent_id]
                            if(replace_curr_pair_count >= REPLACE_ADJ_NOUN_AGREEMENT_COUNT_MAX): break
                            
                            for replacement_tag in replacement_tags:
                                tokenised_sent = [tagged_token.split('///') for tagged_token in correct_sent.split('___')]
                                tokenised_sent = tokenised_sent[1:-1]

                                curr_word_to_replace = ""
                                for tagged_token in tokenised_sent:
                                    if(tagged_token[1] == curr_tag_to_replace):
                                        curr_word_to_replace = tagged_token[0]
                                        break
                                
                                # Deal with най- and по- for A
                                comparative_prefix = ""
                                if(len(curr_word_to_replace) > 4 and curr_word_to_replace[:4] == "най-"):
                                    comparative_prefix = "най-"
                                    curr_word_to_replace = re.sub(r'\bнай-', "", curr_word_to_replace)
                                elif(len(curr_word_to_replace) > 4 and curr_word_to_replace[:4] == "Най-"):
                                    comparative_prefix = "Най-"
                                    curr_word_to_replace = re.sub(r'\bНай-', "", curr_word_to_replace)
                                elif(len(curr_word_to_replace) > 3 and curr_word_to_replace[:4] == "по-"):
                                    comparative_prefix = "по-"
                                    curr_word_to_replace = re.sub(r'\bпо-', "", curr_word_to_replace)  
                                elif(len(curr_word_to_replace) > 3 and curr_word_to_replace[:4] == "По-"):
                                    comparative_prefix = "По-"
                                    curr_word_to_replace = re.sub(r'\bПо-', "", curr_word_to_replace)                                

                                # If any error, skip
                                derivs = get_word_derivs(curr_word_to_replace, curr_tag_to_replace)
                                if(not derivs or derivs[replacement_tag] == '-'):
                                    continue

                                # If replaced word is capitalised, capitaise replacement word
                                if(f'{curr_word_to_replace[0].lower()}{curr_word_to_replace[1:]}' != curr_word_to_replace):
                                    derivs[replacement_tag] = f'{derivs[replacement_tag][0].capitalize()}{derivs[replacement_tag][1:]}'

                                if(comparative_prefix):
                                    curr_word_to_replace = comparative_prefix + curr_word_to_replace
                                    derivs[replacement_tag] = comparative_prefix + derivs[replacement_tag]
                                clear_sent = clean_sent(correct_sent)
                                errornous_sent = clear_sent.replace(f'{curr_word_to_replace} ', f'___{derivs[replacement_tag]}___ ', 1)
                                writer.writerow([sent_pairs, sent_id, 'word_disagreement_adjective_noun', clear_sent.replace(f'{curr_word_to_replace} ', f'___{curr_word_to_replace}___ ', 1), errornous_sent])
                                sent_pairs += 1
                                replace_curr_pair_count += 1
                                if(replace_curr_pair_count >= REPLACE_ADJ_NOUN_AGREEMENT_COUNT_MAX): break
                            if(replace_curr_pair_count >= REPLACE_ADJ_NOUN_AGREEMENT_COUNT_MAX): break
            

    

        
                    

