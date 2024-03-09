import csv, wikipediaapi, re, random

# Initialize the Wikipedia API client with a custom user agent
user_agent = 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'
wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='bg')  # Change 'en' to the desired language code
first_level_count = 40
second_level_count = 10

# Function to fetch and store articles in a CSV file
def fetch_and_store_articles(domains):
    for domain in domains:
        with open(domain + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["class", "category", "title", "content"])
            page = wiki_wiki.page(domain)

            if page.exists():
                title = page.title
                content = page.text
                csv_writer.writerow(["academic_informal", domain, title, content])
                print(f"Now starting '{title}' domain.")

                # Get X good ones
                related_articles = []
                related_articles_raw = list(page.links.keys())
                random.shuffle(related_articles_raw)
                
                for related_article in related_articles_raw:
                    if(related_article.lower() not in domains and
                       not related_article.isnumeric() and
                       'век','Шаблон:',"Уикипедия:" not in related_article.lower() and
                       bool(re.search('[а-яА-Я]', related_article))):
                        # print(related_article)
                        if(len(related_articles) > first_level_count):
                            break
                        related_articles.append(related_article)

                if related_articles:
                    for related_article in related_articles:
                    #     if(related_article.lower() in domains or related_article.isnumeric() or 'век' in related_article.lower()
                    #        or not bool(re.search('[а-яА-Я]', related_article))):
                    #         denied_articles.append(related_article)
                    #         continue
                        related_page = wiki_wiki.page(related_article)
                        if related_page.exists():
                            title = related_page.title
                            content = related_page.text
                            csv_writer.writerow(["academic_informal", domain, title, content])
                            print(f"Now starting '{domain}/{title}' domain.")
                            
                            # Get Y
                            #  good ones
                            related_articles = []
                            related_articles_raw = list(related_page.links.keys())
                            random.shuffle(related_articles_raw)

                            for related_article in related_articles_raw:
                                if(related_article.lower() not in domains and
                                not related_article.isnumeric() and
                                'век','Шаблон:',"Уикипедия:" not in related_article.lower() and
                                bool(re.search('[а-яА-Я]', related_article))):
                                    if(len(related_articles) > second_level_count):
                                        break
                                    related_articles.append(related_article)
                                    

                            if related_articles:
                                for related_article in related_articles:
                                    # if(related_article.lower() in domains or related_article.isnumeric() or 'век' in related_article.lower()
                                    # or not bool(re.search('[а-яА-Я]', related_article))):
                                    #     denied_articles.append(related_article)
                                    #     continue
                                    related_page = wiki_wiki.page(related_article)
                                    if related_page.exists():
                                        title = related_page.title
                                        content = related_page.text
                                        csv_writer.writerow(["academic_informal", domain, title, content])

# with open("denied.txt", 'w', newline='', encoding='utf-8') as file:
#     for word in denied_articles:
#         file.write(word)
#     file.close()

# List of article names you want to request
domains = [
    "Физика",
    "Химия",
    "Биология",
    "Образование",
    "Архитектура",
    "Математика",
    "Инженерна наука",
    "Психология",
    "Архитектура",
    "Народно творчество",
    "История",
    "Медицина",
    "Икономика",
    "Маркетинг",
    "Журналистика",
    "Право",
    "Екология",
    "Езикознание",
    "Изкуствен интелект",
    "Компютърна сигурност",
    "Биология",
    "Астрономия",
    "Макроикономика",
    "Микроикономика",
    "Генетика",
    "Изкуство",
    "Геометрия",
    "Алгебра",
    "Стереометрия",
    "Тригонометрия"
]

# Fetch and store articles
fetch_and_store_articles(domains)
