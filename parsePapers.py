
#!/usr/bin/env python

import csv


''' 
    This function will return the dictionary which contains only papers that are
    duplicates of others as a key and values are the duplicate paperIds. The fun
    will also return the names of the duplicate papers, and the set of duplicateIds

    Ideally the duplicateId set will be used in the getNamesOfPapers function
'''
def matchingPaperIds():
    paperDict = dict()
    duplicateNames = set()
    duplicateIds = set()


    with open("dataRev2/Paper.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['Title']
            paperId = row['Id']

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].append(paperId)
                duplicateNames.add(title)
            else:
                paperDict[title] = [paperId]

    duplicateDict = dict()

    for entry in duplicateNames:
        duplicateNames[entry] = paperDict[entry]
        for item in paperDict[entry]:
            duplicateIds.add(int(item))


    
    return (duplicateDict, duplicateNames, duplicateIds)



''' 
    Given a paperIdSet, this function will attempt to get all of the authors
    for the papers in the set of paperIdSet
'''

def getNamesOfPapers(paperIdSet):
    pidToAuthor = dict()

    with open("dataRev2/PaperAuthor.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            paperId = row['PaperId']
            authorId = row['AuthorId']
            authorName = row['Name']
            if int(paperId) in paperIdSet:
                if paperId in pidToAuthor:
                    pidToAuthor[paperId].append((authorId, authorName))
                else:
                    pidToAuthor[paperId] = [(authorId, authorName)]

    return pidToAuthor


(dupPaperDict, dupNames, dupIds) = matchingPaperIds()
getNamesOfPapers(dupIds)
