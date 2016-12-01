import unittest
import affParserHelper as affp

### Haven't tested this yet.

class AffTest(unittest.TestCase):

	def testGetParentsHappyCase(self):
		testString1 = 'department of physics; stanford university'
		testString2 = 'department of physics |stanford university'
		testString3 = ' stanford university / department of physics '
		testString4 = 'department of physics |georgia institute of technology '
		testString5 = 'department of physics | harvard college '
		testString6 = 'department of physics / university of california, los angeles '
		expectedString1 = 'stanford university'
		expectedString2 = 'georgia institute of technology'
		expectedString3 = 'harvard college'
		expectedString4 = 'university of california, los angeles'
		self.assertTrue(expectedString1 == affp.getParents(testString1))
		self.assertTrue(expectedString1 == affp.getParents(testString2))
		self.assertTrue(expectedString1 == affp.getParents(testString3))
		self.assertTrue(expectedString2 == affp.getParents(testString4))
		self.assertTrue(expectedString3 == affp.getParents(testString5))
		self.assertTrue(expectedString4 == affp.getParents(testString6))


	def testInstitutionMapper(self):
		testString = 'brown univ'
		expectedString = 'brown university'
		self.assertTrue(expectedString == affp.institutionAliasMapper(testString))

	def testRemoveTags(self):
		testString = '<sup>stanford university</sup>'
		expectedString = ' stanford university '
		self.assertTrue(expectedString == affp.removeHTMLTags(testString))


if __name__ == '__main__':
    unittest.main()