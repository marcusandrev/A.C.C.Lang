# This file is the entry point of the package.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))

from lexer import *
from token import *
from error_handler import *

source_code = r"""
/^Testing Lexer^/
shimenet kween() {
    chika name = "Shrek";
    anda age = 247.365;
    serve("Name: " + name + ", Age: " + age);
}
"""

if __name__ == '__main__':
    print_lex(source_code)
    # Test()
    # Test2()
    # Test3()
