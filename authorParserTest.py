import unittest
import authorParserHelper as aph

class AccentTest(unittest.TestCase):

	def testHappyPath(self):
		testString = 'éô'
		expectedString = 'eo'
		self.assertTrue(expectedString == aph.removeAccents(testString))
		self.assertTrue(expectedString == aph.removeAccents2(testString))

if __name__ == '__main__':
    unittest.main()