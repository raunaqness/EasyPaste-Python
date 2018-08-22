from inspect import getsourcefile
import os.path as path, sys

current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

import unittest
from easypaste import testclass

class TestApp(unittest.TestCase):

	def test_testclass(self):
		_testclass = testclass()
		result = _testclass.add(10, 5)
		self.assertEqual(result, 15)

	
if __name__ == "__main__":
	unittest.main()