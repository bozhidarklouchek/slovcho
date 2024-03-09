import csv, random

wiki_dir = ('C:/Users/klouc/Desktop/slovcho/grammar_checking/data/errors1_wikipedia_articles/wiki_sents_tagged.csv', "wikipedia")
oscar_dir = ('C:/Users/klouc/Desktop/slovcho/grammar_checking/data/errors2_oscar/oscar_sents_tagged.csv', "oscar")

data_dir = 'C:/Users/klouc/Desktop/slovcho/grammar_checking/data'

all_sents = []

for dir in [wiki_dir, oscar_dir]:
    with open(dir[0], 'r', newline='', encoding="utf-8") as target:
        reader = csv.DictReader(target) 
        for row in reader:
            all_sents.append((row['sent'], dir[1]))

random.shuffle(all_sents)

with open(f'{data_dir}/oscar_wiki_tagged.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'sent', 'source'])

    c = 0
    for sent in all_sents:
        writer.writerow([c, sent[0], sent[1]])
        c += 1