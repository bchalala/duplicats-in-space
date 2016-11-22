
#!/usr/bin/env python

import csv

def matchingPaperIds():
    paperDict = dict()
    duplicates = set()

    with open("dataRev2/Paper.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['Title']
            paperId = row['Id']

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].append(paperId)
                duplicates.add(title)
            else:
                paperDict[title] = [paperId]

    for entry in duplicates:
        print(entry)
        print(paperDict[entry])
    
    return (paperDict, duplicates)

matchingPaperIds()
