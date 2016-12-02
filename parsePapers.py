
#!/usr/bin/env python

import csv
from unidecode import unidecode
import prefixScan
import re
import authorParserHelper as aph

dataDirectory = "dataRev2/"

''' 
    This function will return the dictionary which contains duplicate paper titles
    as a key and values are the duplicate paperIds. The function
    will also return the names of the duplicate papers, and the set of duplicateIds

    Ideally the duplicateId set will be used in the getNamesOfPapers function
'''
def matchingPaperIds():
    paperDict = dict()
    duplicateNames = set()
    duplicateIds = set()


    with open(dataDirectory + "Paper.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['Title']
            paperId = row['Id']

            title = aph.removeAccents(title)
            title = aph.removeNonalphanum(title)

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].append(paperId)
                duplicateNames.add(title)
            else:
                paperDict[title] = [paperId]

    duplicateDict = dict()

    for entry in duplicateNames:
        duplicateDict[entry] = paperDict[entry]
        for item in paperDict[entry]:
            duplicateIds.add(int(item))


    
    return (duplicateDict, duplicateNames, duplicateIds)



''' 
    Given a paperIdSet, this function will attempt to get all of the authors
    for the papers in the set of paperIdSet. Authors must be in the set of all
    authors. Author names are cleaned up using authorParserHelper.
'''

def getPaperAuthorsFromSet(paperIdSet, authorDict):
    pidToAuthor = dict()

    with open(dataDirectory + "PaperAuthor.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            paperId = row['PaperId']
            authorId = row['AuthorId']
            authorName = aph.cleanUpName(row['Name'])
            if (int(paperId) in paperIdSet) and (int(authorId) in authorDict):
                if paperId in pidToAuthor:
                    pidToAuthor[paperId].append((authorId, authorName))
                else:
                    pidToAuthor[paperId] = [(authorId, authorName)]

    return pidToAuthor

'''
    Returns all authors with their id as their duplicate
'''
def authors():
    authorToAuthorSet = dict()

    with open(dataDirectory + "Author.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            aId = int(row['Id'])
            authorToAuthorSet[aId] = set([int(aId)])

    return authorToAuthorSet


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
authorDict = authors()
(dupPaperDict, dupNames, dupIds) = matchingPaperIds()
pidToAuthor = getPaperAuthorsFromSet(dupIds, authorDict)

duplicateAuthors = set()

print("--- Duplicate Papers ---")
for key, value in dupPaperDict.items():
    print(key + ": " + ', '.join(value))

print("--- Paper Authors ---")
minsup = 2
minwidth = 8

for key, value in dupPaperDict.items():
    authorNames = []
    sanitizedNamesWithId = []
    sanitizedNamesWithoutId = []
    for paperId in value:
        if paperId in pidToAuthor:
            authorNames = authorNames + pidToAuthor[paperId]
            for (authorId, authorName) in authorNames:
                # remove unnusual characters before pattern scan
                sanitizedName = re.sub(r"[^a-zA-Z0-9]", '', authorName)
                sanitizedNamesWithId.append((sanitizedName, authorId))

    # There may be problems with checking equality of names when they have
    # all the spaces removed. This might be very occasional, but still.
    
    sanitizedNamesWithId.sort()
    #print("sanitized with id")
    #print(sanitizedNamesWithId)
    #print("\n")

    curId = -1
    curName = ""
    for (authorName, authorId) in sanitizedNamesWithId:
        if curId == -1:
            curId = authorId
            curName = authorName
            sanitizedNamesWithoutId.append(authorName)
            continue

        if curName == authorName:
            if curId != authorId:
                authorDict[int(curId)].add(int(authorId))
                authorDict[int(authorId)].add(int(curId))
                print("duplicate:")
                print(curId)
                print(authorId)
        else:
            sanitizedNamesWithoutId.append(authorName)
            curId = authorId
            curName = authorName


    #print("sanitized without id")
    #print(sanitizedNamesWithoutId)
    #print("\n")

    if len(sanitizedNamesWithoutId) <= 1:
        continue
    else:
        print(key)
        print("sanitized without id")
        print(sanitizedNamesWithoutId)
        #print("\n")


    # Run prefixScan on names that are not equal to eachother.
    patterns = prefixScan.mine(sanitizedNamesWithoutId, minsup)

    readablePatterns = []
    for (pattern, support) in patterns:
        if (len(pattern) >= minwidth):
            readablePatterns.append(''.join(pattern))
    print("- patterns: " + str(readablePatterns))
















