
#!/usr/bin/env python

import csv

paperDict = dict()
duplicates = set()

with open("dataRev2/Paper.csv") as csvfile:
    fn = ['id', 'title', 'year', 'conferenceid', 'journalid', 'keywords']
    reader = csv.DictReader(csvfile, fieldnames=fn)
    for row in reader:
        title = row['title']

        if title is "":
            continue
            
        if title in paperDict:
            pids = paperDict[title]
            pids.add(row['id'])
            paperDict[title] = pids
            duplicates.add(title)
        else:
            paperDict[title] = set(row['id'])

for elem in duplicates:
    print(elem)
    print(paperDict[elem])
