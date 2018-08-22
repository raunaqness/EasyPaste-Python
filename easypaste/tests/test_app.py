import sys
sys.path.append("..")

import unittest
import app

class TestApp(unittest.TestCase):

	def test_testclass(self):
		_testclass = app.testclass()
		result = _testclass.add(10, 5)
		self.assertEqual(result, 15)

	
if __name__ == "__main__":
	unittest.main()