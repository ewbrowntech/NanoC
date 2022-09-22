import unittest
import sys
sys.path.append('..')
from src.file_management import load_file
'''
file_management_test.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 AUG 22

Test file management functions
'''

class TestLoadFile(unittest.TestCase):
    # Nominal input
    def test_nominal_001_fileExists_returnString(self):
        expectedResult = 'abcdef'
        actualResult = load_file('lexer\singleString.c')
        self.assertEqual(expectedResult, actualResult)

    def test_nominal_002_multLines_returnString(self):
        expectedResult = 'a\na\na\na\na'
        actualResult = load_file('lexer\multLines.c')
        self.assertEqual(expectedResult, actualResult)

    # Abnormal input
    def test_abnormal_001_fileNA_throwError(self):
        expectedResult = 'Error: File not found'
        actualResult = load_file('lexer\doesNotExist.c')
        self.assertEqual(expectedResult, actualResult)