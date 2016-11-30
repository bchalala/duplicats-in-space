
def getParents(affString):
	""" This function gets the univeristy name from a possible combination of department name 
	and school/org name. Return null if the keyword doesn't match"""

	orgArr1 = affString.split(';')
	orgArr2 = affString.split('|')
	orgArr3 = affString.split('/')

	orgArray.append(getParentsHelper(orgArr1))
	orgArray.append(getParentsHelper(orgArr2))
	orgArray.append(getParentsHelper(orgArr3))

	# Now we take the string with smallest length because that's the highest order
	# Not necessarily sure if this is necessary

	desiredOrg = min(orgArray, key=len).strip() # in case there's spaces before

	return desiredOrg


def checkKeywords(affString):
	""" This function checks if the word contains keywords """

	if 'university of ' in affString:
		return True

	if ' university' in affString:
		return True

	if ' college' in affString:
		return True

	if ' institute' in affString:
		return True

	## A special case when an university is referred without the keyword: ETH Zurich
	if 'eth ' in affString:
		return True

	return False

def getParentsHelper(orgArr):
	""" A helper function for the getParents function """

	for org in orgArr:
		if checkKeywords(org):
			return org

def institutionAliasMapper(affString):
	""" A function that returns the name of the institution after converting the nickname.
		Currently developing new possible aliases"""

	D = {}
	D['univ'] = 'university'
	D['univ.'] = 'university'

	newAffString = ''

	orgArr = affString.split()
	for word in orgArr:
		if word in D:
			word = D[word]

		newAffString += word

	return newAffString

def removeHTMLTags(affString):
	""" Removing the HTML tags from the string. Notice this replaces the tag with white spaces. 
		So we have to run this before the squashing white spaces functionalities """

	affString = affString.replace('<sup>', ' ')
	affString = affString.replace('</sup>', ' ')

	return affString


def getUniversityName(affString):
	""" This function get the university name given an affiliation string. 
	For example: Stanford University --> Stanford
				 Don't think this applies to schools like University of California, XX
		Haven't found a case where this is useful yet...
	"""

