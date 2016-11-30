import unittest
import authorParserHelper as aph

### To perform unit test, just run $python filename.py

class AuthorTest(unittest.TestCase):

	def testAccentHappyPath(self):
		testString = 'éô'
		expectedString = 'eo'
		self.assertTrue(expectedString == aph.removeAccents(testString))
		self.assertTrue(expectedString == aph.removeAccents2(testString))

	def testRemoveHappyPath(self):
		testString1 = 'a~bla-|_  a,b-'
		expectedString1 = 'abla a b'
		self.assertTrue(expectedString1 == aph.removeNonalphanum(testString1))

	def testSpecialCaseHappyPath(self):
		testString1 = 'John Smith iii'
		testString2 = 'John Smith ii'
		testString3 = 'John Smith iv'
		expectedString = 'John Smith'
		self.assertTrue(expectedString == aph.SpecialCharCases(testString1))
		self.assertTrue(expectedString == aph.SpecialCharCases(testString2))
		self.assertTrue(expectedString == aph.SpecialCharCases(testString3))

	def testCheckMistakenNames(self):
		self.assertTrue(aph.checkMistakenNames("he and me"))
		self.assertTrue(aph.checkMistakenNames("for the glory of the south"))
		self.assertTrue(aph.checkMistakenNames("trick or treat"))
		self.assertTrue(aph.checkMistakenNames("a bottle of wine"))
		self.assertFalse(aph.checkMistakenNames("arab"))
		self.assertTrue(aph.checkMistakenNames("reach to the sky"))
		self.assertTrue(aph.checkMistakenNames("turn on the TV"))
		self.assertTrue(aph.checkMistakenNames("I'm in here"))
		self.assertTrue(aph.checkMistakenNames("something of value"))


	def generateNamesWithInitialsHappyPath(self):
		testString = 'John Smith'
		expectedString = 'J Smith'
		self.assertTrue(expectedString == aph.SpecialCharCases(testString))


if __name__ == '__main__':
    unittest.main()