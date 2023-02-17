# Imports
import string
import math

from preprocess import makeJson
# step 1. Inputs will be - (i) query and (ii) inverted index.

# step 2. Identify the format of the inverted index.

# step 3. Format the query text.

# step 4. (Elaborate this)

def rankAndRetrieve(invertedIndex, queryVocabulary, documentLengths):
    '''
    This functions creates index for queries and then retrieves tokens for each query.
    Function ranks the retrieved docs.

    :param dict invertedIndex: Of vocabulary tokens.
    :param dict queryVocabulary: Created from imported queries 
    :param dict documentLengths: doc ids and their vector lengths.
    :return: rankedQueryDocs
    :returnType: dict
    '''
    # Length of query vector for each query.
    queryVectorLengths = dict()
    # Documents related to query.
    queryRelatedDocs = dict()
    # Build query index.
    queryIndex = dict()
    
    # Build query index, list of docs related to query, list of query vector lengths.
    for query in queryVocabulary:
        # list of tokens of each query.
        queryTokens = queryVocabulary[query]
        # query tokens and info.
        queryDict = dict()
        squaredSum = 0
        tokenFound = False
        # Token related docs.
        docs = []
        for token in queryTokens:
            tokenDict = dict()
            tokenFreq = queryTokens.count(token)
            
            # TODO: Add check to see if token is in inverted index.
            if token in invertedIndex:
                # Calculate token weight.
                tokenFound = True
                tokenWeight = (0.5 + (0.5*tokenFreq))*invertedIndex[token][1]['Idf']
                squaredSum = squaredSum + tokenWeight**2
                # Add token related docs.
                docs.extend(list(invertedIndex[token][0]))
                tokenDict = {"Tf": tokenFreq, "tokenWeight": tokenWeight}
                queryDict[token] = tokenDict
        # Add docs related to all tokens of a query.
        queryRelatedDocs[query] = list(dict.fromkeys(docs))
        queryVectorLengths[query] = math.sqrt(squaredSum)
        queryIndex[query] = queryDict
        
    makeJson(queryIndex, './assets/query-index')
    makeJson(queryRelatedDocs, './assets/query-related-docs')
    makeJson(queryVectorLengths, './assets/query-vector-lengths')

    # Cossimilarity.
    rankedQueryDocs = dict()
    for query in queryIndex:
        print(query)
        queryTokens = queryVocabulary[query]
        cosSimilarityValues = dict()
        for document in queryRelatedDocs[query]:
            cosSimilarityValues
            product = 0.0
            for token in queryTokens:

                # Check if token is in present in this document.
                try:
                    documentWt = invertedIndex[token][0][document]
                except KeyError:
                    # Could not find token in doc, next token.
                    continue
                # If token found in doc successfully, calculate product.
                product = product + (documentWt * queryIndex[query][token]['tokenWeight'])
                
            # Check if product is 0
            if product == 0.0:
                # If so, go to next document related to query.
                continue
                
            # Calculate Cossimilarity value.
            try:
                cosSimilarityValues[document] = product/(queryVectorLengths[query]*documentLengths[document])
            except ZeroDivisionError:
                continue
            
        # Sorting in descending order.
        # TODO: Make it work. Currently sorting in write.py file.
        rankedQueryDocs[query] = {k: v for k, v in sorted(cosSimilarityValues.items(), key=lambda cosSimilarityValues: cosSimilarityValues[1], reverse=True)}

    makeJson(rankedQueryDocs, "./assets/rankedResult")
    
    return rankedQueryDocs