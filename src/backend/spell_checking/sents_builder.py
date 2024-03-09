import os, csv

# Building the sents dataset used for spell checking task for Slovcho
cwd = 'C:/Users/klouc/Desktop/slovcho/spell_checking'

with open(f'{cwd}/sents.csv', 'w', newline='', encoding="utf-8") as target:
    writer = csv.writer(target)
    writer.writerow(['id', 'sent', 'source', 'file'])

    txtFilesDir = f'{cwd}/data/ultimate_bg_dataset'
    if(os.path.exists(txtFilesDir)):
        txtFiles = os.listdir(txtFilesDir)
        counter = 0
        for txtFile in txtFiles:
            with open(f'{cwd}/data/ultimate_bg_dataset/{txtFile}', 'r', encoding="utf-8") as file:
                for line in file:
                    writer.writerow([counter, line.replace('\n', ''), 'ultimate_bg_dataset', txtFile])
                    counter += 1