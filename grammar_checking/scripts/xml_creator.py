import csv, random, sys
import xml.etree.ElementTree as ET

csv.field_size_limit(100000000)

# Create the root element
root = ET.Element("sents")

# Building the error dataset used for grammar error handling task for Slovcho
dataDir = 'C:/Users/klouc/Desktop/slovcho/data'
# stylesDir = 'C:/Users/klouc/Desktop/slovcho/style_classification/styles.csv'

sents_to_add_to_xml = []

for i in range(71):
    with open(f'C:/Users/klouc/Desktop/oscar/oscar_{i}.csv', 'r', newline='', encoding="utf-8") as target:
        reader = csv.DictReader(target) 
        counter = 0

        full_sent_list = []
        for row in reader:
                full_sent_list.append(row['text'])
        random.shuffle(full_sent_list)
        sents_to_add_to_xml.extend(full_sent_list[:777])

counter = 0
for sent in sents_to_add_to_xml:
    sent_xml = ET.Element("article")
    sent_xml.text = sent
    root.append(sent_xml)
    counter += 1
          
# Create an ElementTree
tree = ET.ElementTree(root)
# Write the XML to a file
tree.write("sents_sample.xml", encoding="utf-8")