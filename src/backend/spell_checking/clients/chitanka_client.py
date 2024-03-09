import requests, csv, time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
api_url = f'https://rechnik.chitanka.info/'
word_index = 0

def parse_html_word(api_url, word):
    try:
        response = requests.get(api_url + word, headers=headers)
        if response.status_code == 200:
            html_content = response.text

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")


            # Extract structured data from the HTML
            content = soup.find("div", {"id": "content"})
            meanings = content.find_all(recursive=False)
            for meaning in meanings:

                # extracting id
                try:
                    id = meaning.get('id').split('_')[1]
                except:
                    continue

                # extracting definition
                definition = ''
                # try:
                #     definition = meaning.find("div", {"class": "data", "id": f'meaning_{id}'})
                #     definition = definition.get_text().replace("\n", " ").replace("\t", " ").replace("  ", "")
                #     if(definition[0] == ' '): definition = definition[1:]
                #     if(definition[len(definition) - 2: len(definition)] == ' ('): definition = definition[:len(definition) - 2]
                #     # print(definition) 
                # except:
                #     print(f'Error in definition for {word}') 
                
                # extracting type
                word_type = ''
                # try:
                #     word_type = meaning.find("span", {"id": f'type_{id}'})
                #     word_type = word_type.contents[0].replace("\n", " ").replace("\t", " ").replace("  ", " ")
                #     if(word_type[0] == ' '): word_type = word_type[1:]
                #     if(word_type[len(word_type) - 2: len(word_type)] == ' ('): word_type = word_type[:len(word_type) - 2]
                #     # print(word_type)
                # except:
                #     print(f'Error in type for {word}')
                

                # extracting derivatives
                derivs = []
                try:
                    tableDiv = meaning.find("div", {"class": "derivative-forms box"})
                    deriv_list = tableDiv.find_all("a")
                    for deriv in deriv_list:
                        print(deriv.contents[0])
                    # print(deriv.contents)
                    # tables = tableDiv.find_all("table", {"class": "forms-table"})
                    # for table in tables:
                    #     derivs.extend([deriv.contents[0].replace('-','') for deriv in table.find_all("a")])
                    # derivs = ','.join(list(set(derivs)))
                    # print(derivs)
                except:
                    print(f'Error in derivatives for {word}')
                if(derivs == []):
                    derivs = ""

                global word_index
                # writer.writerow([word_index, word, word_type, definition, derivs ])
                word_index += 1

        else:
            print(f"Request failed with status code: {response.status_code} for word {word}")
            if(response.status_code == 404):
                # writer.writerow([word_index, word, "", "", "" ])
                word_index += 1
            else:
                # If unexpected error occurred sleep for 120s
                # sleep_writer.writerow([word, response.status_code])
                time.sleep(120)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        # If unexpected error occurred sleep for 120s
        # sleep_writer.writerow([word, str(e)])
        time.sleep(120)
        return None

# with open(f'dictionary.csv', 'w', encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(['id', 'headword', 'type', 'definition', 'derivatives'])
#     with open(f'slept_words.csv', 'w', encoding="utf-8") as slept:
#         sleep_writer = csv.writer(slept)
#         sleep_writer.writerow(['word', 'error_code'])
#         with open(f'bg_words.csv', 'r', encoding="utf-8") as csv_file:
#             reader = csv.DictReader(csv_file) 
#             for row in reader:
#                 parse_html_word(api_url, row['headword'], writer, sleep_writer)

def parse_html_type_pages(api_url, type_dict, writer, sleeper):
    for key in type_dict.keys():
        type_id, type_name, type_code = key.split('/')
        pages = type_dict[key]
        for page in pages:
            url_end = f'/type/{type_id}'
            if(page != 1):
                url_end += f'/{str(page)}'

            try:
                response = requests.get(api_url + url_end, headers=headers)
                if response.status_code == 200:
                    html_content = response.text

                    # Use BeautifulSoup to parse the HTML
                    soup = BeautifulSoup(html_content, "html.parser")


                    # Extract structured data from the HTML
                    content = soup.find("ul", {"class": "words"})
                    deriv_list = content.find_all("a")
                    for deriv in deriv_list:
                        writer.writerow([deriv.contents[0], key])


                else:
                    print(f"Request failed with status code: {response.status_code} for type {key}")
                    if(response.status_code == 404):
                        # writer.writerow([word_index, word, "", "", "" ])
                        word_index += 1
                    else:
                        # If unexpected error occurred sleep for 120s
                        sleeper.writerow([key, response.status_code])
                        time.sleep(120)
                    return None

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                # If unexpected error occurred sleep for 120s
                sleep_writer.writerow([key, str(e)])
                time.sleep(120)
                return None

# with open(f'dictionary.csv', 'w', encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(['id', 'headword', 'type', 'definition', 'derivatives'])
#     with open(f'slept_words.csv', 'w', encoding="utf-8") as slept:
#         sleep_writer = csv.writer(slept)
#         sleep_writer.writerow(['word', 'error_code'])
#         with open(f'bg_words.csv', 'r', encoding="utf-8") as csv_file:
#             reader = csv.DictReader(csv_file) 
#             for row in reader:
#                 parse_html_word(api_u
# parse_html_word(api_url, f"w/{скачам}")

with open(f'typed_words.csv', 'w', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['word', 'type'])
    with open(f'slept_words.csv', 'w', encoding="utf-8") as slept:
        sleep_writer = csv.writer(slept)
        sleep_writer.writerow(['word', 'error_code'])
        type_dict = {
            '188/adverb/D': [1,2,3,4,5,6,7,8,9,10,
                             11,12,13,14,15,16,17,18,19,20,
                             21,22,23,24,25,26,27,28,29,30,
                             31],
            '189/conjunction/C': [1],
            '190/interjection/I': [1],
            '191/articles/T': [1,2],
            '192/preposition/R': [1]
        }
        nums = parse_html_type_pages(api_url, type_dict, writer, sleep_writer)

