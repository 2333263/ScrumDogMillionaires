import unittest

class TestMethods(unittest.TestCase):
   def __init__(self):
      self.test_add()
   def test_add(self):
      self.assertEqual("test1","test1")

      
Test=TestMethods()
