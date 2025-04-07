# This file is for the implementation of the GUI
from flask import Flask, render_template, request, jsonify
import os
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser
from src.packages.parser.semantic_analyzer import SemanticAnalyzer
from src.packages.codegen.ast_generator import ASTGenerator
from src.packages.codegen.code_generation import CodeGenerator

app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')

# @app.route('/lex', methods=['POST'])
# def lex():
#     # file_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'lexer_test.acc')
#     # with open(file_path, 'r') as file:
#     #     source_code = file.readlines()

#     source_code = request.form['source_code']
#     lex = Lexer(source_code)
#     lex.start()
#     token_stream = lex.token_stream
#     print(token_stream)
    
#     error_log = lex.log
#     print(error_log)
#     return jsonify({'token_stream': token_stream, 'error_log': str(error_log)})

@app.route('/run_lexer', methods=['POST'])
def run_lexer():
    source_code = request.form.get('source_code')
    
    # if not source_code.strip():
    #     return jsonify({'error': 'No source code provided'}), 400

    print("running lexer")
    lex = Lexer(source_code)
    lex.start()
    token_stream = [stream[0] for stream in lex.token_stream]
    # token_stream = lex.token_stream   # Use this if you want to see the token stream with line numbers
    print(token_stream)
    
    error_log = str(lex.log)
    print(error_log)

    if len(error_log) == 0: # Only run parser if there is no lexical error
        print("running syntax")
        parser = Parser(source_code, token_stream)
        parser.start()
        error_log = parser.log

        if len(error_log) == 0: # Only run semantic if there is no syntax error
            print("running semantic")
            analyzer = SemanticAnalyzer(lex.token_stream)
            analyzer.analyze()
            error_log = analyzer.log
            print(analyzer.symbol_table)

            if len(error_log) == 0:
                ast_gen = ASTGenerator(lex.token_stream)
                ast = ast_gen.generate()
                print(ast)
                target_code = CodeGenerator().generate(ast)
                print(target_code)

    print(f"TOKENS: {token_stream}")
    print(f"LOG: {error_log}")


    return jsonify({'tokens': token_stream, 'log': error_log, 'error_log': error_log})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5006)
