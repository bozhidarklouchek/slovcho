# Slovcho

Slovcho is a digital writing assistant in Bulgarian, that aims to make writing in correct Bulgarian easier and more accessible.

## Software

Slovcho's a React application that utilises npm as a package manager and flask as its server architecture. It utilises NLP models in its backend in order to classify style and correct errors.

The following files have been extracted from the codebase in order to make it clear the key parts of the submission.

## NLP Models

It comes with three models:
- style classification model: Classify the style of writing into one of five distinct classes (academic, administrative, creative, news or casual) using a multinomial Naive Bayes classifier.
- spell correction model: Identify and give suggestions for spelling mistakes using a Noisy Channel model, it can identify and correct:
  - non-word errors, which result in words that aren't valid and thus not present in the dictionary, and
  - real world errors, which result in words that are present in the dictionary, but are invalid in the current context
- grammar correction model: Uploaded to [huggingface](https://huggingface.co/thebogko/mt5-finetuned-bulgarian-grammar-mistakes). Identify and correct grammar mistakes using a fine-tuned version of Google's mt5-base model.

All of the models you can find uploaded in the [Google drive](https://drive.google.com/drive/folders/1vaJTNxh-6OFIuDHzjt4n67m4qq-ajCTd?usp=sharing).

## Data

The datasets used are bespoke and have been created for this specific project, but may be useful to others:
- style collection: NOT uploaded to huggingface as may contains sensitive information. Collection of Bulgarian sentences in various different writing styles.
- dictionary: Uploaded to [huggingface](https://huggingface.co/datasets/thebogko/bulgarian-dictionary-2024). Collection of Bulgarian one-word terms, along with a POS tag for each.
- spelling errors: Uploaded to [huggingface](https://huggingface.co/datasets/thebogko/bulgarian-spelling-mistakes). Dataset of spelling mistakes in Bulgarian that have been induced automatically on an originally correct dataset; the error types include:
  - changes in vowels depending on word stress,
  - changes in consonants depending on articles, pronounciation and syntax
  - random changes in characters
  - changes in characters that result in real world errors (words that are present in the dictionary, but are invalid in the current context)
- grammar errors: Uploaded to [huggingface](https://huggingface.co/datasets/thebogko/bulgarian-grammar-mistakes). Dataset of grammar mistakes in Bulgarian that have been induced automatically on an originally correct dataset. The error types include:
  - article misuse errors,
  - pronoun misuse errors,
  - verb suffixes errprs,
  - adjective-noun disagreement errors

All of the datasets you can find uploaded in the [Google drive](https://drive.google.com/drive/folders/1c_cdidKvW-kMg51Q0-lHWNocDRIlYnTo?usp=sharing).
