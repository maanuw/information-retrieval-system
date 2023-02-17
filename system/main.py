from writer import generateResultsTable
from Indexer import createInvertedIndex
from rankerAndRetriever import rankAndRetrieve
from preprocess import importCollection, importQuery

def main():
    print ("\n CSI - 4107 - Information Retrieval System \n")

    print("\n Importing collection of documents ...\n")
    collectionPath = './coll'

    # Import all documents from the coll directory.
    importCollection(collectionPath)

    print("\n Importing queries ...\n")
    # Import all queries.
    queryVocabulary = importQuery('./assets/queries')

    print("\n Creating index ...\n")
    # Create inverted index.
    collectionTokens = './assets/collection-tokens.json'
    index, documentVectors = createInvertedIndex(collectionTokens)

    # Rank and retrieve.
    print("\n Ranking and retrieving ...\n")
    results = rankAndRetrieve(index, queryVocabulary, documentVectors)

    # Makes the Results.txt file.
    generateResultsTable(results)

if __name__ == "__main__":
    main()