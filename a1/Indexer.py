from collections import Counter
import math
import json
import copy


def indexer(document_word_dict):

    all_tokens = []

    # Iterate through document_word_dictionary to retrieve the tokens obtained from the preprocessing module and store them in token_words list for
    # each document
    for docID in document_word_dict:
        token_words = document_word_dict.get(docID)

        # Iterate through token_words and add the word to the list of all the words initially created to have a list of words across all the documents
        # the tokens are unique so we don't have any duplicate, now we need to use this to create a dictionary with the frequency of each token
        for token in token_words:
            if token not in all_tokens:
                all_tokens.append(token)

    frequency_dict = {}
    for token in all_tokens:
        frequency_dict[token] = {}
    
    # Create a count_words_in_doc dictionary to using Counter to count frequency of appearance of each word in every document
    count_words_in_doc = {}
    for doc in document_word_dict:
        count_words_in_doc[doc] = Counter(document_word_dict[doc])
    
    # Creating a loop to iterate through Counters and get frequency values for words, store them in dictionary now we have all toens with
    # their respective frequency values
    for docID in count_words_in_doc:
        counter = count_words_in_doc.get(docID)
        for token in counter:
            token_frequency = counter.get(token)
            frequency_dict[token][docID] = token_frequency

    
    #copy frequency_dict to weighted_dict
    weighted_dict = copy.deepcopy(frequency_dict)
    
    for token in weighted_dict:

        #creates copy of weighted_dict[word]
        freq_in_documents_dict = weighted_dict[token]
        
        #calculates max_freq for a token in a document
        max_freq = 0
        for docID in freq_in_documents_dict:
            if freq_in_documents_dict[docID] > max_freq:
                max_freq = freq_in_documents_dict[docID]

        #calculate inv_doc_freq
        inverted_doc_freq = math.log((float (len(weighted_dict)) / len(freq_in_documents_dict)), 2)

        
        for docID in freq_in_documents_dict:

            #creates copy of documents[id]
            freq = freq_in_documents_dict[docID]

            #calculate word_freq
            word_freq = float(freq) / max_freq

            #calculate weight value and set weight value to dict
            freq_in_documents_dict[docID] = inverted_doc_freq * word_freq
    
    return weighted_dict

    










