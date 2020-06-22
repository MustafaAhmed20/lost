from . import TestConfig


class TestUser(TestConfig):
	def test_true(self):
		assert True

	def test_true2(self):
		#self.assertEqual(app.config['TESTING'], True)
		assert True

	def test_true3(self):
		assert True