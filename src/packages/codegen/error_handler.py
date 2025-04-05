# This file is used for the error handling of the parser

def Test3():
    print("Test for Error Handling")

class SemanticError(Exception):
    def __init__(self, message, line = None):
        location = f" at line {line + 1}" if line else ""
        super().__init__(f"{message}{location}")

# if __name__ == '__main__':
#     line = '      serve("Hello, World"); #'
#     position = (6, 29)
#     print(UnexpectedError(line, position))