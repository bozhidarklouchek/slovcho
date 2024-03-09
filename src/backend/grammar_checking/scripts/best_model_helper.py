import json
from collections import defaultdict
file_path = "data.json"

mt5 = 'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/finetuning/mt5/{ITER}/mt5_{HP_COMBO}.json'
rnn = 'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/finetuning/RNN/{ITER}/RNN_{HP_COMBO}.json'

# mt5
model_map = defaultdict(list)
for iter in range(1, 4):
    best_val = 100
    best_setup = None
    for hp_combo in range(1, 19):
        with open(mt5.replace('{ITER}', str(iter)).replace('{HP_COMBO}', str(hp_combo)), "r") as json_file:
            data = json.load(json_file)
            for id, epoch in enumerate(data['model_deets']):
                if('train_runtime' not in epoch):
                    hp = f"batch_size - {data['batch_size']}, lr_rate - {data['lr_rate']}, w_decay - {data['w_decay']}, epoch - {id+1}"
                    model_map[hp].append(epoch['val_loss'])
                    if(best_val > epoch['val_loss']):
                        best_val = epoch['val_loss']
                        best_setup = hp
    # print(best_setup, best_val)
    # print(model_map)

best_val = 100
best_setup = None
for hp in model_map:
    if(best_val > sum(model_map[hp])/3):
        best_val = sum(model_map[hp])/3
        best_setup = hp

print('mt5')
print(model_map[best_setup])
print(best_setup, best_val)


# rnn
model_map = defaultdict(list)
for iter in range(1, 4):
    best_val = 100
    best_setup = None
    for hp_combo in range(1, 28):
        with open(rnn.replace('{ITER}', str(iter)).replace('{HP_COMBO}', str(hp_combo)), "r") as json_file:
            data = json.load(json_file)
            for id, epoch in enumerate(data['model_deets']):
                hp = f"batch_size - {data['batch_size']}, lr_rate - {data['lr_rate']}, embed_dim - {data['embed_dim']}, epoch - {id+1}"
                model_map[hp].append(epoch['val_loss'])
                if(best_val > epoch['val_loss']):
                    best_val = epoch['val_loss']
                    best_setup = hp
                if(id == 19): break
    # print(best_setup, best_val)
    # print(model_map)

best_val = 100
best_setup = None
for hp in model_map:
    if(best_val > sum(model_map[hp])/3):
        best_val = sum(model_map[hp])/3
        best_setup = hp

print('rnn')
print(model_map[best_setup])
print(best_setup, best_val)
