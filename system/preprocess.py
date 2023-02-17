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
nltk.download('stem.porter')

# Initialize porter stemmer.
ps = PorterStemmer()

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
 
        resDoc=soup.findAll("doc")

        resDocNo=soup.findAll("docno")
        
        # Add tokens for each document.
        k = 0
        for doc in resDoc:
            # Extract text from docs.
            restext = doc.findAll("text")
            newStr=''
            # Doc has more than one text which will lead to list of docno to unmatch from list of text tags.
            if len(restext) > 1:
                for j in range (len(restext)):
                    obj = restext[j]
                    newStr += str(obj)
            else:
                # doc doesnt have text tags.
                if len(restext) == 0:
                    continue
                # doc has only one txt tag.
                obj = restext[0]
                newStr += str(obj)
            
            docVocabulary = []
            pattern = r'[0-9]'
            newStr = re.sub(pattern, ' ', str(newStr))
            # Tokenize
            docVocabulary.extend(tokenize(newStr.replace("<text>", "").replace("</text>", "").replace(",", " ").replace("-", " ").replace(".", " ").replace('\'', " ").replace('_', ' ')))
            # Add docno
            docNo = resDocNo[k]
            # add to vocabulary.
            vocabulary[str(docNo).replace("<docno>", "").replace("</docno>", "")] = docVocabulary
            k = k + 1
        
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
    
    with open(queryPath, 'r') as f: 
        soup=BeautifulSoup(f, features='lxml', from_encoding="utf-8-sig")

    resTitle=soup.findAll("title")
    resDescription=soup.findAll("desc")

    # Token list for each query.
    titleVocabulary = [[]]
    descVocabulary = [[]]
    # Add tokens for each query title.
    for title in resTitle:
        pattern = r'[0-9]'
        newStr = re.sub(pattern, '', str(title))
        titleVocabulary.append(tokenize(newStr.replace("<title>", "").replace("</title>", "").replace(",", " ").replace("-", " ").replace(".", " ").replace('\'', " ").replace('_', ' ')))

    # Add tokens for each query description.
    for desc in resDescription:
        pattern = r'[0-9]'
        newStr = re.sub(pattern, '', str(desc))
        descVocabulary.append(tokenize(newStr.replace("<desc>", "").replace("</desc>", "").replace(",", " ").replace("-", " ").replace(".", " ").replace('\'', " ").replace('_', ' ')))

    print(descVocabulary[50])
    # Add document tokens to all doc dictionary.
    for i in range(len(resTitle)+1):
        vocab = titleVocabulary[i] + descVocabulary[i]
        queryVocabulary[i] = vocab

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
    # Custom Stopwards to tackle edge cases.
    edgeStopWords = ['``', '\'s', 'n\'t', '\'d', "\'\'", "..."]

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