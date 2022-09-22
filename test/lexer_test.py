import unittest
import sys
sys.path.append('..')
from src.lexer import lexer
'''
lexer_test.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 30 AUG 22

Test compiler functions
'''

class TestLexer(unittest.TestCase):
    # Nominal input
    def test_nominal_001_basic_expression(self):
        fileContents = "int i = 1;"
        expectedResult = [{'content': 'int', 'position': 0, 'type': 'keyword'},
                          {'content': 'i', 'position': 4, 'type': 'id'},
                          {'content': '=', 'position': 6, 'type': 'operator'},
                          {'content': '1', 'position': 8, 'type': 'val'},
                          {'content': ';', 'position': 9, 'type': 'declCease'}]
        actualResult = lexer(fileContents)
        self.assertEqual(expectedResult, actualResult)

    # def test_nominal_002_arrayInit(self):
    #     fileContents = "int val[1] = {1}"
    #     expectedResult = [{'content': 'int', 'position': 0, 'type': 'keyword'},
    #                       {'content': 'val', 'position': 4, 'type': 'id'},
    #                       {'content': '[', 'position': 7, 'type': 'arrDeclStart'},
    #                       {'content': '4', 'position': 8, 'type': 'val'},
    #                       {'content': ']', 'position': 9, 'type': 'arrDeclCease'},
    #                       {'content': '=', 'position': 11, 'type': 'operator'},
    #                       {'content': '[', 'position': 13, 'type': 'arrInitStart'},
    #                       {'content': '1', 'position': 14, 'type': 'val'},
    #                       {'content': '[', 'position': 15, 'type': 'arrInitCease'}]
    #     actualResult = lexer(fileContents)
    #     self.assertEqual(expectedResult, actualResult)

    def test_nominal_003_basic_parantheses(self):
        fileContents = "i = 1 * (1 + 1);"
        expectedResult = [{'content': 'i', 'position': 0, 'type': 'id'},
                          {'content': '=', 'position': 2, 'type': 'operator'},
                          {'content': '1', 'position': 4, 'type': 'val'},
                          {'content': '*', 'position': 6, 'type': 'operator'},
                          {'content': '(', 'position': 8, 'type': 'parStart'},
                          {'content': '1', 'position': 9, 'type': 'val'},
                          {'content': '+', 'position': 11, 'type': 'operator'},
                          {'content': '1', 'position': 13, 'type': 'val'},
                          {'content': ')', 'position': 14, 'type': 'parCease'},
                          {'content': ';', 'position': 15, 'type': 'declCease'}]
        actualResult = lexer(fileContents)
        self.assertEqual(expectedResult, actualResult)
