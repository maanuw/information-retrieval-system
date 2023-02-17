

# CSI4107 Assignment 1

## Reference

https://www.site.uottawa.ca/~diana/csi4107/A1_2023.htm

## Author

Manav Patel - 300074687

## Task Distribution

Manav Patel
- Step 1, Step 2, Step 3 
- (I have emailed Professor Diana regarding my group sitution).

## Setting up

Prerequisites:

1. `python3` installed and executable.
2. `nltk` libaries installed (all of these can be downloaded using `python3` -> `import nltk` -> `nltk.download('corpus | tokenize | stem.porter')`: 
	  - `corpus`
	  - `tokenize`
	  - `stem.porter`
3.  `prettytable`
4.  `re`
5.  `bs4` libraries installed for beautifulSoup
      - `BeautifulSoup`
 
## Project Overview

The `assets/` directory contains all the information provided for this assignment:
- `stop_words.txt` - A collection of stopwords, and
- `queries` - A collection of 50 test queries.
- `qrels1-50ap.txt` - Provided relevance feedback file.

The `coll/` directory contains all the documents provided for this assignment.

The `trec_eval_latest/` directory contains necessary file to install the trec eval script.

Other files in the root directory include:
- `eval.sh` - This script can be run by command `sh eval.sh` which in turn will run the trec eval software.
- `Results.txt` - Contains a collection of all 50 test queries, and their corresponding relevant documents, ordered by highest to lowest relevance. 
- `trec_eval_all_query.txt` - Resulting file from Trec Eval execution. This file contains a detailed comparision of `Results.txt` against `qrels1-50ap.txt`.
		

## Execution

Once all of the prerequesits are met, the program can be ran with:
**```python3 main.py```**

This will generate `Results.txt` in the `root` directory in the following format: 

        topic_id  Q0  docno            rank   score                   tag      
        1         Q0   AP880813-0156   0      0.0010272398719625396   run_name 
        1         Q0   AP881225-0023   1      0.001098417624315712    run_name 
        1         Q0   AP881224-0092   2      0.0011021651736541232   run_name 
        1         Q0   AP880518-0138   3      0.0011123056312694372   run_name 

Additionally it will also generate the following files in the `./assets` directory:
- `collection-tokens.json` - Json file that contains all the preprocessed and stemmed tokens for each doc.
- `inverted-index.json` - Json file that contains the inverted index.
- `doc-vector-lengths.json` - Json file that contains the length of all document vectors.
- `query-index.json` - Json file containing query index.
- `query-related-docs.json`- Json file containing documents that are related to each query.
- `query-tokens.json` - Json file that contains token info for each query.
- `query-vector-lengths.json` - Json file that contains the length of all document vectors.
- `rankedResult.json` - Json version of the Results.

## Evaluation

To evaluate the effectiveness of our Information retrieval system:

- Run the `eval.sh` script. Running this script will create a txt file called `trec_eval_all_query.txt` which will list the overall performance measures of the code for all the queries as a whole.

## Functionality

Our task for this assignment was to implement an Information Retrieval (IR) system for a collection of documents. A brief summary of what the system does as a whole:

1. We import all the documents files and the query file. We process the files using BeautifulSoup to extract from the <text> <docno> (for documents) <title> and <desc> for the query file. We perform stemming andd stopword removal on the extracted words to tokenize these words and stored them in dictionaries. This allowed the words to formatted in way that could be easily read and accessed by the python code.

2. The system creates an inverted index dictionary that contains all the unique tokens along with important information such **Df** and **Idf** values. Moreover, it also stores doc numbers in which these words occur and along with these documents we store the weight of tokens for that specific document. To calculate the weight of tokens we use the **Df** to calculate the **Idf** (Formula: Log<sub>2</sub>(Total number of documents/Document frequency of the term)) and then we use the **Tf*Idf** formula.

3. We create a query index which contains all the tokenized words from the 50 queries along with their **Tf** and `Token weights`. More over another index/dictionary is created that contains the query IDs and the documents that relate to that ID. Finally we calculate the `CosSim` values for the words to find their similarity score with the query. The results are order in descending order based on the similarity score of each document with a query. Ultimately a Results.txt file is created with this information.

## Algorithms, Data Structures, and Optimizations

  Our implementation of the information retrieval system was based on the guidelines provided in the assignment. The folder contains five python files containing the function used in implementing the IR system. 

### Project Specific Files

#### `main.py`:
  This file contains the main() function. In the `main()`, we started by importing the important functions that were used for implementing the IR system. TThe system starts its process by importing the collection documents and the query file. By importing the documents and queries from the `asset folder`, `step1: preprocessing` commences using `tokenize()` function that gets called from the  `importCollections()` and `importQuery` functions. Once the words are tokenized and preprocessed the system begins building the `inverted index` for the the documents. We got the `index and document length vector list`, which is then used for the retrieval and ranking process. In the `retrievalandranking` function, the CosSimalarity scores are calculated along with ranking and a dictionary for the mentioned is returned. 
#### Preprocess.py:
 This file contains the process of developing `step1:Preprocessing` and `step2:Indexing` using python. Below are the functions implemented in the `preprocess.py`
 - isFloat(s): Check if a string contains float values.
 - importCollection(): imports the documents from the collection. We first started by opening and parsing the text files using `BeautifulSoup`, then we filter the file using our `tokenize` function.
 - importQuery(): imports query from the query file. Same process as the importCollection().
 - tokenize(text): processes parsed sentences from documents and queries. This function builds a list of `stopwords` and then `tokenizes` each word in the paragraphs by removing any numerics, punctuation, special symbols or stopwords contained in the list. Each imported doc and query runs through the 
 `NLTK's stopword list`, a `custom stopword list` that included the  `abbreviations and special characters`, and the provided `stopword list`. After this step, each word is tokenized and stemmed with `Porter stemmer`. Under the `additional libraries` section, we discussed in-depth the use of `tokenization`, `stopwords`, and `porter stemmer`.
 - makeJson(): This is a helper function to create json files for relevant dictionaries.
 #### Indexer.py
 - createInvertedIndex(collectionTokens): builds the inverted index for each entry word in the vocabulary. The data structure used for the implementation was hash maps. In the realms of python development, dictionaries are equivalent to hash maps. We used dictionaries for storing the data that was being processed and used for the documents and queries. We initialized an `allTokens`  as an empty dictionary and started iterating through a vocabulary of unique words/tokens. Since initially with 130k words the estimated time to build the index was 6 hours, we pruned words of length 2. We also optimized this section of the index building by storing documents related to a token and token frequencies as we iterated through the vocabulary to create our set of unique tokens. This was a vast improvement from our previous implementation and changed our estimated time of building an index to seconds. In this way we eliminated alot of recurrent iterations in this section of code. Ultimately we store the df, idf documents related to each tokens and token weights in the index. This function also creates another dictionary that contains the length of document vectors for each document. 

#### rankerAndRetriever.py 
  This file contains the function for calculating the Cosimilarity values for the set of documents against each queries and then ranks the similarity scores in descending order. Dictionary was used as our main source for storing the values of the `queryIndex`, `documentLength`.  and the `queryVectorLength`. At the start, we first calculated the occurrences of the token in each query. We then moved to calculate the `TF-IDF` and the `length of the query` and creating a `queryindex`. After getting the necessary calculations needed, we then moved to solving the `CosSimalarity values` and then `ranking the document` according to the order that was specified.
#### write.py: 
  The function creates a table for each of the results generated in the `result.py`.
 
### Additional Libraries

#### Prettytable (`prettytable.py`):  
 
A helper library to format the output for the `Results.txt` file. Used in `write.py`.

#### NLTK:

#### PorterStemmer
Porter stemmer was an external resource that was used in the implementation of `tokenize(text)`. It was used for normalizing the data for each token that was created. Stemming helps remove the morphological and inflexional endings from words in the text file.
#### Stopwords
Stopwords were also used in the preprocessing of the data. Since stopwords are common that generally do not contribute to the meaning of a sentence, we tend to filter them out which can be seen done in the `tokenize(text)` function.
#### Tokenizer
We Tokenized our data in the `tokenize(text)` so as to provide a link between queries and documents. Tokens are sequences of alphanumeric characters separated by nonalphanumeric characters, which are performed as part of the preprocessing (`step1` requirement).

## Final Result Discussion
  The following is the evaluation of our system using the trec_eval script by comparing our results (`Results.txt`) with the expected results from the provided relevance feedback file.

    runid                 	all	run_name
    num_q                 	all	50
    num_ret               	all	2270913
    num_rel               	all	2099
    num_rel_ret           	all	2090
    map                   	all	0.2399
    gm_map                	all	0.1238
    Rprec                 	all	0.2591
    bpref                 	all	0.2966
    recip_rank            	all	0.4985
    iprec_at_recall_0.00  	all	0.5510
    iprec_at_recall_0.10  	all	0.4430
    iprec_at_recall_0.20  	all	0.3671
    iprec_at_recall_0.30  	all	0.3267
    iprec_at_recall_0.40  	all	0.2718
    iprec_at_recall_0.50  	all	0.2465
    iprec_at_recall_0.60  	all	0.2077
    iprec_at_recall_0.70  	all	0.1667
    iprec_at_recall_0.80  	all	0.1177
    iprec_at_recall_0.90  	all	0.0760
    iprec_at_recall_1.00  	all	0.0338
    P_5                   	all	0.3640
    P_10                  	all	0.3160
    P_15                  	all	0.2987
    P_20                  	all	0.2870
    P_30                  	all	0.2553
    P_100                 	all	0.1562
    P_200                 	all	0.1011
    P_500                 	all	0.0543
    P_1000                	all	0.0316


From an overall perspective, The result seems okay, but not as accurate as I expected. I had to make some tweaks in my preprocessor and index builder to increase the `MAP` score from `0.08` to `0.2399`/`23.99%`. I made optimizations to the indexer script as mentioned above in detail which helped me achieve this map score. I have noticed some anomalies with our python code that generates the idf scores. It is sensible to presume that on debugging those calculations would potentially help in improving the system. However since, fundamentally the logic of the system stands correct, some fine tuning can do the trick such as, check the preprocessing, tokenizing and Idf values. However, given an opportunity the system can definitely be improved.

## Results from Queries 1 and 25

### Query 1

    topic_id  Q0  docno            rank   score                   tag      
    1         Q0   AP881122-0107   0      0.00028492614143231867  run_name 
    1         Q0   AP880617-0251   1      0.00029109700342177234  run_name 
    1         Q0   AP880615-0271   2      0.00029110276006548983  run_name 
    1         Q0   AP881109-0243   3      0.0002967841212215339   run_name 
    1         Q0   AP880425-0253   4      0.000297316484102289    run_name 
    1         Q0   AP880608-0267   5      0.0003133702558078317   run_name 
    1         Q0   AP880828-0010   6      0.0003172351906365927   run_name 
    1         Q0   AP881014-0266   7      0.000317508479203022    run_name 
    1         Q0   AP880411-0266   8      0.0003255881149707923   run_name 
    1         Q0   AP880706-0272   9      0.00033082409268940223  run_name 
    1         Q0   AP880408-0274   10     0.00033891508004051476  run_name 
     

### Query 25

    topic_id  Q0  docno            rank   score                   tag      
    25        Q0   AP880810-0267   0      0.00011697465198517658  run_name 
    25        Q0   AP880222-0182   1      0.00013987848077943218  run_name 
    25        Q0   AP880328-0238   2      0.0001585303716096217   run_name 
    25        Q0   AP881115-0250   3      0.00016187624911542467  run_name 
    25        Q0   AP880331-0289   4      0.00016222286029245357  run_name 
    25        Q0   AP880803-0015   5      0.00016424679459163636  run_name 
    25        Q0   AP880829-0220   6      0.00016608987874675824  run_name 
    25        Q0   AP881023-0004   7      0.0001693222307167516   run_name 
    25        Q0   AP880418-0006   8      0.00017211658683608536  run_name 
    25        Q0   AP880327-0104   9      0.00017214753439692083  run_name 
    25        Q0   AP880618-0018   10     0.00017450564860668137  run_name 
        
## Discussion

To my surprise the results of `MAP` score when using query title and query description and using just query title was not very different in terms of metric. This maybe because of the description containing too many stop words and not a lot more important words than in the title.
The `MAP`(`21.19%`) score below is while using tokens from only title. The table showed above with `MAP` score of `23.99%` is using title and description.

    runid                 	all	run_name
    num_q                 	all	50
    num_ret               	all	762721
    num_rel               	all	2099
    num_rel_ret           	all	1977
    map                   	all	0.2119
    gm_map                	all	0.0910
    Rprec                 	all	0.2396
    bpref                 	all	0.2804
    recip_rank            	all	0.4420
    iprec_at_recall_0.00  	all	0.4992
    iprec_at_recall_0.10  	all	0.3955
    iprec_at_recall_0.20  	all	0.3228
    iprec_at_recall_0.30  	all	0.2898
    iprec_at_recall_0.40  	all	0.2473
    iprec_at_recall_0.50  	all	0.2156
    iprec_at_recall_0.60  	all	0.1799
    iprec_at_recall_0.70  	all	0.1346
    iprec_at_recall_0.80  	all	0.1029
    iprec_at_recall_0.90  	all	0.0668
    iprec_at_recall_1.00  	all	0.0329
    P_5                   	all	0.3120
    P_10                  	all	0.3000
    P_15                  	all	0.2733
    P_20                  	all	0.2600
    P_30                  	all	0.2333
    P_100                 	all	0.1420
    P_200                 	all	0.0936
    P_500                 	all	0.0506
    P_1000                	all	0.0297
    
## Vocabulary
  
Our vocabulary size was `121514` tokens
  
Below is the sample of 100 tokens from our vocabulary:
  
win
weekli
state
lotteri
number
pick
friday
lotto
win
weekli
state
lotteri
number
pick
lotto
play
wednesday
megabuck
pick
lotto
bonu
wednesday
lotto
game
supplementari
big
lotteri
grand
lot
game
tent
schedul
presidenti
candid
juli
inform
candid
sunday
juli
democrat
dukaki
colorado
jackson
san
franicisco
dalla
fort
worth
texa
republican
bush
washington
monday
juli
democrat
dukaki
boston
jackson
washington
cincinnati
republican
bush
washington
tuesday
juli
democrat
dukaki
boston
jackson
washington
republican
bush
washington
cincinnati
wednesday
juli
democrat
dukaki
open
jackson
chicago
republican
bush
washington
thursday
juli
democrat
dukaki
open
jackson
chicago
indianapoli
republican
bush
open
friday
juli
democrat
dukaki
open
