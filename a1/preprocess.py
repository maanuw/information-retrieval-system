import nltk
import string
import os
import json
import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download nltk libraries if not available locally.
nltk.download('punkt')
nltk.download('stopwords')
#nltk.download('stem.porter')

def importCollection(collectionPath):
    '''
    This function imports all textual paragraphs from the collection of documents.
    TODO: Remove unwanted characters like '//, \\, |, ~, \'(num), .'
    :param string collectionPath: String path to the directory containing collection docs.
    :return: list of tokens for all documents.
    :returnType: Dictionary
    '''
    # Loop over all documents in the collection.
    vocabulary = dict()
    i = 0
    for filename in os.listdir(collectionPath):
        i = i + 1
        print(str(i) + " of 322")
        with open(os.path.join(collectionPath, filename), 'r') as f: 
            soup=BeautifulSoup(f, features='lxml', from_encoding="utf-8-sig")

        res=soup.findAll("text")
        # Token list for each document.
        docVocabulary = []
        # Add tokens for each document.
        for text in res:
            pattern = r'[0-9]'
            newStr = re.sub(pattern, '', str(text))
            docVocabulary.extend(tokenize(newStr.replace("<text>", "").replace("</text>", "").replace(",", " ").replace("-", " ")))
        
        # Add document tokens to all doc dictionary.
        vocabulary[filename]=docVocabulary
        
    # Create json file.
    makeJson(vocabulary, "./assets/collection-tokens")

    return vocabulary

def importQuery(queryPath):
    '''
    This function imports all queries from the collection of documents.
    TODO: Remove unwanted characters like '//, \\, |, ~, \'(num), .'
    :param string collectionPath: String path to the directory containing queries.
    :return: list of tokens for all queries.
    :returnType: Dictionary
    '''
    # Loop over all queries.
    queryVocabulary = dict()
    
    with open(os.path.join(queryPath, filename), 'r') as f: 
        soup=BeautifulSoup(f, features='lxml', from_encoding="utf-8-sig")

    resTitle=soup.findAll("title")
    resDescription=soup.findAll("desc")

    # Token list for each query.
    titleVocabulary = []
    descVocabulary = []
    # Add tokens for each query title.
    for title in resTitle:
        pattern = r'[0-9]'
        newStr = re.sub(pattern, '', str(title))
        titleVocabulary.extend(tokenize(newStr.replace("<title>", "").replace("</title>", "").replace(",", " ").replace("-", " ")))

    # Add tokens for each query description.
    for desc in resDescription:
        pattern = r'[0-9]'
        newStr = re.sub(pattern, '', str(desc))
        descVocabulary.extend(tokenize(newStr.replace("<desc>", "").replace("</desc>", "").replace(",", " ").replace("-", " ")))

    # Add document tokens to all doc dictionary.
    for i in range(len(resTitle)):
        queryVocabulary[i] = titleVocabulary[i].extend(descVocabulary[i])

    # Create json file.
    makeJson(queryVocabulary, "./assets/query-tokens")

    return queryVocabulary

def tokenize(text):
    '''
    Tokenizes a string using nltk PorterStemmer. Performs necessary stopword and punctuation deductions.
    Uses nltk stopwords along with custom stopwords.

    :param string text: Text string to tokenize.
    :return: Tokens from the string
    :returnType: List
    '''
    # Initialize porter stemmer.
    ps = PorterStemmer()

    # Custom Stopwards to tackle edge cases.
    edgeStopWords = ['``', '\'s', 'n\'t', '\'d', "\'\'"]

    # Set of all stopwords.
    allStopWords = set(stopwords.words('english')).union((line.strip('\n') for line in open("./assets/stopwords.txt", "r"))).union(edgeStopWords)
    
    # List of Tokenized paragraph.
    # TODO:  check if isnumeric() and isFloat(word) do the same thing.
    tokens = [ps.stem(word.lower()) for word in word_tokenize(text)
        if word.lower() not in allStopWords and word not in string.punctuation
        and not word.isnumeric() and not isFloat(word)]
    
    # Return token list.
    return tokens
    
def isFloat(s):
    '''
    Checks whether a string is a float.

    :param string s: String to verify.
    :return: True if the string s is float number, False otherwise.
    :returnType: boolean
    '''
    try:
        return float(s)
    except ValueError:
        return False

def makeJson(dictionary, filename):
    '''
    Dumps dictionary into a json file of the given name and path.

    :param dictionary: Dictionary to be dumped in the json file.
    :param filename: Path and filename of json file to be created.
    :return: null
    :returnType: null 
    '''
    with open(filename+".json", "w") as outfile:
        json.dump(dictionary, outfile)