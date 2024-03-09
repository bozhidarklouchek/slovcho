import csv, os, random, sys
from pathlib import Path

# Building the style dataset used for style classification task for Slovcho
cwd = 'C:/Users/klouc/Desktop/slovcho/style_classification'
classes = [
    'administrative',
    'casual_real',
    'casual_fictional',
    'news',
    'academic_formal',
    'academic_informal',
    'creative'
]
doc_number_limit_per_class = 4000

# csv.field_size_limit(sys.maxsize)

def getTxtFileData(text_class, writer):
    doc_count = 0
    txtFilesDir = f'{cwd}/data/{text_class}/txt'
    if(os.path.exists(txtFilesDir)):
        txtFiles = os.listdir(txtFilesDir)
        for txtFile in txtFiles:        
            with open(f'{cwd}/data/{text_class}/txt/{txtFile}', 'r', encoding="utf-8") as text:
                writer.writerow([text_class, Path(txtFile).stem, text.read()])
                doc_count += 1

def getCsvFileData(text_class, writer):
    doc_count = 0
    csvFilesDir = f'{cwd}/data/{text_class}/csv'
    if(os.path.exists(csvFilesDir)):
        csvFiles = os.listdir(csvFilesDir)
        for csvFile in csvFiles:
            with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
                # Read as dictionaries
                reader = csv.DictReader(csv_file) 
                for row in reader:
                    if(doc_count > doc_number_limit_per_class):
                        break
                    writer.writerow([text_class, f'{row["title"]}', f'{row["content"]}'])
                    doc_count += 1

def getWikipediaCsvFileData(text_class, writer):
    csvFilesDir = f'{cwd}/data/{text_class}/csv'
    if(os.path.exists(csvFilesDir)):
        csvFiles = os.listdir(csvFilesDir)
        csvFileCount = len(csvFiles)
        articlesPerDomain = doc_number_limit_per_class / csvFileCount
        for csvFile in csvFiles:
            doc_count = 0
            with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
                # Read as dictionaries
                reader = csv.DictReader(csv_file) 
                for row in reader:
                    if(doc_count > articlesPerDomain):
                        break
                    writer.writerow([text_class, f'{row["category"]}/{row["title"]}', f'{row["content"]}'])
                    doc_count += 1

def getRedditCsvData(text_class, writer):
    doc_count = 0
    csvFilesDir = f'{cwd}/data/{text_class}/csv'
    if(os.path.exists(csvFilesDir)):
        csvFiles = os.listdir(csvFilesDir)
        for csvFile in csvFiles:
            with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
                # Read as dictionaries
                reader = csv.DictReader(csv_file) 
                reader_randomised = []
                for row in reader:
                    reader_randomised.append(row)

                random.shuffle(reader_randomised)
                for row in reader_randomised:
                    if(doc_count > doc_number_limit_per_class):
                        break
                    writer.writerow([text_class, f'{row["title"]}', f'{row["content"]}'])
                    doc_count += 1



with open(f'{cwd}/styles.csv', 'w', newline='', encoding="utf-8") as target:
    writer = csv.writer(target)
    writer.writerow(['class', 'title', 'content'])


    # ACADEMIC_FORMAL
    text_class = 'academic_formal'


    # ACADEMIC_INFORMAL 
    text_class = 'academic_informal'
    getWikipediaCsvFileData(text_class, writer)

    
    # ADMINISTRATIVE
    text_class = 'administrative'
    getTxtFileData(text_class, writer)
    getCsvFileData(text_class, writer)

    
    # CASUAL_FICTION 
    text_class = 'casual_fiction'


    # CASUAL_REAL
    text_class = 'casual_real'
    getRedditCsvData(text_class, writer)


    # CREATIVE 
    text_class = 'creative'
    getTxtFileData(text_class, writer)
    getCsvFileData(text_class, writer)

    # NEWS
    text_class = 'news'
    getCsvFileData(text_class, writer)

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)
chars = set()
with open(f'{cwd}/styles.csv', 'r', newline='', encoding="utf-8") as target:
    reader = csv.DictReader(target)  
    for row in reader:
        for char in row["content"]:
            chars.add(char)
print(chars)

        # # Go through .txt files
        # txtFilesDir = f'{cwd}/data/{text_class}/txt'
        # if(os.path.exists(txtFilesDir)):
        #     txtFiles = os.listdir(txtFilesDir)
        #     for txtFile in txtFiles:        
        #         with open(f'{cwd}/data/{text_class}/txt/{txtFile}', 'r', encoding="utf-8") as text:
        #             writer.writerow([text_class, Path(txtFile).stem, text.read()])
        #             doc_count += 1

        # # Go through .csv files
        # csvFilesDir = f'{cwd}/data/{text_class}/csv'
        # if(os.path.exists(csvFilesDir)):
        #     csvFiles = os.listdir(csvFilesDir)
        #     for csvFile in csvFiles:

        #         # Reddit CSVs
        #         if('reddit_' in csvFile):
        #             # Reddit CSV Header:
        #             # Subreddit, contenttype, id, title, content
        #             with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
        #                 # Read as dictionaries
        #                 reader = csv.DictReader(csv_file) 
        #                 reader_randomised = []
        #                 for row in reader:
        #                     reader_randomised.append(row)

        #                 random.shuffle(reader_randomised)
        #                 for row in reader_randomised:
        #                     if(doc_count > doc_number_limit_per_class):
        #                         break
        #                     writer.writerow([text_class, f'{row["subreddit"]}-{row["content_type"]}-{row["id"]}', f'{row["title"]} {row["content"]}'])
        #                     doc_count += 1

        #         # Wikipedia CSVs
        #         elif('wikipedia_' in csvFile):
        #             # Wikipedia CSV Header:
        #             # Category, title, content
        #             with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
        #                 # Read as dictionaries
        #                 reader = csv.DictReader(csv_file) 
        #                 for row in reader:
        #                     writer.writerow([text_class, f'{row["Category"]}-{row["title"]}', f'{row["content"]}'])
        #                     doc_count +=1
                
        #         else:
        #             # General CSV
        #             # Must include content
        #             with open(f'{cwd}/data/{text_class}/csv/{csvFile}', 'r', encoding="utf-8") as csv_file:
        #                 # Read as dictionaries
        #                 reader = csv.DictReader(csv_file) 
        #                 for row in reader:
        #                     writer.writerow([text_class, f'{row["title"]}', f'{row["content"]}'])
        #                     doc_count += 1
