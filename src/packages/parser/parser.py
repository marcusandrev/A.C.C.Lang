from lark import Lark
from .error_handler import UnexpectedError

class Parser:
    def __init__(self, source_code, token_stream):
        self._token_stream = token_stream
        self.log = ''
        self._source_code = source_code
        # for token in self._token_stream:
        #     if token[1] == 'whitespace': self._source_code += ' '
        #     elif token[1] == 'newline': self._source_code += '\n'
        #     elif token[1][:2] == 'id': self._source_code += 'id'
        #     else: self._source_code += token[1]
        # print(f'\n{self._source_code}')

    def clean_expected(self, expected: list):
        temp = []
        for allowed in expected:
            token = allowed.lower()
            if token == 'lpar': token = '('
            elif token == 'rpar': token = ')'
            elif token == 'lbrace': token = '{'
            elif token == 'rbrace': token = '}'
            elif token == 'lsqb': token = '['
            elif token == 'rsqb': token = ']'
            elif token == 'equal': token = '='
            elif token == 'comma': token = ','
            elif token == 'semicolon': token = ';'
            elif token == 'plus_equal': token = '+='
            elif token == 'minus_equal': token = '-='
            elif token == 'modulo_equal': token = '%='
            elif token == 'divide_equal': token = '/='
            elif token == 'floor_equal': token = '//='
            elif token == 'times_equal': token = '*='
            elif token == 'exponentiate_equal': token = '**='
            elif token == 'star': token = '*'
            elif token == 'exponentiate': token = '**'
            elif token == 'floor': token = '//'
            elif token == 'greater_equal': token = '>='
            elif token == 'less_equal': token = '<='
            elif token == 'equal_equal': token = '=='
            elif token == 'not_equal': token = '!='
            elif token == 'and': token = '&&'
            elif token == 'or': token = '||'
            elif token == 'not': token = '!'
            elif token == 'minus_minus': token = '--'
            elif token == 'plus_plus': token = '++'
            elif token == 'morethan': token = '>'
            elif token == 'lessthan': token = '<'
            elif token == 'slash': token = '/'
            elif token == 'plus': token = '+'
            elif token == 'percent': token = '%'
            elif token == 'minus': token = '-'
            if token in temp: continue
            temp.append(token)
        return temp

    def start(self):

        with open("Files/cfg/grammar.lark", "r") as file:
            grammar = file.read()

        parser = Lark(grammar, parser="earley", lexer="basic")

        try:
            parse_tree = parser.parse(self._source_code)
            print(parse_tree)
        except Exception as e:
            # print(f"Parsing error: {e}")
            source = self._source_code.splitlines('\n')
            source[-1] += ' '
            index = (e.line if e.line > 0 else len(source), e.column if e.column > 0 else len(source[-1]))
            unexpected = UnexpectedError(source[index[0]-1], index)
            # for char in source[index[0]-1][index[1]-1:]:
            #     if char in [' ', '\n']: break
            #     unexpected += char

            try:
                expected = e.allowed
            except:
                expected = e.expected

            expected = self.clean_expected(expected)
            print(e)
            self.log = f'Unexpected token at line {index[0]} column {index[1]}: {unexpected}\nExpected any: {expected}'
            print(self.log)