import unittest
import titleParserHelper as tph


class TitleTest(unittest.TestCase):

	def testQuotationHappyPath(self):
		testString = '"Lorem ipsum'
		expectedString = 'Lorem ipsum'
		self.assertTrue(expectedString == tph.removeQuotations(testString))

	def testCheckWordcount(self):
		testString1 = 'Lorem ipsum'
		testString2 = 'Lorem ipsum dolor sit'
		self.assertTrue(tph.checkWhenLessThan3(testString1))
		self.assertFalse(tph.checkWhenLessThan3(testString2))

if __name__ == '__main__':
    unittest.main()