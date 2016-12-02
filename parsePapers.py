
#!/usr/bin/env python

import csv
from unidecode import unidecode
import prefixScan
import re
import authorParserHelper as aph

import pro
dataDirectory = "dataRev2/"
answerFileName = "answer.txt"

# Prefixscan variables
minsupport = 2
highThreshold = .85
lowThreshold = .4


from progress.bar import Bar


'''
Everything we've got.
Parses all the Paper & Author data in the dataDirectory, and outputs duplicate authors to an answer file.
Will print duplicates as they are found
'''
def authorList():
    # Step 1
    # find duplicate papers by
    # mapping paper title to ids: {"paper title": [id1, id2], "other title": [id3]}
    print("indexing data files...")
    paperDict = papers()

    authorDict = authors()
    availableAuthorIds = authorDict.keys()

    pidToAuthorIds = paperAuthors()
    availablePaperIds = pidToAuthorIds.keys()

    theList = authorsToAuthors(availableAuthorIds) # actually a dict

    paperCount = 0
    print("comparing authors...")

    frameSize = len(paperDict)

    bar = Bar('Processing...', max=frameSize)

    for paper, pidList in paperDict.items():
        # opt: if we only compare names between duplicate papers, we can skip papers without duplicates
        if len(pidList) < 2:
            continue

        # Step 2
        # build list of lists of authors for a paper, corresponding to authors of each of its duplicates
        authorIdGroups = []

        for pid in pidList:
            if pid in availablePaperIds:
                authorGroup = []
                authorIds = pidToAuthorIds[pid]
                for authorId in authorIds:
                    if authorId in availableAuthorIds:
                        authorGroup.append(authorDict[authorId])
                authorIdGroups.append(authorGroup)

        # authorIdGroups looks like:
        '''
        [[{'name': 'Donald J. Wuebbles', 'affiliation': 'University of Illinois Urbana Champaign'}], []]
        [[], []]
        [[{'name': 'Edward A. Panacek', 'affiliation': 'University of California Davis'}], []]
        [[{'name': 'Claudio Nicolini', 'affiliation': ''}], []]
        [[{'affiliation': 'University of Pittsburgh', 'name': 'Kirk R. Pruhs'}], [{'affiliation': '', 'name': 'Peter P. Groumpos'}]]
        '''


        # Step 2.5
        '''
            Build the list of names to mine prefix patterns from, remove duplicate names, 
            add any duplicate ids to theList, get unique patterns
        '''

        prefixGroupWithID = []
        prefixGroupNoID = []
        sanitizedNames = []


        for group in authorIdGroups:
            for author in group:
                sanitizedName = re.sub(r"[^a-zA-Z0-9]", '', author['name'])
                sanitizedNames.append((sanitizedName, author['id']))


            # There may be problems with checking equality of names when they have
            # all the spaces removed. This might be very occasional, but still.
            # e.g. Bobb G Reen or Bobb Green (meh)
            
        sanitizedNames.sort()
        curId = -1
        curName = ""

        for (authorName, authorId) in sanitizedNames:
            if curId == -1:
                curId = authorId
                curName = authorName
                prefixGroupWithID.append((authorName, authorId))
                prefixGroupNoID.append(authorName)
                continue

            if curName == authorName:
                if curId != authorId:
                    #print("found exact duplicate authors:")
                    #print("  " + curName + "(" + curId + ")")
                    #print("  " + authorName + "(" + authorId + ")")
                    theList[curId].add(authorId)
                    theList[authorId].add(curId)
            else:
                prefixGroupWithID.append((authorName, authorId))
                prefixGroupNoID.append(authorName)
                curId = authorId
                curName = authorName


        # If the list is a single element or less, then no need to compare.
        if len(prefixGroupWithID) <= 1:
            continue

        prefixGroupNoID.sort(key=len)
        #print(prefixGroupNoID)

        # Step 3
        # compare authors (maybe mine patterns in all names before compare loop)
        '''
            Gets all patterns using prefixscan algorithm. Then goes through and checks to see
            if each pattern meets the high threshold for any item, and if it does, it goes through
            the list again and tries the pattern against names with the lower threshold. If the list
            of names which satisfied the threshold is longer than 2, it adds them to theList

            #TODO   Fix behavior where it will keep matching prefixes even if names have already been
                    matched.
        '''


        patterns = prefixScan.mine(prefixGroupNoID, minsupport)
        patterns.sort(key=lambda x: len(x[0]))

        minPatternSize = highThreshold*len(prefixGroupNoID[0])
        newPrefixGroup = set()
        curPatternLength = minPatternSize

        for (pattern, support) in patterns:
            patternLength = len(pattern)
            if (patternLength >= minPatternSize):
                if (patternLength != curPatternLength):
                    curPatternLength = patternLength
                    prefixGroupNoID = list(newPrefixGroup)

                matchIds = []
                high = False
                for (authorName, authorId) in prefixGroupWithID:
                    if minPatternWithThreshold(pattern, highThreshold, authorName):
                        high = True

                if high:
                    for (authorName, authorId) in prefixGroupWithID:
                        if minPatternWithThreshold(pattern, lowThreshold, authorName):
                            matchIds.append((authorId, authorName))
                            newPrefixGroup.add((authorId, authorName))

                if len(matchIds) >= 2:
                    print("found duplicate authors by prefixScan:")
                    idset = set([x[0] for x in matchIds])
                    for (aid, name) in matchIds:
                        theList[aid] |= idset
                        print("  " + name + "(" + aid + ")")

                if len(matchIds) >= len(prefixGroupNoID):
                    break


        '''
        for pIndex in range(0, len(authorIdGroups)):
            otherAuthors = authorIdGroups[0:pIndex] + authorIdGroups[pIndex+1:len(pidList)]
            for authorA in authorIdGroups[pIndex]:
                aId = authorA['id']

                for authorGroup in otherAuthors:
                    for authorB in authorGroup:
                        bId = authorB['id']
                        if aId == bId:
                            continue

                        # TO DO: compare authors (maybe check if they both follow a pattern)
                        # if authorsLookLikeDuplicates(authorA, authorB):
                        if authorA['name'][0:6].lower() == authorB['name'][0:6].lower():

                            if aId not in theList[bId]:
                                print("found duplicate authors:")
                                print("  " + authorA['name'] + "(" + authorA['id'] + ")")
                                print("  " + authorB['name'] + "(" + authorB['id'] + ")")
                                # mark as duplicates
                                theList[aId].add(bId)
                                theList[bId].add(aId)
        '''
        bar.next()


    bar.finish()
        


    # Step 4
    # union lists of duplicates
    theList = unifyAuthorDuplicates(theList)

    # Step 5
    # Output results
    print("writing results to " + answerFileName + "...")
    answer = open(answerFileName, 'w')
    answer.truncate()
    answer.write("AuthorId,DuplicateAuthorIds\n")
    intList = [int(x) for x in theList.keys()]
    for aId in sorted(intList):
        aId = str(aId)
        idList = theList[aId]

        answer.write(aId + ",")
        first = True
        for bId in idList:
            if first:
                first = False
            else:
                answer.write(" ")
            # " bId"
            answer.write(bId)
        answer.write("\n")
    answer.close()

    print("finished.")


