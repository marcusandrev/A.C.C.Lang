# This file is the entry point of the package.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))

from lexer import *
from token import *
from error_handler import *

if __name__ == '__main__':
    source_code = open("A.C.C.Lang/Files/lexer_test.acc", "r").readlines()
    print_lex(source_code)

    # Test()
    # Test2()
    # Test3()
