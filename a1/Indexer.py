from collections import Counter
import math
import json
import copy


def indexer(document_word_dict):

### need to test code
    
    all_tokens = []

    # Iterate through document_word_dictionary to retrieve the tokens obtained from the preprocessing module and store them in token_words list for
    # each document
    for docID in document_word_dict:
        token_words = document_word_dict.get(docID)

        # Iterate through token_words and add the word to the list of all the words initially created to have a list of words across all the documents
        # the tokens are unique so we don't have any duplicate, now we need to use this to create a dictionary with the frequency of each token
        for token in token_words:
            if word not in all_tokens:
                all_tokens.append(token)

    frequency_dict = {}
    for token in all_tokens:
        frequency_dict[word] = {}
    
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


### need to make changes here!!

    #Save to folder
    #Important: When we test later, we only need to load the json file (No need to recreate a new file every query)
    frequency_dict_path = "Modules/data/frequency_dict.json"
    with open(frequency_dict_path, "w") as file:
        json.dump(frequency_dict, file)
    

    #############################
    #weighted_dict
    #This dictionary with weighted values will be used for queries

    #copy frequency_dict to weighted_dict
    weighted_dict = copy.deepcopy(frequency_dict)
    
    #frequency_dict size
    dict_size = len(weighted_dict)
    
    for word in weighted_dict:

        #creates copy of weighted_dict[word]
        documents = weighted_dict[word]
        
        #documents size
        doc_freq = len(documents)
        
        #calculates max_freq
        documents = weighted_dict.get(word,{})
        max_freq = 0
        for i in documents:
            if documents[i] > max_freq:
                max_freq = documents[i]

        #calculate inv_doc_freq
        inv_doc_freq = math.log((float(dict_size) / doc_freq), 2)

        
        for id in documents:

            #creates copy of documents[id]
            freq = documents[id]

            #calculate word_freq
            word_freq = float(freq) / max_freq

            #calculate weight value
            weight = inv_doc_freq * word_freq

            #set weight value to dict
            documents[id] = weight

            
    #Test out weighted_dict (can comment out)
    #print(weighted_dict)

    
    #Save to folder
    #Important: When we test later, we only need to load the json file (No need to recreate a new file every query)
    weighted_dict_path = "Modules/data/weighted_dict.json"
    with open(weighted_dict_path, "w") as file:
        json.dump(weighted_dict, file)
    
    #############################

    #This section below is no longer required
    
    #Returns both dictionaries (frequency_dict) and (weighted_dict)
    #return frequency_dict, weighted_dict

    










