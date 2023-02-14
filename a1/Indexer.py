import math
import json

from preprocess import makeJson

def createInvertedIndex(collectionTokens):
    '''
    Builds an inverted index for a vocabulary tokens.

    :params dict collectionTokens: A dictionary of tokens and the documents the occur in.
    :return: An invert index of tokens.
    :returnType: dict
    '''
    # List of unique token values.
    allTokens = []
    # List of tokens and docs they occur in.
    vocabulary = openDictionary(collectionTokens)
    # Total number of documents.
    noOfDocs = len(collectionTokens)

    # Get all token values.
    for document in vocabulary:
        allTokens.extend(vocabulary[document])

    # before: 2439989
    #print(allTokens)
    # Remove duplicate tokens.
    allTokens = list(dict.fromkeys(allTokens))
    print(allTokens)
    print(len(allTokens))
    # after: 135983
    #print(len(allTokens))
    #exit()

    # Indexing the tokens obtained.
    invertedIndex = dict()
    i = 0
    for token in allTokens:
        i = i + 1
        print(str(i) + " of " + str(len(allTokens)))
        # Store token data : df, idf, tfs.
        tokenInfo = dict()
        # Tfs for token in each document.
        tokenFreqs = dict()
        for document in vocabulary:
            # Get Tf for this document.
            tokenFreq = vocabulary[document].count(token)
            if tokenFreq > 0:
                # Add document to list of document: Tfs.
                tokenFreqs[document] = tokenFreq
        # Add Df, Idf values.
        tokenInfo['Df'] = len(tokenFreqs)
        tokenInfo['Idf'] = math.log((noOfDocs/len(tokenFreqs)), 2)
        # Calculate weight of tokens. Formula Tf*Idf
        for document in tokenFreqs:
            tokenFreqs[document] = tokenFreqs[document]*tokenInfo['Idf']
        tokenInfo['Tfs'] = tokenFreqs
        # Add to inverted index.
        invertedIndex[token] = tokenInfo
    # Create a list of each documents vector length.
    makeJson(invertedIndex, "./assets/inverted-index")

    return invertedIndex

def openDictionary(file):
    '''
    Function to open and load a json file as dictionary.

    :params string file: A filepath and name string.
    :return: Json file contents loaded as a dictionary.
    :returnType: dict
    '''
    with open(file) as json_file:
        data = json.load(json_file)

    return data








