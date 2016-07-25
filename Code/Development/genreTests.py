import unittest
from daveApp import Genre, GenreList

class GenreTestCase(unittest.TestCase):
	
	def setUp(self):
		self.genre = Genre('Name', 5)

	def tearDown(self):
		#self.genre.dispose()
		self.genre = None

	def testGenreName(self):
		assert self.genre.name == 'Name'

	def testGenreNumber(self):
		assert self.genre.number == 5

class GenreListTestCase(unittest.TestCase):

	def setUp(self):
		self.name = ['one', 'two', 'three']
		self.genre = GenreList(self.name[0], self.name[1], self.name[2])

	def tearDown(self):
		self.genre = None

	def testGenreListNamesAndNumbers(self):
		for index, Genre in enumerate(self.genre.list):
			assert Genre.name == self.name[index]
			assert Genre.number == index

	

# def suite():
# 	suite = unittest.TestSuite()
# 	suite.addTest(GenreTestCase('testGenreList'))
# 	return suite

# test1 = GenreTestCase('testGenreName')
# test2 = GenreTestCase('testGenreNumber')

# -------- Set up the Test Suite -------

genreTestSuite = unittest.TestSuite()
genreTestSuite.addTest(GenreTestCase('testGenreName'))
genreTestSuite.addTest(GenreTestCase('testGenreNumber'))

genreListTestSuite = unittest.TestSuite()
genreListTestSuite.addTest(GenreListTestCase('testGenreListNamesAndNumbers'))

alltests = unittest.TestSuite((genreTestSuite, genreListTestSuite))

# -------- Run the Tests ---------

runner = unittest.TextTestRunner()

runner.run(alltests)

# if __name__ == '__main__':
# 	unittest.main()
# 	