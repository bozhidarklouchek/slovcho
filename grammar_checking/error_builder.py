import os, csv, re

# Building the error dataset used for grammar error handling task for Slovcho
cwd = 'C:/Users/klouc/Desktop/slovcho/grammar_checking'
REPLACE_PAIR_COUNT_MAX = 20

# ERROR TYPES

# 1. article_misuse: Using a full article when a short one is required and vice versa for masculine gender;
# Includes nouns, adjectives, some pronouns, some numerals and some verbs
# Nouns:
# N(oun), c(ommon) - no propers!, m/f/n, s(ingular) p(lural) l(forever plural) - no counts!
# i (no article)
# d (definite f/n/plurals)
# h & f (short and full for m)
# Nc(m/f/n)(s/p/l)(i/d/h/f)
# Adjectives
# full -> short Жълтият павилион е там -> ЖълтиЯ павилион е там
# short -> full: Аз изядох жълтия кекс -> Аз изядох жълтиЯТ кекс
# Pronouns
# а. Неговият брат е много луд -> НеговиЯ брат е много луд
# short -> full: Портфейлът е под неговия двор -> Портфейлът е под неговиЯТ двор
# Numerals
# full -> short Третият мъж не знае къде е тя -> ТретиЯ мъж не знае къде е тя
# short -> full: Тя победи дори първия си брат -> Тя победи дори първиЯТ си брат
# Verbs
# full -> short Падащият лист беше жълт -> ПадащиЯ лист беше жълт
# short -> full: Той извади горящият меч -> Той извади горящиЯ меч


# 2. multiple_adjective_agreement: Using a full article on all adjectives when they're referring to
# the same object or using it only on the first one when referring to multiple ones
# Single Object: Големият и силен мъж вдигна тежестта -> Големият и силниЯТ мъж вдигна тежестта
# Multiple Objects -> full Руските и полските волейболисти минаха на финал -> Руските и полски() волейболисти минаха на финал


# 5. multiple_vs_numeral: Using the multiple form of a noun instead of the numeral form


# NOT_PROTOTYPE
# 6. formality: Mistakes when using formal form


# 7. pronoun_misue: Use of the wrong pronoun depending on gender agreement or case
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


# 8. 1p_plural_verb_form: Incorrect adding of 'e' to some verbs of 1st person plural form
# Хайде да пишем -> Хайде да пишеме


# NOT_PROTOTYPE
# 9. invalid_imperative: Creating an invalid imperative.


# NOT_PROTOTYPE
# 10. invalid_gerund: Creating an invalid gerund.


# NOT_PROTOTYPE
# 11. adjective_noun_disagreement: Disagreement before adjective and noun genders and plural/singular


# NOT_PROTOTYPE
# 11.2. subject_verb_disagreement: Disagreement between actor and action


# NOT_PROTOTYPE
# 12. invalid_verb_combo: Using two verbs that require different sentence roles words
# Той предпочита и се вдъхновя от волйебола (Предпочита изисква пряко допълнение, а не съюз)

# error_dict = {
#     "article_misuse": [],
#     "multiple_adjective_agreement": [],
#     "pronoun_misue": [],
#     "1p_plural_verb_form": []
# }

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

# Make an collection of words that will be indexed over
indexed_words = set()
for group in pronoun_replacement_words:
    for word in group:
        indexed_words.add(word)

# Init inverse sentence index collection
inv_sent_index = dict()
for index_word in list(indexed_words):
    inv_sent_index[index_word] = []

def clean_sent_from_POS(sent):
    # Clean pos tags in beginning/middle and end of sentence (keeps underscores)
    sent = re.sub(r'___[a-zA-Z0-9-]+', '', sent)
    return sent

with open(f'{cwd}/errors.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'sentId', 'class', 'correct', 'erroneous'])

    with open(f'{cwd}/sents_tagged.csv', 'r', newline='', encoding="utf-8") as target:
        reader = csv.DictReader(target) 

        all_sents = {}

        # Populate inverse sent index
        for row in reader:
            for index_word in list(indexed_words):
                all_sents[row["id"]] = row["sent"]
                if(f' {index_word}___' in row['sent']):
                    inv_sent_index[index_word].append(row['id'])
        
        count = 0
        for group in pronoun_replacement_words:
            for i in range(len(group)):
                curr_word_to_replace = group[i]
                replacements = [word for word in group if word != curr_word_to_replace]
                sent_ids_with_word = inv_sent_index[curr_word_to_replace]

                for sent_id in sent_ids_with_word:
                    clean_sent = clean_sent_from_POS(all_sents[sent_id])
                    
                    replace_curr_pair_count = 0
                    for replacement in replacements:
                        errornous_sent = clean_sent.replace(f'{curr_word_to_replace} ', f'___{replacement}___ ', 1)
                        writer.writerow([count, sent_id, 'pronoun_misuse', clean_sent.replace(f'{curr_word_to_replace} ', f'___{curr_word_to_replace}___ ', 1), errornous_sent])
                        count += 1
                        replace_curr_pair_count += 1
                        if(replace_curr_pair_count >= REPLACE_PAIR_COUNT_MAX): break
                    if(replace_curr_pair_count >= REPLACE_PAIR_COUNT_MAX): break
                    

