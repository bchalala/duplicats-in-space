import pandas as pd

import titleParserHelper as tph
import affParserHelper as affp
import authorParserHelper as aph

## For time optimization and progress bar
import time
from progress.bar import Bar

start_time = time.time()


filePath1 = 'sampleData/'
filePath2 = 'dataRev2/'
authorFilePath = filePath1 + 'Author.csv'
paperAuthorFilePath = filePath1 + 'PaperAuthor.csv'
paperFilePath = filePath1 + 'Paper.csv'

authorDataframe = pd.read_csv(authorFilePath)
paperAuthorDataframe = pd.read_csv(paperAuthorFilePath)
paperDataframe = pd.read_csv(paperFilePath)

##########################################
## This part we clean up the author file #
##########################################
index = 0

## Adding new columns here

print('Now processing author.csv...')
authorDataframe['Nickname'] = 'NaN'
frameSize = len(authorDataframe['Name'])

bar = Bar('Processing', max=frameSize)
while index < frameSize:

	nameString = authorDataframe['Name'][index]
	nameString = aph.removeAccents(nameString)
	nameString = aph.removeNonalphanum(nameString)
	nameString = aph.SpecialCharCases(nameString)

	nickname = aph.generateNamesWithInitials(nameString)
	authorDataframe['Nickname'] = nickname

	nameDict = aph.nicknameMapping()

	if nameString in nameDict:
		nameString = nameDict[nameString]

	if aph.checkMistakenNames(nameString):
		index += 1
		continue

	authorDataframe['Name'][index] = nameString

	index += 1
	bar.next()

bar.finish()

##########################################
## This part we clean up the paper file  #
##########################################

print("Now processing paper.csv")
print("Time used %s seconds " % (time.time() - start_time))

index = 0
frameSize = len(paperDataframe['Title'])
bar = Bar('Processing', max=frameSize)

while index < frameSize:

	nameString = paperDataframe['Title'][index]
	nameString = aph.removeAccents(nameString)
	## nameString = aph.removeNonalphanum(nameString) should we have this or no?
	nameString = tph.removeQuotations(nameString)


	paperDataframe['Title'][index] = nameString

	index += 1
	bar.next()

bar.finish()

################################################
## This part we clean up the paperAuthor file  #
################################################
print("Now processing paperAuthor.csv")
print("Time used %s seconds " % (time.time() - start_time))

paperAuthorDataframe['Nickname'] = 'NaN'
index = 0
frameSize = len(paperAuthorDataframe['Name'])

bar = Bar('Processing', max=frameSize)
while index < frameSize:

	nameString = paperAuthorDataframe['Name'][index]
	nameString = aph.removeAccents(nameString)
	nameString = aph.removeNonalphanum(nameString)
	nameString = aph.SpecialCharCases(nameString)

	nickname = aph.generateNamesWithInitials(nameString)
	paperAuthorDataframe['Nickname'] = nickname

	nameDict = aph.nicknameMapping()

	if nameString in nameDict:
		nameString = nameDict[nameString]

	if aph.checkMistakenNames(nameString):
		index += 1
		continue

	paperAuthorDataframe['Name'][index] = nameString

	index += 1
	bar.next()
bar.finish()


paperAuthorDataframe['AffAlias'] = 'NaN'
frameSize = len(paperAuthorDataframe['Affiliation'])

bar = Bar('Processing', max=frameSize)
while index < frameSize:

	affString = paperAuthorDataframe['Affiliation'][index]

	affString = aph.removeAccents(affString)
	affString = affp.removeHTMLTags(affString)
	affAlias = affp.getParents(affString)

	paperAuthorDataframe['AffAlias'] = affAlias

	index += 1
	bar.next()

bar.finish()

print("Time used %s seconds " % (time.time() - start_time))

authorDataframe.to_csv('PrunedAuthor.csv')
paperAuthorDataframe.to_csv('PrunedPaperAuthor.csv')
paperDataframe.to_csv('PrunedPaper.csv')



