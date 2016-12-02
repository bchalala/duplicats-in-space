import pandas as pd

import titleParserHelper as tph
import affParserHelper as affp
import authorParserHelper as aph

authorFilePath = 'sampleData/Author.csv'
paperAuthorFilePath = 'sampleData/PaperAuthor.csv'
paperFilePath = 'sampleData/Paper.csv'

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
while index < frameSize:

	nameString = authorDataframe['Name'][index]
	nameString = aph.removeAccents2(nameString)
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

##########################################
## This part we clean up the paper file  #
##########################################

print("Now processing paper.csv")
index = 0
frameSize = len(paperDataframe['Title'])
while index < frameSize:

	nameString = paperDataframe['Title'][index]
	nameString = aph.removeAccents2(nameString)
	## nameString = aph.removeNonalphanum(nameString) should we have this or no?
	nameString = tph.removeQuotations(nameString)


	paperDataframe['Title'][index] = nameString

	index += 1

################################################
## This part we clean up the paperAuthor file  #
################################################
print("Now processing paperAuthor.csv")

paperAuthorDataframe['Nickname'] = 'NaN'
index = 0
frameSize = len(paperAuthorDataframe['Name'])
while index < frameSize:

	nameString = paperAuthorDataframe['Name'][index]
	nameString = aph.removeAccents2(nameString)
	nameString = aph.removeNonalphanum(nameString)
	nameString = aph.SpecialCharCases(nameString)

	nickname = apg.generateNamesWithInitials(nameString)
	paperAuthorDataframe['Nickname'] = nickname

	nameDict = aph.nicknameMapping()

	if nameString in nameDict:
		nameString = nameDict[nameString]

	if aph.checkMistakenNames(nameString):
		index += 1
		continue

	paperAuthorDataframe['Name'][index] = nameString

	index += 1

paperAuthorDataframe['AffAlias'] = 'NaN'
frameSize = len(paperAuthorDataframe['Affiliation'])
while index < frameSize:

	affString = paperAuthorDataframe['Affiliation'][index]

	affString = aph.removeAccents2(affString)
	affString = affp.removeHTMLTags(affString)
	affAlias = affp.getParents(affString)

	paperAuthorDataframe['AffAlias'] = affAlias

	index += 1


authorDataframe.to_csv('PrunedAuthor.csv')
paperAuthorDataframe.to_csv('PrunedPaperAuthor.csv')
paperDataframe.to_csv('PrunedPaper.csv')



