from datasets import load_dataset
import csv
import time

# from huggingface_hub import login
# login()

# If the dataset is gated/private, make sure you have run huggingface-cli login
dataset = load_dataset("oscar-corpus/OSCAR-2301",
                        use_auth_token=True, # required
                        language="bg",
                        streaming=True, # optional
                        split="train") # optional

LIMIT_VAL = 100000
oscar_c = 0
c = 0
buff = []
start_time = time.time()
dataset.shuffle()
for d in dataset:
    for line in d['text'].split('\n'):
        if(len(line) > 50):
            buff.append(
                {
                    'id': d['id'],
                    'type': d['meta']['warc_headers']['warc-type'],
                    'uri': d['meta']['warc_headers']['warc-target-uri'],
                    'text': line
                }
            )
        if(len(buff) >= LIMIT_VAL):
            with open(f'C:/Users/klouc/Desktop/oscar/oscar_{oscar_c}.csv', 'w', encoding="utf-8")as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'oscar_id', 'oscar_type', 'uri', 'text'])
                for b in buff:
                    writer.writerow([c, b['id'], b['type'], b['uri'], b['text']])
                    c += 1
            buff = []
            end_time = time.time()
            print(f'Finished file {oscar_c} for: {end_time - start_time} seconds')
            start_time = time.time()
            oscar_c += 1
