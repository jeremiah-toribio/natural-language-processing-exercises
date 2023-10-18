# arrays
import numpy as np
import pandas as pd
# nlp
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
# ascii manipulation
import unicodedata
# regex
import re
# my scripts
import acquire as a

def basic_clean(data):
    '''
    Prepares data to move forward into exploration.
    '''

    # Lower
    data = data.lower()

    # Replace anything that is not a letter, number, whitespace, single quote
    data = re.sub(r'[^\w\s]', '', data)
    data = re.sub(r"[^a-z0-9'\s]", '', data)
    # Normalize unicode
    data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    return data

def tokenize(data):
    '''
    Tokenizes data to then be stemmed and lemmed
    '''
    # Tokenizer obj
    tokenizer = nltk.tokenize.ToktokTokenizer()

    # Tokenize
    data = tokenizer.tokenize(data, return_str=True)

    return data

def stem(data):
    '''
    Returns the stems of provided data.
    '''

    # Stem obj
    ps = nltk.porter.PorterStemmer()

    # Stemming
    stems = [ps.stem(word) for word in data.split()]

    # Combine
    data_stemmed = ' '.join(stems)

    return data_stemmed

def lemmatize(data):
    '''
    Returns the provided data lemmatized
    '''

    # Lem obj
    wnl = nltk.stem.WordNetLemmatizer()

    # Lemming
    lemmas = [wnl.lemmatize(word) for word in data.split()]

    # Combine
    data_lemmatized = ' '.join(lemmas)

    return data_lemmatized

def remove_stopwords(data, extra_words=None, exclude_words=None):
    '''
    Removes the stopwords from data.

    Adding/removing words will be passed as a list in str format

    Returns data with no stopwords
    '''
    # Setting stopwords
    stopwords = nltk.corpus.stopwords.words('english')

    # Removing extra words if applicable
    if exclude_words is not None:
        stopwords = [word for word in stopwords if word not in exclude_words]

    # Adding extra words if applicable
    if extra_words is not None:
        stopwords.extend(extra_words)



    # splitting on words
    words = data.split() 
    
    # filtering
    filtered_words = [w for w in words if w not in stopwords]

    data_no_stopwords = ' '.join(filtered_words)

    print(f'Removed {len(words) - len(filtered_words)} stopwords')
    print('---')


    return data_no_stopwords


def prep_data(data, text='content',extra_words=None, exclude_words=None, stem=None,lemme=None):
    '''
    Uses basic clean, tokenize, stem, lemmetize functions on a string of data.

    

    Has extra_words and exclude words parameters for stop words.
    '''

    # cleaning data
    cleaned = data[text].apply(basic_clean)

    # tokenize
    cleaned = cleaned.apply(tokenize)

    # removing stopwords
    cleaned = cleaned.apply(remove_stopwords(cleaned, extra_words= extra_words, exclude_words= exclude_words))

    # stem or lemme
    if stem == True:
        stem = stem(cleaned)
    elif lemme == True:
        lemmetized = cleaned.apply(lemmatize)
        return cleaned, lemmetized
    else:
        return TypeError('Missing stem or lemme positional argument.')
    

    return cleaned, stem 





