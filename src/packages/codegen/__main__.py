# This file is the entry point of the package.
import sys, os, subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))

# from lexer import *
# from token import *
# from error_handler import *
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser
from src.packages.parser.parser import Parser
from src.packages.parser.semantic_analyzer import SemanticAnalyzer
from src.packages.codegen.ast_generator import ASTGenerator
from src.packages.codegen.code_generation import CodeGenerator

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
        parser = Parser(source_code)
        # parser = parse(lexer.token_stream)
        parser.start()
        print(parser.log)

        if len(parser.log) <= 0:
            analyzer = SemanticAnalyzer(lexer.token_stream)
            analyzer.analyze()
            print(analyzer.symbol_table)
            print(analyzer.log)

            if len(analyzer.log) <= 0:
                ast_gen = ASTGenerator(lexer.token_stream)
                ast = ast_gen.generate()
                print(ast)
                target_code = CodeGenerator().generate(ast)
                print(target_code)

                output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Files', 'compiled', 'compiled.py'))
                with open(output_path, "w") as f:
                    f.write(target_code)

                # Run as subprocess
                print("\n=== Running ACCLANG ===\n")
                subprocess.run(["python", output_path])
            # if not analyzer.analyze():
            #     print("Semantic errors found.")