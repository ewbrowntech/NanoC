import os
'''
file_management.py

@Author - Ethan Brown - ewb0020@auburn.edu
@Version - 17 NOV 22

Manages the input and output of files
'''


# Finds specified file in examples folder. Makes testing easier, as full path not required.
# Arguments:
# - filename (string) - full specified filename with extension
# Returns:
# - filePath (string) - path of specified file
def get_path(filename):
    currentDir = os.getcwd()
    parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    filePath = parentDir + '/test/examples/' + filename
    print("\nSource Filepath: " + str(filePath) + "\n")
    return filePath


# Loads specified file from examples folder and creates a string with its contents
# Arguments:
# - filename (string) - full specified filename with extension
# Returns:
# - fileContents (string) - contents of specified file
def load_file(filename):
    filePath = get_path(filename)
    try:
        file = open(filePath, "r")
        fileContents = file.read()
        file.close()
    except OSError:
        return "Error: File not found"
    return fileContents
