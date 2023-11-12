import xml.etree.ElementTree as ET
import csv

# Replace 'your_file.xml' with the path to your XML file
xml_file_path = 'C:/Users/klouc/Desktop/sents_sample_tagged.xml'
cwd = 'C:/Users/klouc/Desktop/slovcho/grammar_checking'

try:
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    all_sents = set()

    # Iterate through the XML elements and print them
    for element in root:
        if(element.tag == 'root'):
            for subelement in element:
                if(subelement.tag == 's'):
                    curr_sent = "<s>"
                    ignore_tok = False

                    for token in subelement:
                        if(token.tag == 'tok'):

                            # Remove all text within brackets
                            if(token.text == '('):
                                ignore_tok = True
                            if(token.text == ')'):
                                ignore_tok = False
                                continue
                            if(ignore_tok):
                                continue
                            else:
                                curr_sent += "___" + token.text + "///" + token.attrib['ana']
                    curr_sent += '___</s>'
                    if("///V" in curr_sent):
                        if(curr_sent[:2] == '" ' or curr_sent[:2] == "' "):
                            curr_sent = curr_sent[2:]
                        if(curr_sent[0] == ' '):
                            curr_sent = curr_sent[1:]
                        if(curr_sent[len(curr_sent) - 1] == '"' or curr_sent[len(curr_sent) - 1] == "'"):
                            curr_sent = curr_sent[:len(curr_sent) - 1]
                        all_sents.add(curr_sent)

    with open(f'{cwd}/sents_tagged.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'sent'])

        c = 0
        for sent in list(all_sents):
            writer.writerow([c, sent])
            c += 1
                    
                    

except ET.ParseError as e:
    print(f"XML parsing error: {e}")
except FileNotFoundError:
    print(f"File not found: {xml_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
