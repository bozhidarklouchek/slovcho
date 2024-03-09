import tqdm
import csv
import re
# from spacy import load
# from spacy.tokenizer import Tokenizer 
# from language_components.token_exceptions import TOKENIZER_EXCEPTIONS

CWD = 'C:/Users/klouc/Desktop/slovcho/src/backend/data/corpora'
SPLIT = 'split'
RAW = 'raw'

# current_file = 'btv_articles.csv'

# csv_dict = {
#     'Изкуствен интелект.csv': 'content',
#     'nova_articles.csv': 'content',
#     'Алгебра.csv': 'content',
#     'Архитектура.csv': 'content',
#     'Астрономия.csv': 'content',
#     'Биология.csv': 'content',
#     'Генетика.csv': 'content',
#     'Геометрия.csv': 'content',
#     'Езикознание.csv': 'content',
#     'Екология.csv': 'content',
#     'Журналистика.csv': 'content',
    
#     'Изкуство.csv': 'content',
#     'Икономика.csv': 'content',
#     'Инженерна наука.csv': 'content',
#     'История.csv': 'content',
#     'Компютърна сигурност.csv': 'content',
#     'Макроикономика.csv': 'content',
#     'Маркетинг.csv': 'content',
#     'Математика.csv': 'content',
#     'Медицина.csv': 'content',
#     'Микроикономика.csv': 'content',
#     'Народно творчество.csv': 'content',
#     'Изкуствен интелект.csv': 'content',
#     'Образование.csv': 'content',
#     'Право.csv': 'content',
#     'Психология.csv': 'content',
#     'Стереометрия.csv': 'content',
#     'Тригонометрия.csv': 'content',
#     'Физика.csv': 'content',
#     'Химия.csv': 'content',
# }

# txt_files = {
#     'bulgarian_constitution.txt',
#     'girltalk.txt',
#     'richard_bach_illusions.txt',
#     'state_energy.txt',
#     'sufferings_of_shernenhoh.txt'
# }

# semi_split_files = {
#     'wikipedia_sentences.txt',
#     'news_sentences.txt'
# }

# def custom_tokenizer(nlp):
#     prefix_re = re.compile(r'''^[\[\("'“„]''')
#     suffix_re = re.compile(r'''[\]\)"'\.\?\!,:%$€“„]$''')
#     infix_re = re.compile(r'''[~]''')
#     simple_url_re = re.compile(r'''^https?://''')

#     return Tokenizer(nlp.vocab, 
#                      rules=TOKENIZER_EXCEPTIONS,
#                      prefix_search=prefix_re.search,
#                      suffix_search=suffix_re.search,
#                      infix_finditer=infix_re.finditer,
#                     url_match=simple_url_re.match, 
#                      )


# nlp = load("bg_bg")
# nlp.tokenizer = custom_tokenizer(nlp)


# def should_keep_sent(sent):
#     for t in sent:
#         if(t.tag_[0] == 'V'):
#             return True
#     return False

# for txt_file in tqdm.tqdm(semi_split_files):
#     with open(f'{CWD}/{RAW}/{txt_file}', 'r', newline='', encoding='utf-8') as input_file:
#         # csv_reader = csv.DictReader(input_file)
#         # header = next(csv_reader, None)

#         with open(f'{CWD}/{SPLIT}/{txt_file[0:-4]}.csv', 'w', newline='', encoding='utf-8') as output_file:

#             csv_writer = csv.writer(output_file)
#             c = 0
#             csv_writer.writerow(['id', 'source', 'sent'])

#             sents = []

#             # print(content)
#             for row in tqdm.tqdm(input_file):
#                 row = row.replace('\n','').replace('\r', '')
#                 tokens = nlp(row)

#                 curr_sent = []
#                 for t in tokens:
#                     curr_sent.append(t)
#                     if(t.is_sent_end):
#                         if(should_keep_sent(curr_sent)):
#                             csv_writer.writerow([c, txt_file, [f"{t.text}///{t.tag_}" for t in curr_sent]])
#                             c += 1
#                             # sents.append(curr_sent)
#                         curr_sent = []
#             # print(sents)


# # print(f"New CSV file '{output_csv_file}' created successfully.")



import os
import csv
import pandas as pd

def extract_and_save_row(input_directory, output_file, target_row_index):
    # Initialize an empty list to store row values
    all_row_values = []

    # Iterate through all files in the specified directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)

            # Read the CSV file using pandas
            with open(file_path, 'r', newline='', encoding='utf-8') as input_file:
                csv_reader = csv.DictReader(input_file)
                for row in csv_reader:
                    all_row_values.append("_____".join((row['sent'][2:-2].split("', '"))))
            # # Check if the target row index is within the range of the DataFrame
            # if target_row_index < len(df):
            #     # Extract the specified row value
            #     row_value = df.iloc[target_row_index].values.tolist()

                # Append the row value to the list
            
            # else:
            #     print(f"Warning: Row index {target_row_index} is out of range for file {filename}")

    # Write the collected row values to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header if the list is not empty
        c=0
        csv_writer.writerow(['id', 'sent'])
        for row in all_row_values:
            
            # Write data
            csv_writer.writerow([c, row])
            c += 1

# Example usage
input_directory = f'{CWD}/split'
output_file = "sents.csv"
target_row_index = 2  # Change this to the specific row index you want to extract

extract_and_save_row(input_directory, output_file, target_row_index)
