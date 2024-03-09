import requests, csv, time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
api_url = f'https://rechnik.chitanka.info/'
word_index = 0

# def disambiguate_meaning(soup, word, type):
#     meanings = soup.find_all("div", {"class": "meaning box"})
#     candidates = [meaning.find('a').text.replace('-','') for meaning in meanings]
#     print(candidates)

def get_word_derivs(word, type):
    if('-' in word): return None

    try:
        response = requests.get(f'{api_url}w/' + word, headers=headers)
        if response.status_code == 200:
            html_content = response.text

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            c = soup.find("div", {"id" : "content"})
            meaning = c.find_all("div", {"class": "meaning box"})

            if(len(meaning) == 1):
                single_meaning = meaning[0]
                subtext = single_meaning.find("p", {"class" : "data"})
                if(subtext and "е производна форма" in subtext.text):
                    return get_word_derivs(single_meaning.find('a').text, type)

            if(len(meaning) > 1):
                if(type[:1] == 'V'):
                    subtexts = [single_meaning.find("p", {"class" : "data"}) for single_meaning in meaning]
                    valid_subtexts = [subtext and subtext.text and "е производна форма" in subtext.text for subtext in subtexts]
                    if(False in valid_subtexts or None in valid_subtexts):
                        return None
                    else:
                        return get_word_derivs(meaning[0].find('a').text, type)
                else:
                    return None


            all_deriv_tables = soup.find_all("table", {"class": "forms-table"})

            if(not all_deriv_tables):
                return None
            
            # content = soup.find("table", {"class": "forms-table"})

            # if(all_deriv_tables == None or len(all_deriv_tables) == 0):
            #     try:
            #         return get_word_derivs(meaning[0].find('a').text, type)
            #     except:
            #         print('Critical error for finding new word')
            #         return None
            
            # verbs
            all_forms = [[td.text.replace("-","") for td in table.find_all('td') if(len(td.text) > 1)] for table in all_deriv_tables]

            # noun and adj   
            derivs = [td.text.replace("-","") for td in all_deriv_tables[0].find_all('td') if(len(td.text) > 1)]

            if(type[:3] == 'Ncm'):
                try:
                    return {
                        'Ncmsi': derivs[0],
                        'Ncmsh': derivs[1],
                        'Ncmsf': derivs[2],
                        'Ncmpi': derivs[3],
                        'Ncmpd': derivs[4]
                    }
                except:
                    return None
            elif(type[:3] == 'Ncf'):
                try:
                    return {
                        'Ncfsi': derivs[0],
                        'Ncfsd': derivs[1],
                        'Ncfpi': derivs[2],
                        'Ncfpd': derivs[3]
                    }
                except:
                    return None
            elif(type[0:3] =='Ncn'):
                try:
                    return {
                        'Ncnsi': derivs[0],
                        'Ncnsd': derivs[1],
                        'Ncnpi': derivs[2],
                        'Ncnpd': derivs[3]
                    }
                except:
                    return None
            elif(type[:3] == 'Nc-'):
                try:
                    return {
                        'Nc-li': derivs[3],
                        'Nc-ld': derivs[4]
                    }
                except:
                    return None
            elif(type[:1] == 'A'):
                try:
                    return {
                        'Amsi': derivs[0],
                        'Amsh': derivs[1],
                        'Amsf': derivs[2],
                        'Afsi': derivs[3],
                        'Afsd': derivs[4],
                        'Ansi': derivs[5],
                        'Ansd': derivs[6],
                        'A-pi': derivs[7],
                        'A-pd': derivs[8]
                    }
                except:
                    return None
            elif(type[:1] == 'V'):
                try:
                    return sum([len(dvs) for dvs in all_forms])
                except:
                    return None
            return None
            
        else:
            # print(f"Request failed with status code: {response.status_code} for word {word}")
            if(response.status_code == 404):
                return False
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


# print(get_word_derivs('боравя', 'V'))
# print(get_word_derivs('доближавам', 'V'))
# print(get_word_derivs('кацна', 'V'))
# print(get_word_derivs('уплаша', 'V'))
# print(get_word_derivs('живота', 'Ncmsh'))
# print(get_word_derivs('има', 'V'))
# print(get_word_derivs('избие', 'V'))
# print(get_word_derivs('засърби', 'V'))