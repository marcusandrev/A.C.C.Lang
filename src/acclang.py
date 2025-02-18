# This file is for the implementation of the GUI
from flask import Flask, render_template, request, jsonify
import os
from src.packages.lexer.lexer import Lexer
from src.packages.parser.parser import Parser

app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/lex', methods=['POST'])
def lex():
    # file_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'lexer_test.acc')
    # with open(file_path, 'r') as file:
    #     source_code = file.readlines()

    source_code = request.form['source_code']
    lex = Lexer(source_code)
    lex.start()
    token_stream = lex.token_stream
    print(token_stream)
    
    error_log = str(lex.log)
    print(error_log)

    parser = Parser(token_stream)
    parser.start()
    error_log += parser.log
    return jsonify({'token_stream': token_stream, 'error_log': error_log})



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5006)
