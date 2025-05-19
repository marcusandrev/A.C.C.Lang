from lark import Lark
from .error_handler import UnexpectedError

class Parser:
    def __init__(self, source_code):
        self.log = ''
        self._source_code = source_code
        self.ast = ''

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
            elif token == 'times': token = '*'
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
            elif token == 'greater_than': token = '>'
            elif token == 'less_than': token = '<'
            elif token == 'divide': token = '/'
            elif token == 'plus': token = '+'
            elif token == 'modulo': token = '%'
            elif token == 'minus': token = '-'
            elif token == 'naur': token = 'naur'
            elif token == 'shimenet': token = 'shimenet'
            elif token == 'anda': token = 'anda'
            elif token == 'andamhie': token = 'andamhie'
            elif token == 'chika': token = 'chika'
            elif token == 'eklabool': token = 'eklabool'
            elif token == 'korik': token = 'korik'
            elif token == 'eme': token = 'eme'
            elif token == 'givenchy': token = 'givenchy'
            elif token == 'serve': token = 'serve'
            elif token == 'pak': token = 'pak'
            elif token == 'ganern': token = 'ganern'
            elif token == 'versa': token = 'versa'
            elif token == 'betsung': token = 'betsung'
            elif token == 'ditech': token = 'anda'
            elif token == 'forda': token = 'forda'
            elif token == 'keri': token = 'keri'
            elif token == 'lang': token = 'lang'
            elif token == 'amaccana': token = 'amaccana'
            elif token == 'gogogo': token = 'gogogo'
            elif token == 'kween': token = 'kween'
            elif token == 'push': token = 'push'
            elif token == 'from': token = 'from'
            elif token == 'to': token = 'to'
            elif token == 'step': token = 'step'
            if token in temp: continue
            temp.append(token)
        return temp

    def start(self):

        with open("Files/cfg/grammar.lark", "r") as file:
            grammar = file.read()

        parser = Lark(grammar, parser="earley", lexer="basic")

        try:
            parse_tree = parser.parse(self._source_code)
            self.ast = parse_tree
        except Exception as e:
            source = self._source_code.splitlines('\n')
            source[-1] += ' '
            index = (e.line if e.line > 0 else len(source), e.column if e.column > 0 else len(source[-1]))
            unexpected = UnexpectedError(source[index[0]-1], index)

            try:
                expected = e.allowed
            except:
                expected = e.expected

            expected = self.clean_expected(expected)
            self.log = f'Unexpected token at line {index[0]} column {index[1]}: {unexpected}\nExpected any: {expected}'