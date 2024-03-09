import csv

def verb_cleaner():
     with open("break_deriv.txt", 'w', encoding='utf-8') as break_deriv:
        with open("spell_checking/dictionary.csv", 'r', encoding='utf-8') as csv_file:
            # Create a CSV reader object
            csv_reader = csv.DictReader(csv_file) 

            article_list = [
                            'съм', 'си', 'е', 'сме', 'сте', 'са',
                            'бях', 'беше', 'бяхме', 'бяхте', 'бяха',
                            'бил', 'била', 'било', 'били',
                            'бих', 'би', 'бихме', 'бихте', 'биха',
                            'ще',
                            'щях', 'щеше', 'щях', 'щяхме', 'щяхте', 'щяха',
                            'щял', 'щяла', 'щяло', 'щели',
                            'да',
                            ]

            # Iterate through each row in the CSV file and print them
            words = set()
            for row in csv_reader:
                headw = row['headword']
                words.add(headw)
                derivs = row['derivatives'].split(',')
                for deriv in derivs:
                    content_word = []
                    broken_deriv = deriv.split(' ')
                    for part in broken_deriv:
                        if(part not in article_list):
                            content_word.append(part)
                    if(len(content_word) == 0):
                        break_deriv.write('Killed all derivs of: ' + headw + '\n')
                    elif(len(content_word)) == 1:
                        words.add(content_word[0])
                    else:
                        break_deriv.write('Polluted: ' + headw + ' '.join(content_word) +'\n')
            
            for article in article_list:
                words.add(article)
                
            for word in list(words):
                break_deriv.write(word + '\n')
            

verb_cleaner()