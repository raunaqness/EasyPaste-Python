import sys
sys.path.append("..")

import unittest
from easypaste import testclass

class TestApp(unittest.TestCase):

	def test_testclass(self):
		_testclass = testclass()
		result = _testclass.add(10, 5)
		self.assertEqual(result, 15)

	
if __name__ == "__main__":
	unittest.main()