''' 
    This function will return the dictionary which contains only papers that are
    duplicates of others, with paper name as a key -> values are the duplicate paperIds
'''
def papers():
    paperDict = dict()

    with open(dataDirectory + "Paper.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            # TODO: Ensure that the cleanUpTitle is thorough
            title = aph.cleanUpTitle(row['Title'])
            paperId = row['Id']

            if title is "":
                continue   
            if title in paperDict:
                paperDict[title].append(paperId)
            else:
                paperDict[title] = [paperId]

    # paperDict looks like {"paper title": [id1, id2], "other title": [id3]}
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
            if paperId in pidToAuthorIds:
                pidToAuthorIds[paperId].append(authorId)
            else:
                pidToAuthorIds[paperId] = [authorId]

    return pidToAuthorIds


'''
    Returns all authors: {authorId: {"name": "...", "id": "1"}}
'''
def authors():
    aidToAuthor = dict()

    with open(dataDirectory + "Author.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            authorName = aph.cleanUpName(row['Name'])
            authorAffiliation = row['Affiliation']

            # TO DO: clean up author affiliation
            # authorAffiliation = cleanedAffiliation(authorAffiliation)

            authorId = row['Id']
            author = {"name": authorName, "affiliation": authorAffiliation, "id": authorId}
            aidToAuthor[authorId] = author

    ## TO DO: should we include unknown authors from PaperAuthor?
    ## brett says no
    # with open(dataDirectory + "PaperAuthor.csv") as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         authorId = row['AuthorId']
    #         if authorId not in aidToAuthor.keys():
    #             author = {"name": row['Name'], "affiliation": "", "id": authorId}
    #             aidToAuthor[authorId] = author

    return aidToAuthor

'''
    Returns new `theList` with all authors marked with themselves as duplicates: {authorId: {"name": "...", "id": "1"}}
'''
def authorsToAuthors(authorIds):
    idsToIds = dict()
    for aId in authorIds:
        a = set()
        a.add(aId)
        idsToIds[aId] = a
    return idsToIds


def minPatternWithThreshold(pattern, threshold, name):

    pattern = [x[0] for x in pattern]
    namelen = len(name)
    patternlen = len(pattern)

    if namelen == 0:
        return False

    # Pattern must be within threshold
    percentage = patternlen/namelen
    if percentage < threshold or percentage > 1:
        return False

    curChar = 0
    for i in range(0, len(name)):
        if curChar >= patternlen:
            return True

        if name[i] == pattern[curChar]:
            curChar += 1

    if curChar >= patternlen:
        return True

    return False

''' 
    This function will go through each author's duplicate set and take the union of
    the current author's duplicates and each item in the duplicate set's duplicates.
    If there are no changes detected after the process, we are finished. Otherwise,
    we do it again.
'''
def unifyAuthorDuplicates(authorDict):

    change = False
    authors = authorDict.keys()

    for authorId in authors:
        duplicates = authorDict[authorId]
        newDups = duplicates
        for dup in duplicates:
            if authorDict[dup] != newDups:
                newDups = newDups.union(authorDict[dup])
                authorDict[dup] = newDups
                change = True

        if newDups != duplicates:
            authorDict[authorId] = newDups

    if change is False:
        return authorDict
    else:
        return unifyAuthorDuplicates(authorDict)


authorList()
