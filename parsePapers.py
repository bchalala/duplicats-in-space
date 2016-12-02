
#!/usr/bin/env python

import csv
from unidecode import unidecode
import prefixScan
import re

dataDirectory = "sampleData/"

def authorList():
    # mapping of paper title to ids: {"paper title": [id1, id2], "other title": [id3]}
    paperDict = papers()

    authorDict = authors()
    availableAuthorIds = authorDict.keys()

    pidToAuthorIds = paperAuthors()
    availablePaperIds = pidToAuthorIds.keys()

    paperCount = 0
    for paper, pidList in paperDict.items():
        # build list of lists of ids, corresponding to duplicate papers
        # [[id1, id2, id3], [id6]. [id5, id4]]
        authorIdGroups = []
        for pid in pidList:
            if pid in availablePaperIds:
                authorGroup = []
                authorIds = pidToAuthorIds[pid]
                for authorId in authorIds:
                    # print(authorIds)
                    if authorId in availableAuthorIds:
                        authorGroup.append(authorDict[authorId])
                authorIdGroups.append(authorGroup)

        if paperCount < 10:
            print(authorIdGroups)
            paperCount += 1



    # pidToAuthor = getPaperAuthorsFromSet(dupIds)

    # # authorDict = authorsAsDict()
    # # duplicateAuthors = set()

    # print("--- Duplicate Papers ---")
    # for key, value in dupPaperDict.items():
    #     print(key + ": " + ', '.join(value))

    # print("--- Paper Authors ---")
    # minsup = 3
    # minwidth = 6
    # for paperID, authorList in pidToAuthor.items():
    #     authorNames = []
    #     sanitizedNames = []
    #     for (authorId, authorName) in authorList:
    #         authorNames.append(authorName)

    #         # remove unnusual characters before pattern scan
    #         sanitizedName = re.sub(r"[^a-zA-Z0-9]", '', authorName)
    #         sanitizedNames.append(sanitizedName)

    #     print(authorNames)

    #     patterns = prefixScan.mine(sanitizedNames, minsup)
    #     # ignore short patterns and turn lists into strings for readability
    #     readablePatterns = []
    #     for (pattern, support) in patterns:
    #         if (len(pattern) >= minwidth):
    #             readablePatterns.append(''.join(pattern))
    #     print("- patterns: " + str(readablePatterns))


''' 
    This function will return the dictionary which contains only papers that are
    duplicates of others as a key and values are the duplicate paperIds. The fun
    will also return the names of the duplicate papers, and the set of duplicateIds

    Ideally the duplicateId set will be used in the getNamesOfPapers function
'''
def papers():
    paperDict = dict()
    # duplicateNames = set()
    # duplicateIds = set()


    with open(dataDirectory + "Paper.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['Title']
            paperId = row['Id']

            # TO DO: clean up paper title so duplicates are indexed the same

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].append(paperId)
                # duplicateNames.add(title)
            else:
                paperDict[title] = [paperId]

    # duplicateDict = dict()

    # for entry in duplicateNames:
    #     duplicateDict[entry] = paperDict[entry]
    #     for item in paperDict[entry]:
    #         duplicateIds.add(int(item))


    # paperDict: {"paper title": [id1, id2], "other title": [id3]}
    return paperDict



''' 
    Given a paperIdSet, this function will attempt to get all of the authors
    for the papers in the set of paperIdSet. Any strings that are not ascii
    will be automatically converted to ascii. Additionally, they will be made
    lowercase. 
'''

def paperAuthors():
    pidToAuthorIds = dict()

    with open(dataDirectory + "PaperAuthor.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            paperId = row['PaperId']
            authorId = row['AuthorId']
            # ignore other fields?
            # authorName = unidecode(row['Name'])
            # authorName = authorName.lower()
            if paperId in pidToAuthorIds:
                pidToAuthorIds[paperId].append(authorId)
            else:
                pidToAuthorIds[paperId] = [authorId]

    return pidToAuthorIds


'''
    Returns all authors with their id as their duplicate
'''
def authors():
    aidToAuthor = dict()

    with open(dataDirectory + "Author.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            authorName = row['Name']
            authorAffiliation = row['Affiliation']

            # TO DO: clean up author name
            # TO DO: clean up author affiliation

            author = {"name": authorName, "affiliation": authorAffiliation}
            aidToAuthor[row['Id']] = author

    return aidToAuthor


''' 
    This function will go through each author's duplicate set and take the union of
    the current author's duplicates and each item in the duplicate set's duplicates.
    If there are no changes detected after the process, we are finished. Otherwise,
    we do it again.
'''

def unifyAuthorDuplicates(authorDict):

    change = False
    authors = authorDict.keys()

    for author in authors:
        duplicates = authorDict[author]
        newDups = duplicates
        for dup in duplicates:
            if authorDict[dup] != newDups:
                newDups = newDups.union(authorDict[dup])
                authorDict[dup] = newDups
                change = True

        if newDups != duplicates:
            authorDict[author] = newDups

    if change is False:
        return authorDict
    else:
        return unifyAuthorDuplicates(authorDict)

'''
testdict = {1: set([1]), 2: set([1, 2]), 3: set([3, 1])}
unifyAuthorDuplicates(testdict)
for item in testdict.keys():
    print(item)
    print(testdict[item])


''' 

authorList()
