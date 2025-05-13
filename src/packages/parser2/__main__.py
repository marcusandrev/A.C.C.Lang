# main.py
from src.packages.parser2.lexer import Lexer
from src.packages.parser2.parser2 import Parser
from src.packages.parser2.error_handler import UnexpectedError

rules = [
    # Whitespace
    ("WS",              r"[ \t\n]+"),

    # Parentheses / Braces / Brackets
    ("LPAR",            r"\("),
    ("RPAR",            r"\)"),
    ("LBRACE",          r"\{"),
    ("RBRACE",          r"\}"),
    ("LSQB",            r"\["),
    ("RSQB",            r"\]"),

    # Punctuation
    ("COLON",           r":"),
    ("COMMA",           r","),
    ("SEMICOLON",       r";"),

    # Compound operators (order matters)
    ("EXPONENTIATE_EQUAL", r"\*\*="),
    ("FLOOR_EQUAL",        r"//="),
    ("TIMES_EQUAL",        r"\*="),
    ("DIVIDE_EQUAL",       r"/="),
    ("MODULO_EQUAL",       r"%="),
    ("PLUS_EQUAL",         r"\+="),
    ("MINUS_EQUAL",        r"-="),

    ("EXPONENTIATE",    r"\*\*"),
    ("FLOOR",           r"//"),

    ("GREATER_EQUAL",   r">="),
    ("LESS_EQUAL",      r"<="),
    ("EQUAL_EQUAL",     r"=="),
    ("NOT_EQUAL",       r"!="),

    ("AND",             r"&&"),
    ("OR",              r"\|\|"),

    ("PLUS_PLUS",       r"\+\+"),
    ("MINUS_MINUS",     r"--"),

    # Single-char operators
    ("PLUS",            r"\+"),
    ("MINUS",           r"-"),
    ("TIMES",           r"\*"),
    ("DIVIDE",          r"/"),
    ("MODULO",          r"%"),
    ("NOT",             r"!"),
    ("GREATER_THAN",    r">"),
    ("LESS_THAN",       r"<"),
    ("EQUAL",           r"="),

    # Keywords (all from your grammar.lark)
    ("NAUR",            r"naur"),
    ("SHIMENET",        r"shimenet"),
    ("ANDA",            r"anda"),
    ("ANDAMHIE",        r"andamhie"),
    ("ADELE",           r"adele"),
    ("ADELETE",         r"adelete"),
    ("CHIKA",           r"chika"),
    ("EKLABOOL",        r"eklabool"),
    ("KORIK",           r"korik"),
    ("EME",             r"eme"),
    ("GIVENCHY",        r"givenchy"),
    ("SERVE",           r"serve"),
    ("PAK",             r"pak"),
    ("GANERN",          r"ganern"),
    ("VERSA",           r"versa"),
    ("BETSUNG",         r"betsung"),
    ("DITECH",          r"ditech"),
    ("FORDA",           r"forda"),
    ("KERI",            r"keri"),
    ("LANG",            r"lang"),
    ("LEN",             r"len"),
    ("AMACCANA",        r"amaccana"),
    ("GOGOGO",          r"gogogo"),
    ("KWEEN",           r"kween"),
    ("PUSH",            r"push"),
    ("FROM",            r"from"),
    ("TO",              r"to"),
    ("STEP",            r"step"),

    # Literals
    ("ANDA_LITERAL",    r"[0-9]+"),
    ("ANDAMHIE_LITERAL",r"[0-9]+\.[0-9]+"),
    ("CHIKA_LITERAL",   r'"([^"\\]|\\.)*"'),

    # Identifier (after keywords so they don’t match here)
    ("ID",              r"[a-zA-Z][a-zA-Z0-9_]{0,19}"),
]

# Sample source code input
source_code = '''

shimenet kween(){
    anda x = 5 - 10;
}
'''

def run():
    try:
        lexer = Lexer(rules)
        lexer.input(source_code)
        tokens = list(lexer.tokens())

        parser = Parser(tokens)
        ast = parser.parse()
        print("AST:")
        print(ast)
    except UnexpectedError as e:
        print("Syntax Error:")
        print(e)

if __name__ == "__main__":
    run()
