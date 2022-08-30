import unittest
import sys
sys.path.append('..')
from src.lexer import lexer
'''
lexer_test.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 AUG 22

Test compiler functions
'''

class TestLexer(unittest.TestCase):
    # Nominal input
    def test_nominal_001_basic_expression(self):
        fileContents = "int i = 1"
        expectedResult = [{'content': 'int', 'position': 0, 'type': 'keyword'},
                          {'content': 'i', 'position': 4, 'type': 'id'},
                          {'content': '=', 'position': 6, 'type': 'operator'},
                          {'content': '1', 'position': 8, 'type': 'val'}]
        actualResult = lexer(fileContents)
        self.assertEqual(expectedResult, actualResult)
