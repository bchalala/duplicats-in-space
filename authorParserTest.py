import unittest
import authorParserHelper as aph

### To perform unit test, just run $python filename.py

class AuthorTest(unittest.TestCase):

	def testAccentHappyPath(self):
		testString = 'éô'
		expectedString = 'eo'
		self.assertTrue(expectedString == aph.removeAccents(testString))
		self.assertTrue(expectedString == aph.removeAccents2(testString))

	def testRemove(self):
		testString1 = 'a~bla-|_  a,b-'
		expectedString1 = 'abla a b'
		print(aph.removeNonalphanum(testString1))
		self.assertTrue(expectedString1 == aph.removeNonalphanum(testString1))

	def testSpecialCase(self):
		testString1 = 'John Smith iii'
		testString2 = 'John Smith ii'
		testString3 = 'John Smith iv'
		expectedString = 'John Smith'
		self.assertTrue(expectedString == aph.SpecialCharCases(testString1))
		self.assertTrue(expectedString == aph.SpecialCharCases(testString2))
		self.assertTrue(expectedString == aph.SpecialCharCases(testString3))

	def generateNamesWithInitials(self):
		testString = 'John Smith'
		expectedString = 'J Smith'
		self.assertTrue(expectedString == aph.SpecialCharCases(testString))


if __name__ == '__main__':
    unittest.main()