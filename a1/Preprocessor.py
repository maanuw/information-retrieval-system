from collections import Counter
import csv
import os
import re
import nltk
from nltk.stem.snowball import EnglishStemmer
import string
from nltk import TreebankWordTokenizer
import json
from pathlib import Path
import xml.etree.ElementTree as ET

# author: Simon Proulx 300067852
# comments: code is not currently finished. Full version will be available soon



def main():
    do_preprocessor('')

def do_preprocessor(filepath):
    
    filepath = 'coll'
    
    punct_set = set(string.punctuation)
    
    print(filepath)
    
    document_word_dict = {}
    
    for filename in os.listdir(filepath):
        p = Path(filepath+"/"+filename)
        p.rename(p.with_suffix('.xml'))
        
        with open(filepath+"/"+filename+".xml", encoding = "utf-8-sig") as file:
            
            tree = ET.fromstring(file.read())
            for node in tree.iter('text'):
                print('\n')
                
            
            
            
        pr = Path(filepath+"/"+filename+".xml")
        pr.rename(p.with_suffix(''))
    


    #Save to folder
    #Important: When we test later, we only need to load the json file (No need to recreate a new file every query)
    document_word_dict_path = "document_word_dict.json"
    with open(document_word_dict_path, "w") as file:
        json.dump(document_word_dict, file)  
    
    #Create a temporary dict for (document_word_dict)
    tmp_dict = document_word_dict
    #print(tmp_dict)

    
    

    #Create document_word_count_dict
    document_word_count_dict = {}
    for doc in tmp_dict:
        document_word_count_dict[doc] = Counter(tmp_dict[doc]);
    #print(document_word_count_dict)


    #Returns both dictionaries (document_word_dict) and (document_word_count_dict)
    return document_word_dict, document_word_count_dict # only need tokenized dictionary

if __name__=="__main__":
    main()