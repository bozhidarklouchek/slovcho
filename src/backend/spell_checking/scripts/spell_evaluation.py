import csv, re, nltk
from tqdm import tqdm
from sklearn.metrics import f1_score

def calculate_scores(inp, ref, pred):
    # Convert sentences to lists of words
    inp = inp.split()
    ref = ref.split()
    pred = pred.split()

    # print(inp)
    # print(ref)
    # print(pred)

    # Calculate true positives, false positives, and false negatives
    woip = set(ref) - set(inp)
    woin = set(inp) - set(ref)
    positives = set(pred) - set(inp)
    negatives = set(pred) & set(inp)

    # print('positives', positives)
    # print('negatives', negatives)
    # print('TP', woip & positives)
    # print('FP', positives - woip)
    # print('FN', negatives & woin)
    # print('TN', negatives - (negatives & woin))

    true_positives = len(woip & positives)
    false_positives = len(positives - woip)
    false_negatives = len(negatives & woin)
    true_negatives = len(negatives - (negatives & woin))
    
    # if(
    #     true_positives + false_positives + false_negatives + true_negatives != len(set(pred)) or
    #     len(set(pred)) != len(set(inp)) or
    #     len(set(inp)) != len(set(ref))
    # ):
    #     raise Exception

    # Calculate precision
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

    # Calculate recall
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    # Calculate F1-score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    beta = 0.5
    fp5 = (1 + beta**2) * (precision * recall) / (((beta**2)*precision) + recall) if (precision + recall) > 0 else 0

    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)


    return precision, recall, f1, fp5, accuracy

for file in tqdm([
    'C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/scripts/spell_eval_no_NER.csv',
    'C:/Users/klouc/Desktop/slovcho/src/backend/spell_checking/scripts/spell_eval_NER.csv',


]):
    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        p = 0
        r = 0
        f1 = 0
        fp5 = 0
        accuracy = 0
        c = 0
        for row in csv_reader:

            inp = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['err'])
            ref = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['corr'])
            pred = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['pred'])

            # print()
            # print(inp)
            # print(ref)
            # print(pred)

            # inp = 'Това е столъ, за който гуворих който'
            # ref = 'Това е стола, за който говорих който'
            # pred = 'Товъ е стола, за който гуворих койту'

            score = calculate_scores(inp, ref, pred)
            p += score[0]
            r += score[1]
            f1 += score[2]
            fp5 += score[3]
            accuracy += score[4]
            c += 1
            # break


    print('precision:', p/c)
    print('recall:',r/c)
    print('f1:',f1/c)
    print('f0.5:',fp5/c)
    print('accuracy:',accuracy/c)

