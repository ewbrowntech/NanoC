import os
'''
file_management.py

@Author - Ethan Brown - ewb0020@auburn.edu

@Version - 29 AUG 22

Manages the input and output of files
'''


# Loads specified file from examples folder. Makes testing easier, as full path not required.
# Arguments:
# - filename (string) - full specified filename with extension
# Returns:
# - filePath (string) - path of specified file
def get_path(filename):
    currentDir = os.getcwd()
    parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    filePath = parentDir + '\examples\\' + filename
    print(filePath)
    return filePath