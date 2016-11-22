
#!/usr/bin/env python

import csv

def matchingPaperIds():
    paperDict = dict()
    duplicates = set()

    with open("dataRev2/Paper.csv") as csvfile:
        fn = ['id', 'title', 'year', 'conferenceid', 'journalid', 'keywords']
        reader = csv.DictReader(csvfile, fieldnames=fn)
        for row in reader:
            title = row['title']
            paperId = (row['id'], row['conferenceid'], row['journalid'])

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].add(paperId)
                duplicates.add(title)
            else:
                paperDict[title] = set(paperId)

    for entry in duplicates:
        print(entry)
        print(paperDict[entry])
    
    return (paperDict, duplicates)

matchingPaperIds()
