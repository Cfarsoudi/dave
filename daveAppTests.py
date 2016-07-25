import unittest
from daveApp import DaveApp, HomePage, CharacterPage

class DaveAppTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = DaveApp()

	def tearDown(self):
		pass

# 	def testConstructFrames(self):
# 		assert isinstance(self.app.frames[Homepage], Homepage) == True

# DaveAppTestSuite = unittest.TestSuite()
# DaveAppTestSuite.addTest(DaveAppTestCase('testFrameGeneration'))
# #genreTestSuite.addTest(DaveAppTestCase('testGenreNumber'))

# runner = unittest.TextTestRunner()

# runner.run(DaveAppTestSuite)