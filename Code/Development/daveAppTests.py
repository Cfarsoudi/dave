import unittest
import daveApp
from daveApp import DaveApp
from daveApp import HomePage
from daveApp import CharacterPage


class AppTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = DaveApp()
		self.app.frames = self.app.constructFrames(self.app.container,
										  HomePage, CharacterPage)

	def tearDown(self):
		pass

	def testConstructFrames(self):
		self.assertIsInstance(self.app.frames[HomePage], HomePage)

	# def testShowFrame(self):
	# 	self.app.showframe(HomePage)
	# 	self.assertIsNone(self.app.frames[HomePage])

	def testOutputModes(self):
		pass


appTestSuite = unittest.TestSuite()
appTestSuite.addTest(AppTestCase('testConstructFrames'))
# appTestSuite.addTest(AppTestCase('testShowFrame'))

# -------- Run the Tests ---------
runner = unittest.TextTestRunner()
runner.run(appTestSuite)

