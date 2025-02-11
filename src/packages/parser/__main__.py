# This file is the entry point of the package.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))

# from lexer import *
# from token import *
# from error_handler import *
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser

if __name__ == '__main__':
    # source_code = open("A.C.C.Lang/Files/lexer_test.acc", "r").read()

    # For MacOS
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Files', 'lexer_test.acc'))
    source_code = open(file_path, "r").read()
    lexer = Lexer(source_code)
    lexer.start()

    parser = Parser(lexer.token_stream)
    parser.start()