from joblib import load
import sys

def classify_style(text):
    classifier = load('src/backend/style_classification/style_classification.joblib')
    print(classifier.predict([text])[0])

if(sys.argv[1] == 'classify_style'):
    text = sys.argv[2]
    classify_style(text)
