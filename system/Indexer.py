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
    allTokens = dict()
    # List of tokens and docs they occur in.
    vocabulary = openDictionary(collectionTokens)
    # Total number of documents.
    noOfDocs = len(vocabulary)

    # Get all token values.
    for document in vocabulary:
        # For each document.
        for token in vocabulary[document]:
            # For each token in this document. 
            if token not in allTokens and len(token) > 2:
                # Check if token exists and its length.
                allTokens[token] = [{document: 1}]
            elif token in allTokens:
                # Case: token already exists and doc too.
                if document in allTokens[token][0]:
                    allTokens[token][0][document] += 1
                elif document not in allTokens[token]:
                    allTokens[token][0][document] = 1
        
    print(len(allTokens))

    # Indexing the tokens obtained.
    i = 0
    for token in allTokens:
        i = i + 1
        print(str(i) + " of " + str(len(allTokens)))
        # Store token data : df, idf, tfs.
        tokenInfo = dict()
        # Add Df, Idf values.
        tokenInfo['Df'] = len(allTokens[token][0])
        tokenInfo['Idf'] = math.log((noOfDocs/len(allTokens[token][0])), 2)
        # Calculate weight of tokens. Formula Tf*Idf.
        for document in allTokens[token][0]:
            allTokens[token][0][document] = allTokens[token][0][document]*tokenInfo['Idf']
        # Add to inverted index.
        allTokens[token].append(tokenInfo)


    # Create a list of each documents vector length.
    documentVectorlenghts = dict()
    for document in vocabulary:
        documentTokens = list(dict.fromkeys(vocabulary[document]))
        squaredSum = 0.0
        for token in documentTokens:
            if token in allTokens:
                squaredSum = squaredSum + (allTokens[token][0][document]*allTokens[token][0][document])
        documentVectorlenghts[document] = math.sqrt(squaredSum)


    makeJson(allTokens, "./assets/inverted-index")
    makeJson(documentVectorlenghts, "./assets/doc-vector-lengths")

    return allTokens, documentVectorlenghts

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