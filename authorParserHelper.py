import unicodedata # For accents removing
import collections
import re # For checkMistakeNames function

def removeAccents(dataToTranslate):
	"""Two function to remove accents, either one should work.
	This is for testing which one runs faster.	"""
	return unicodedata.normalize('NFD', 
		dataToTranslate).encode('ASCII', 'ignore').decode("utf-8")

def removeAccents2(dataToTranslate):
	"""Two function to remove accents, either one should work.
	This is for testing which one runs faster.	"""
	return ''.join((c for c in 
		unicodedata.normalize('NFD', dataToTranslate) if unicodedata.category(c) != 'Mn'))


def nicknameMapping():
	''' There are better ways to get this data. But I think for the purpose of this program, 
	it's best to just use this customized dictionary'''
	D = {}
	D['ana'] = 'anna'
	D['ann'] = 'anna'
	D['anne'] = 'anna'
	D['annette'] = 'anna'
	D['abigail'] = 'abby'
	D['abbie'] = 'abby'
	D['alexander'] = 'alexander'
	D['curtis'] = 'curt'
	D['alek'] = 'alex'
	D['aleksandar'] = 'alex'
	D['aleksander'] = 'alex'
	D['aleksandra'] = 'alex'
	D['alexandr'] = 'alex'
	D['alexandra'] = 'alex'
	D['alexandre'] = 'alex'
	D['alexandru'] = 'alex'
	D['alexei'] = 'alexis'
	D['alan'] = 'allan'
	D['alen'] = 'allen'
	D['andrew'] = 'andy'
	D['andrei'] = 'andre'
	D['arthur'] = 'arthur'
	D['benjamin'] = 'ben'
	D['bernie'] = 'bernard'
	D['bob'] = 'robert'
	D['bobby'] = 'robert'
	D['boby'] = 'robert'
	D['rob'] = 'robert'
	D['brian'] = 'brian'
	D['bryan'] = 'brian'
	D['chad'] = 'chardwick'
	D['christopher'] = 'chris'
	D['christoph'] = 'chris'
	D['christophe'] = 'chris'
	D['clifford'] = 'cliff'
	D['cornelus'] = 'cornelius'
	D['cornelis'] = 'cornelius'
	D['david'] = 'dave'
	D['daniel'] = 'dan'
	D['danny'] = 'dan'
	D['dennis'] = 'denise'
	D['denis'] = 'denise'
	D['dmitry'] = 'dmitri'
	D['dimitrios'] = 'dmitri'
	D['dimitris'] = 'dmitri'
	D['douglas'] = 'doug'
	D['ed'] = 'edward'
	D['eddy'] = 'eddie'
	D['erik'] = 'eric'
	D['francoise'] = 'francois'
	D['fredrick'] = 'fred'
	D['fredrik'] = 'fred'
	D['frdric'] = 'fred'
	D['frdrik'] = 'fred'
	D['frdrick'] = 'fred'
	D['fredrik'] = 'fred'
	D['frederick'] = 'fred'
	D['frederic'] = 'fred'
	D['gregory'] = 'greg'
	D['gregg'] = 'greg'
	D['gregor'] = 'greg'
	D['gregorio'] = 'greg'
	D['freddy'] = 'fred'
	D['jeffrey'] = 'jeff'
	D['josef'] = 'joseph'
	D['josep'] = 'joseph'
	D['joey'] = 'joe'
	D['jonathon'] = 'johnathon'
	D['joshua'] = 'josh'
	D['kenneth'] = 'ken'
	D['kenny'] = 'ken'
	D['leonard'] = 'leo'
	D['leonid'] = 'leo'
	D['leonel'] = 'leo'
	D['leonardo'] = 'leo'
	D['louis'] = 'lou'
	D['luis'] = 'louise'
	D['luise'] = 'louise'
	D['luiz'] = 'louise'
	D['lukas'] = 'lucas'
	D['lukasz'] = 'lucas'
	D['luc'] = 'luke'
	D['marc'] = 'mark'
	D['matt'] = 'matthew'
	D['marvin'] = 'marv'
	D['max'] = 'maxwell'
	D['michael'] = 'mike'
	D['micheal'] = 'mike'
	D['mitchell'] = 'mitch'
	D['mitchel'] = 'mitch'
	D['mohamed'] = 'mo'
	D['mohammad'] = 'mo'
	D['nathan'] = 'nate'
	D['nathaniel'] = 'nate'
	D['nicolas'] = 'nick'
	D['nicholas'] = 'nick'
	D['nic'] = 'nick'
	D['patrick'] = 'pat'
	D['patrik'] = 'pat'
	D['peter'] = 'pete'
	D['phillip'] = 'phil'
	D['phillipe'] = 'phil'
	D['phillippe'] = 'phil'
	D['philip'] = 'phil'
	D['rafael'] = 'rafi'
	D['rafaele'] = 'rafi'
	D['raphael'] = 'rafi'
	D['raymond'] = 'ray'
	D['rich'] = 'rick'
	D['richard'] = 'rick'
	D['dick'] = 'richard'
	D['robby'] = 'rob'
	D['robert'] = 'rob'
	D['roberto'] = 'rob'
	D['stanley'] = 'stan'
	D['stephen'] = 'steve'
	D['steven'] = 'steve'
	D['samuel'] = 'sam'
	D['sammy'] = 'sam'
	D['terrance'] = 'terry'
	D['terrence'] = 'terry'
	D['terence'] = 'terry'
	D['terri'] = 'terry'
	D['theodore'] = 'ted'
	D['tobias'] = 'tobias'
	D['toby'] = 'tobias'
	D['tobi'] = 'tobias'
	D['thomas'] = 'tom'
	D['tomas'] = 'tom'
	D['timothy'] = 'tim'
	D['vincent'] = 'vince'
	D['vlad'] = 'vladimir'
	D['walter'] = 'walt'
	D['william'] = 'will'
	D['catherine'] = 'cathy'
	D['jennifer'] = 'jen'
	D['jenifer'] = 'jen'
	D['katherine'] = 'kathy'
	D['kathleen'] = 'kathy'
	D['kimberly'] = 'kim'
	D['pamela'] = 'pam'
	D['sara'] = 'sarah'
	D['sophie'] = 'sophia'
	D['susan'] = 'sue'
	D['susana'] = 'susanna'
	D['suzan'] = 'sue'
	D['teresa'] = 'terry'
	D['terese'] = 'terry'
	D['valerie'] = 'val'
	D['valery'] = 'val'
	D['victoria'] = 'vicky'
	D['vickie'] = 'vicky'
	D['vicki'] = 'vicky'

	return D

def checkMistakenNames(nameString):
	if nameString.contains(' or '):
		return True

	if nameString.contains('for '):
		return True

	if nameString.contains(' and '):
		return True
	
	if re.match('^a ', nameString):
		return True

	if nameString.contains(' to '):
		return True

	if nameString.contains(' in '):
		return True

	if nameString.contains(' of '):
		return True	

	return False

def removeNonalphanum(nameString):
	nameString.replace("~", "")
	nameString.replace("`", "")
	nameString.replace("|", "e")
	nameString.replace("_", "") 
	nameString.replace("\\", "")
	nameString.replace(" \(\w+\)", "") #Multiple whitespace characters
	nameString.str.replace(",", " ")
	nameString.replace("'", "")
	nameString.replace("-", "")
	nameString.replace("\. ", " ")
	nameString.replace("\.", " ")
	nameString.replace("\?", " ")

	return nameString

def handleSpecialCases(nameString):
	nameString.replace(" iii", "")
	nameString.replace(" ii$", "")
	nameString.replace(" iv$", "")
	nameString.replace(" mbbs", "")

