# Imports
import string
import math
# step 1. Inputs will be - (i) query and (ii) inverted index.

# step 2. Identify the format of the inverted index.

# step 3. Format the query text.

# step 4. (Elaborate this)

def retriever(invertedIndex, queryVocabulary):
    '''

    '''
    queryTokenWeights = dict()
    queryVectorLengths = dict()
    queryTokenFreqs = dict()
    for query in queryVocabulary:
        queryTokens = queryVocabulary[query]
        weightedTokens = dict()
        squaredSum = 0
        tokenFound = false
        for token in queryTokens:
            tokenFreq = queryTokens.count(token)
            # TODO: Add check to see if token is in inverted index.
            if token in invertedIndex:
            # Calculate token weight.
                tokenFound = True
                tokenWeight = (0.5 + (0.5*tokenFreq))*invertedIndex[token]['Idf']
                weightedTokens[token] = tokenWeight
                squaredSum = squaredSum + tokenWeight**2
                queryTokenFreqs[token] = tokenFreq
        if tokenFound:
            queryTokenWeights[query] = weightedTokens
            queryVectorLengths[query] = math.sqrt(squaredSum)
    


        

    return 0

def ranker():
    '''
    '''
    return 0