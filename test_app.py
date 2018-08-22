import unittest

import app

class TestApp(unittest.TestCase):

	def test_add(self):
		result = app.add(10, 5)
		self.assertEqual(result, 15)