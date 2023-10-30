import csv, random, sys
import xml.etree.ElementTree as ET

csv.field_size_limit(100000000)

# Create the root element
root = ET.Element("sents")

# Building the error dataset used for grammar error handling task for Slovcho
dataDir = 'C:/Users/klouc/Desktop/slovcho/data'
stylesDir = 'C:/Users/klouc/Desktop/slovcho/style_classification/styles.csv'

with open(f'{stylesDir}', 'r', newline='', encoding="utf-8") as target:
    reader = csv.DictReader(target) 
    counter = 0

    sent_list = []
    for row in reader:
        if(row['class'] == 'academic_informal'):
            sent_list.append(row)
    random.shuffle(sent_list)

    counter = 0
    for sent in sent_list:
        sent_xml = ET.Element("article")
        sent_xml.text = sent['content']
        root.append(sent_xml)
        counter += 1
        if(counter > 100):
            break
          

# Create an ElementTree
tree = ET.ElementTree(root)
# Write the XML to a file
tree.write("sents_sample.xml", encoding="utf-8")