# This file is used for the error handling of the lexer
from constants import ATOMS

def Test3():
    print("Test for Error Handling")

class UnknownCharError():
    def __init__(self, line: str, position: tuple[int, int]):
        self._line = line.replace('\n', '')
        self._position = position

    def __str__(self):
        error_message = f"unknown character: '{self._line[self._position[1]]}'\n" \
                        f" {self._position[0]+1:<5}|{self._line}\n" \
                        f"      |{' '*self._position[1]}^\n"
        
        return error_message

class DelimError():
    def __init__(self, line: str, position: tuple[int, int], delims: list):
        self._line = line.replace('\n', '')
        self._position = position
        self._delims = shorten_delims(list(delims))

    def __str__(self):
        error_message = f"Invalid Delimiter:\n" \
                        f" {self._position[0]+1:<5}|{self._line}\n" \
                        f"      |{' '*self._position[1]}^\n"
        
        return error_message

class UnfinishedAndamhie():
    def __init__(self, line: str, position: tuple[int, int], delims: list):
        self._line = line.replace('\n', '')
        self._position = position
        self._delims = shorten_delims(list(delims))

    def __str__(self):
        error_message = f"unfinished andamhie literal: expected any {self._delims}\n" \
                        f" {self._position[0]+1:<5}|{self._line}\n" \
                        f"      |{' '*self._position[1]}^\n"
        
        return error_message

class UnclosedString():
    def __init__(self, line: str, position: tuple[int, int]):
        self._line = line.replace('\n', '')
        self._position = position

    def __str__(self):
        error_message = f"unclosed string: expected '\"'\n" \
                        f" {self._position[0]+1:<5}|{self._line}\n" \
                        f"      |{' '*self._position[1]}^\n"
        
        return error_message

class UnclosedComment():
    def __init__(self, line: str, position: tuple[int, int]):
        self._line = line.replace('\n', '')
        self._position = position

    def __str__(self):
        error_message = f"unclosed comment: expected '^/'\n" \
                        f" {self._position[0]+1:<5}|{self._line}\n" \
                        f"      |{' '*self._position[1]}^\n"
        
        return error_message

def shorten_delims(delims: list):
    if all(d in delims for d in ATOMS['alphabet']):
        for d in ATOMS['alphabet']:
            if d in delims:
                delims.remove(d)
        delims.append('A-Z')
        delims.append('a-z')

    if all(d in delims for d in ATOMS['digit']):
        for d in ATOMS['digit']:
            if d in delims:
                delims.remove(d)
        delims.append('0-9')

    return delims

if __name__ == '__main__':
    error_type = "UnknownError"
    line = '      serve("Hello, World"); #'
    position = (6, 29)
    print(UnknownCharError(line, position))

