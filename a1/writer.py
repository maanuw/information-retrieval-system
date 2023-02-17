from prettytable import PrettyTable

# Initialize pettytable.
write = PrettyTable()

def generateResultsTable(dict):
    write.field_names = ["topic_id", "Q0", "docno", "rank", "score", "tag"]
    write.align='l'
    write.border=False
    print(type(dict))
    sortedResult = []
    #docMetric = 
    for query in  dict:
        queryDocs = dict[query]
        query = []
        for doc in queryDocs:
            entry = (queryDocs[doc], doc)
            query.append(entry)
        
        query = sorted(query)
        reverse = []
        i = len(query)-1
        while i >= 0:
            reverse.append(query[i])
            i -=1

        sortedResult.append(query)
    print("Created tuples list!")

    for i in range(len(sortedResult)):
        for j in range(len(sortedResult[i])):
            write.add_row([i, "Q0", sortedResult[i][j][1], j, sortedResult[i][j][0], "run_name"])
    print("writing file ...")
            
    with open('Results.txt', 'w') as w:
        w.write(str(write))
    
    print("Done!")