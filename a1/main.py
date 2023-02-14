from preprocess import importCollection


def main():
    print ("\n CSI - 4107 - Information Retrieval System \n")

    print("\n Importing collection of documents ...\n")
    collectionPath = './coll'

    # Import all documents from the coll directory 
    importCollection(collectionPath)

if __name__ == "__main__":
    main()