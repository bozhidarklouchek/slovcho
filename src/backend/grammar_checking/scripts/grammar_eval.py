import csv, re, nltk
from tqdm import tqdm

def calculate_scores(inp, ref, pred):
    # Convert sentences to lists of words
    inp = inp.split()
    ref = ref.split()
    pred = pred.split()

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

    true_positives = len(woip & positives)
    false_positives = len(positives - woip)
    false_negatives = len(negatives & woin)

    # Calculate precision
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

    # Calculate recall
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    # Calculate F1-score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    beta = 0.5
    fp5 = (1 + beta**2) * (precision * recall) / (((beta**2)*precision) + recall) if (precision + recall) > 0 else 0

    bleu_score = nltk.translate.bleu_score.sentence_bleu([ref], pred)

    return precision, recall, f1, fp5, bleu_score

for file in tqdm([
    'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/preds/CLEAN_gpt_giveerr_askerr.csv',
    'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/preds/CLEAN_bggpt_giveerr_askerr.csv',
    'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/preds/CLEAN_gpt_giveerr_askonlyiferr.csv',
    'C:/Users/klouc/Desktop/slovcho/src/backend/grammar_checking/data/preds/CLEAN_bggpt_giveerr_askonlyiferr.csv'

]):
    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        p = 0
        r = 0
        f1 = 0
        fp5 = 0
        bleu = 0
        c = 0
        for row in csv_reader:

            inp = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['err'])
            ref = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['corr'])
            pred = re.sub(re.compile(r'[^a-zA-Z0-9а-яА-Я\s]'), '', row['pred'])

            # print(inp)
            # print(ref)
            # print(pred)

            # inp = 'Това е стола, за когото говоря'
            # ref = 'Това е столът, за който говоря'
            # pred = 'Това е столът, за когото говоря'
            score = calculate_scores(inp, ref, pred)
            p += score[0]
            r += score[1]
            f1 += score[2]
            fp5 += score[3]
            bleu += score[4]
            c += 1


    print('precision:', p/c)
    print('recall:',r/c)
    print('f1:',f1/c)
    print('f0.5:',fp5/c)
    print('bleu:',bleu/c)
