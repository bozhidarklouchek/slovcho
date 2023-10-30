import os, csv

# Building the error dataset used for grammar error handling task for Slovcho
cwd = 'C:/Users/klouc/Desktop/slovcho/grammar_checking'

# ERROR TYPES

# 1. article_misuse: Using a full article when a short one is required and vice versa for masculine gender;
# Includes nouns, adjectives, some pronouns, some numerals and some verbs
# Nouns:
# full -> short: Човекът изяде макароните -> ЧовекА изяде макароните
# short -> full: Видях човека вчера -> Видях човекЪТ вчера
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
    # лични: аз/мен,мене, ти/теб,тебе, той/него, тя/нея, то/него, ние/нас, вие/вас, те/тях
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
        # негов,негова,негово/свой, неговия,неговата,неговото/своя, неговият,неговата,неговото/своят
        # неин,нейна,нейно/своя, нейния,нейната,нейното/своята, нейният,нейната,нейното/своята
        # негов,негова,негово/свое, неговия,неговата,неговото/своето, неговият,неговата,неговото/своето
        # негови/свои, неговите/своите
        # му/си
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


with open(f'{cwd}/errors.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'correct', 'erroneous'])

    with open(f'{cwd}/sents_tagged.csv', 'r', newline='', encoding="utf-8") as target:
        reader = csv.DictReader(target) 
        
        all_sents = []
        for row in reader:
            all_sents.append['sent']

        for row in reader:
            tokens = row['sent'].split(' ')
            for token in tokens:

                # Замести пълен член на:
                # - съществителни,
                # - прилагателни,
                if len(token) >= 3 and token[-2:] == 'ят':
                    print(token)
                    counter += 1
            if(counter >= 200):
                break

