import requests, csv
from bs4 import BeautifulSoup

def parse_html_words(api_url, writer):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            html_content = response.text

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')


            # Extract structured data from the HTML
            data_container = soup.find("div", {"class": "words"})

            if data_container:
                # Convert the extracted data to a Python dictionary
                data_dict = {
                    "data": data_container.text  # You might need to further parse or format this data
                }

                # Remove empty strings
                for word in data_dict["data"].split('\n'):
                    if word:
                        writer.writerow([word])

                # Convert the Python dictionary to JSON
            else:
                print("Data container not found in the HTML")
                return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ'

with open(f'bg_words.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['headword'])
    for char in alphabet.lower():
        print(f'Starting {char}')
        for char2 in alphabet.lower():
            api_url = f'https://slovored.com/sitemap/pravopisen-rechnik/letter/{char}/{char}{char2}'
            parse_html_words(api_url, writer)

