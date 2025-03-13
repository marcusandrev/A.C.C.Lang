# This file is the entry point of the package.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))

# from lexer import *
# from token import *
# from error_handler import *
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser
from src.packages.parser.parse import Parser as parse
from src.packages.parser.semantic_analyzer import SemanticAnalyzer

if __name__ == '__main__':
    # source_code = open("A.C.C.Lang/Files/lexer_test.acc", "r").read()

    # For MacOS
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Files', 'lexer_test.acc'))
    source_code = open(file_path, "r").read()
    lexer = Lexer(source_code)
    lexer.start()

    print(lexer.log)

    if len(lexer.log) <= 0:
        print(lexer.token_stream, end='\n\n')
        parser = Parser(source_code, lexer.token_stream)
        # parser = parse(lexer.token_stream)
        parser.start()
        print(parser.log)

        if len(parser.log) <= 0:
            analyzer = SemanticAnalyzer(lexer.token_stream)
            analyzer.analyze()
            print(analyzer.symbol_table)
            print(analyzer.log)
            # if not analyzer.analyze():
            #     print("Semantic errors found.")