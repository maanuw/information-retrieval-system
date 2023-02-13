# Imports
import string
import xml.etree.ElementTree as ET
from nltk import TreebankWordTokenizer
from nltk.stem.snowball import EnglishStemmer
# step 1. Inputs will be - (i) query and (ii) inverted index.

# step 2. Identify the format of the inverted index.

# step 3. Format the query text.

# step 4. (Elaborate this)


def do_query(queries):
    name = "run_name"
    # Passing the path of the
    # xml document to enable the
    # parsing process
    tree = ET.parse('test-queries.xml')
    root = tree.getroot()
    print(root)
    # Preprocess the query.


def preprocess_query(query):
    # Initialze a list of punctuations.
    punctuations = list(string.punctuation)

    # Initialize a list of stopwords.
    with open('stopwords.txt') as f:
        # List of stopwords
        stopwords = f.readlines()
    
    # Tokenize words (Maybe find a different way to do it.)
    words = []
    for i in TreebankWordTokenizer().tokenize(query):
        if i.lower() not in stopwords and i.lower() not in punctuations:
            try:
                words.append(EnglishStemmer().stem(i.lower()))
            except:
                words.append(i.lower())

    




do_query('test-queries.xml')
#preprocess_query()


# Tf - term frequency
# idf - inverse document frequency