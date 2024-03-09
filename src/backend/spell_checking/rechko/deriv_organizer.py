import csv, tqdm

# with open('spell_checking/rechko/derivs.csv', 'r', encoding='utf-8') as csv_file:
#     # Create a CSV reader object
#     csv_reader = csv.DictReader(csv_file) 
#     descr_set = set()
#     verb_set = set()
#     descr_types = []
#     example_types = []
#     curr_descr = []
#     curr_example = []
#     start = True
#     for row in csv_reader:
#         if(start):
#             curr_descr = [row['description']]
#             curr_example = [row['lemma']]
#             start = False
#             continue
#         if(row['is_inf'] == '0'):
#             curr_descr.append(row['description'])
#             curr_example.append(row['lemma'])
#             continue
#         if(row['is_inf'] == '1'):
#             if(curr_descr not in descr_types):
#                 descr_types.append(curr_descr)
#                 example_types.append(curr_example)
#             curr_descr = [row['description']]
#             curr_example = [row['lemma']]
#             continue
#     csv_file.close()





# copy = False
# copy_to = '1'
# copy_tag = ''
# def get_tag(group):
#     global copy_tag
#     global copy
#     global copy_to
#     global last_tag

#     lemmas = " ".join([row['lemma'] for row in group])
#     descrs = " ".join([row['description'] for row in group])

#     if(copy_to == [row['id'] for row in group][0]):
#         copy = False
#     if(copy):
#         return copy_tag

#     if("вр." in descrs or "наклонение" in descrs or "прич." in descrs):
#         last_tag = 'V'
#         return 'V'
#     elif("бройна форма" in descrs or
#          "звателна форма" in descrs or
#          descrs == "ед.ч. ед.ч. членувано мн.ч. мн.ч. членувано" or
#          descrs == "ед.ч. ед.ч. непълен член ед.ч. пълен член" or
#          descrs == "ед.ч."):
#         last_tag = 'N'
#         return 'N'
#     elif("мъжколична" in descrs or "приблизителен брой" in descrs):
#         last_tag = 'M'
#         return 'M'
#     elif(("м.р." in descrs and "ж.р." in descrs and "ср.р." in descrs) or
#          "ж.р." in descrs and "ср.р." in descrs):
#         last_tag = 'Aog'
#         return 'A'
#     elif("мн.ч. мн.ч. членувано" == descrs and last_tag == 'Aog'):
#         last_tag = 'A'
#         return 'A'
#     elif('м.р.' not in descrs and 'ж.р.' not in descrs and 'ср.р.' not in descrs and "ед.ч." in descrs and 'мн.ч.' in descrs):
#         return 'N'
#     else:
#         print(lemmas)
#         print(descrs)
#         i = str(input()).split(',')
#         copy = True
#         copy_tag = i[0]
#         copy_to = i[1]
#         return i
    
#     # tags = ['N', 'N', 'A', 'N', 'N', 'A', 'A', 'N', 'N', 'N', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'N', 'A', 'A', 'A', 'N', 'A', 'N', 'A', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'A', 'A', 'A', '-', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'N', 'N']
# with open('spell_checking/rechko/derivs.csv', mode='r', newline='', encoding='utf-8') as csv_file:
#     csv_reader = csv.DictReader(csv_file) 
#     with open('derivs_tagged.csv', mode='w', newline='', encoding='utf-8') as new:
#         csv_writer = csv.writer(new)
#         csv_writer.writerow(['id', 'original_id', 'lemma', 'description', 'is_inf', 'search', 'tag'])
#         curr_group = []
#         start = True
#         for row in csv_reader:
#             if(start):
#                 curr_group = [row]
#                 start = False
#                 continue
#             if(row['is_inf'] == '0'):
#                 curr_group.append(row)
#                 continue
#             if(row['is_inf'] == '1'):
#                 tag = get_tag(curr_group)
#                 for row1 in curr_group:
#                     csv_writer.writerow(
#                         [
#                             row1['id'],
#                             row1['original_id'],
#                             row1['lemma'],
#                             row1['description'],
#                             row1['is_inf'],
#                             row1['search'],
#                             tag
#                         ]
#                     )
#                 print(tag)
#                 curr_group = [row]
#                 continue





# with open('spell_checking/rechko/dictionary2.csv', mode='w', newline='', encoding='utf-8') as dictf:
#     d = csv.writer(dictf)
#     with open('spell_checking/rechko/derivs_tagged.csv', mode='r', newline='', encoding='utf-8') as d_taggedf:
#         tagged = csv.DictReader(d_taggedf) 
#         with open('spell_checking/rechko/typed_words.csv', mode='r', newline='', encoding='utf-8') as typed_wf:
#             typed = csv.DictReader(typed_wf) 
#             id = 0
#             d.writerow(['id', 'term', 'pos', 'extra', 'search_count'])
            
#             typed_word_set = set()
#             for t in tqdm.tqdm(typed):
#                 d.writerow([id, t['word'], t['type'].split('/')[-1], '-', '-'])
#                 typed_word_set.add(t['word'])
            
#             for deriv in tqdm.tqdm(tagged):
#                 if(deriv['lemma'] != '-' and deriv['tag'] != 'P' and deriv['lemma'] not in typed_word_set):
#                     d.writerow([id, deriv['lemma'], deriv['tag'], deriv['description'], deriv['search']])
#                     id += 1



with open('spell_checking/rechko/dictionary2.csv', mode='r', newline='', encoding='utf-8') as dictf:
    d = csv.DictReader(dictf) 
    with open('spell_checking/rechko/single_words.csv', mode='w', newline='', encoding='utf-8') as single:
        single_word = csv.writer(single) 
        single_word.writerow(['word', 'tag'])
        word_tags = set()

        print(word_tags)
        article_list = [
                        'съм', 'си', 'е', 'сме', 'сте', 'са', 'се',
                        'бях', 'беше', 'бяхме', 'бяхте', 'бяха',
                        'бил', 'била', 'било', 'били',
                        'бих', 'би', 'бихме', 'бихте', 'биха',
                        'ще',
                        'щях', 'щеше', 'щях', 'щяхме', 'щяхте', 'щяха',
                        'щял', 'щяла', 'щяло', 'щели',
                        'да',
                        ]
        
        for term_def in d:
            if(term_def['pos'] == 'V'):
                broken_down = term_def['term'].split(' ')
                if(len(broken_down) != 1):
                    filtered = [br for br in broken_down if(br not in article_list)]
                    if(len(filtered) == 1):
                        word_tags.add((filtered[0], 'V'))
                    else:
                        continue
                else:
                    word_tags.add((broken_down[0], 'V'))
            else:
                if(len(term_def['term'].split(' ')) == 1):
                    word_tags.add((term_def['term'], term_def['pos']))
                else:
                    print(term_def['term'])
        
        for a in article_list:
            word_tags.add((a, 'T'))
                
        sorted_word_tags = sorted(word_tags, key=lambda x: x[0])
        for word_tag in sorted_word_tags:
            single_word.writerow([word_tag[0], word_tag[1]])