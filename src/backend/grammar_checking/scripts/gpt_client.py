import openai
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import time
import csv
from tqdm import tqdm

MAX_SENT_LENGTH = 300

client = openai.OpenAI(api_key="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")


df = pd.read_csv(f'C:/Users/klouc/Desktop/slovcho/src/backend/data/article_pronoun_mistakes.csv')

# Clean from ___
df['erroneous'] = df['erroneous'].apply(lambda x: re.sub(r'___', r'', x))
df['correct'] = df['correct'].apply(lambda x: re.sub(r'___', r'', x))

# Chars limit
error_mask = df['erroneous'].str.len() <= MAX_SENT_LENGTH
correct_mask = df['correct'].str.len() <= MAX_SENT_LENGTH
mask = []
for c,e in zip(correct_mask, error_mask):
    mask.append(c and e)
df = df[pd.Series(mask)]

print(f'Trimmed to {len(df["correct"])} pairs')

X = df['erroneous']
y = df['correct']

# Split into train, val, test (72/18/10)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                               test_size=0.10,
                                               shuffle=True,
                                               random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                  test_size=0.20,
                                                  shuffle=True,
                                                  random_state=42)

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

# it = 1
# for t in X_test:
#     if(it <= 109):
#         it += 1
#         continue
#     else:
#         print(t)
#         break


def getGPTPreds(error):
    tryAgain = True
    while tryAgain:
        tryAgain = False
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "assistant", "content": ""},
                    {
                    "role": "user",
                    "content": f"Прегледай следното изречение и го препиши, като поправиш грешки в него, ако то има такива: {error}",
                    }
                ],
                n=3
                )
            res = [content.message.content for content in response.choices]
            print(res)
            return res
        except:
            print('i sleep 60')
            tryAgain = True
            time.sleep(60)
        
    

with open('C:/Users/klouc/Desktop/slovcho/src/backend/data/gpt_givecorr_askonlyiferr2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['err', 'corr', 'pred', 'time_for_batch_of_3'])

    it = 1
    for err, corr in tqdm(zip(y_test, y_test), total=len(y_test)):
        if(it <= 125):
            it += 1
            continue
        it += 1
        start = time.time()
        preds = getGPTPreds(err)
        end = time.time() - start
        print('waiting 300')
        time.sleep(60)

        for pred in preds:

            writer.writerow([err, corr, pred, end])




