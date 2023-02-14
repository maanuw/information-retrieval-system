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
    
    document_word_dict = {}
    
    for filename in os.listdir(filepath):
        with open("coll/"+filename, encoding = "utf-8") as file:
            doc = file.read()
            
        tree = ET.parse(doc)
        root = tree.getroot(tree)
        textList = []
        for text in root.iter('text'):
            textList.append(text.text)

        #print(len(textList))              
        exit()

if __name__=="__main__":
    main()