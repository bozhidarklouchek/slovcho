import re, csv
from tqdm import tqdm

#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `name` varchar(100) DEFAULT NULL,
#   `name_stressed` varchar(100) DEFAULT NULL,
#   `name_broken` varchar(120) DEFAULT NULL,
#   `name_condensed` varchar(80) DEFAULT NULL,
#   `description` varchar(150) DEFAULT NULL,
#   `is_infinitive` tinyint(1) DEFAULT '0',
#   `base_word_id` mediumint(9) DEFAULT NULL,
#   `search_count` bigint(20) DEFAULT '0',
#   `corpus_rank` smallint(6) DEFAULT NULL,
#   `corpus_count` int(11) DEFAULT NULL,
#   `corpus_percent` smallint(6) DEFAULT NULL,

# with open('derivs.csv', mode='w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     id = 0
#     csv_writer.writerow(['id', 'original_id', 'lemma', 'description', 'is_inf', 'search'])
#     with open("derivs.txt", "r", encoding='utf-8') as file:
#         pattern = r'\((\d+.*?NULL)\)'
#         for i in tqdm(range(648)):
#             into_statement = file.readline()
            
#             # Remove insert statement
#             derivs_raw = into_statement[37:-2]
#             # Break down lemmas
#             derivs = re.findall(pattern, derivs_raw)
#             for deriv in derivs:
#                 elements = []
#                 curr_word = ''
#                 should_ignore_comma = False
#                 for char in deriv:
#                     if(char == "'" or char == '"'):
#                         should_ignore_comma = not should_ignore_comma
#                         continue
#                     if(char == ',' and not should_ignore_comma):
#                         elements.append(curr_word)
#                         curr_word = ''
#                         continue
#                     curr_word += char
#                 elements.append(curr_word)
#                 original_id, lemma, _, _, _, description, is_inf, _, search, _, _, _ = elements
#                 csv_writer.writerow([id, original_id, lemma, description, is_inf, search])
#                 id += 1
#                 if(len(elements) != 12):
#                     print(elements)
#                     break


#   `id` mediumint(9) NOT NULL AUTO_INCREMENT,
#   `name` varchar(100) DEFAULT NULL,
#   `name_stressed` varchar(100) DEFAULT NULL,
#   `name_broken` varchar(120) DEFAULT NULL,
#   `name_condensed` varchar(80) DEFAULT NULL,
#   `meaning` longtext,
#   `synonyms` longtext,
#   `classification` text,
#   `type_id` smallint(6) DEFAULT NULL,
#   `pronounciation` varchar(100) DEFAULT NULL,
#   `etymology` longtext,
#   `related_words` longtext,
#   `derived_words` longtext,
#   `chitanka_count` bigint(20) DEFAULT NULL,
#   `chitanka_percent` float(18,2) DEFAULT NULL,
#   `chitanka_rank` mediumint(9) DEFAULT NULL,
#   `search_count` bigint(20) DEFAULT '0',
#   `source` enum('bgoffice','eurodict','idi','onlinerechnik','user')
#   `other_langs` text,
#   `deleted_at` datetime DEFAULT NULL,
#   `corpus_count` int(11) DEFAULT NULL,
#   `corpus_percent` int(11) DEFAULT NULL,
#   `corpus_rank` smallint(6) DEFAULT NULL,

# with open('words.csv', mode='w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     id = 0
#     csv_writer.writerow(['id', 'original_id', 'lemma', 'type_id'])
#     with open("spell_checking/rechko/words.txt", "r", encoding='utf-8') as file:
#         pattern = r'\((\d+.*?NULL)\)'
#         for i in tqdm(range(34)):
#             into_statement = file.readline()
            
#             # Remove insert statement
#             derivs_raw = into_statement[26:-2]
#             # Break down lemmas
#             derivs = re.findall(pattern, derivs_raw)
#             for deriv in derivs:
#                 elements = []
#                 curr_word = ''
#                 should_ignore_comma_q = False
#                 should_ignore_comma_q2 = False
#                 for char in deriv:
#                     if(char == "'"):
#                         should_ignore_comma_q = not should_ignore_comma_q
#                     elif(char == '"'):
#                         should_ignore_comma_q2 = not should_ignore_comma_q2
#                         continue
#                     elif(char == ',' and not should_ignore_comma_q and not should_ignore_comma_q2):
#                         elements.append(curr_word)
#                         curr_word = ''
#                         continue
#                     curr_word += char
#                 elements.append(curr_word)
#                 csv_writer.writerow([id, elements[0], elements[1], elements[8]])
#                 id += 1
#                 if(len(elements) != 23):
#                     quack = True
#                     print(len(elements))
#                     print(elements)
#                     raise KeyError


#   `id` smallint(6) NOT NULL AUTO_INCREMENT,
#   `name` varchar(10) DEFAULT NULL,
#   `idi_number` smallint(5) unsigned DEFAULT NULL,
#   `speech_part` varchar(60) DEFAULT NULL,
#   `comment` longtext,
#   `rules` longtext,
#   `rules_test` longtext,
#   `example_word` varchar(100) DEFAULT NULL,

with open('types.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['id', 'idi', 'speech_part'])
    with open("spell_checking/rechko/types.txt", "r", encoding='utf-8') as file:
        pattern = r'\((\d+.*?)\)'
        for i in tqdm(range(1)):
            into_statement = file.readline()
            
            # Remove insert statement
            derivs_raw = into_statement[31:-2]
            # Break down lemmas
            derivs = re.findall(pattern, derivs_raw)
            for deriv in derivs:
                elements = []
                curr_word = ''
                should_ignore_comma_q = False
                should_ignore_comma_q2 = False
                for char in deriv:
                    if(char == "'"):
                        should_ignore_comma_q = not should_ignore_comma_q
                    elif(char == '"'):
                        should_ignore_comma_q2 = not should_ignore_comma_q2
                        continue
                    elif(char == ',' and not should_ignore_comma_q and not should_ignore_comma_q2):
                        elements.append(curr_word)
                        if(len(elements) == 4): break
                        curr_word = ''
                        continue
                    curr_word += char
                csv_writer.writerow([elements[0], elements[2], elements[3]])
                if(len(elements) != 4):
                    quack = True
                    print(len(elements))
                    print(elements)
                    raise KeyError


            