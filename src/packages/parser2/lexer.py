# lexer.py
import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value", "line", "col"])

class Lexer:
    def __init__(self, rules, skip_whitespace=True):
        """
        rules: list of (NAME, regex_pattern)
        skip_whitespace: skip tokens of type 'WS' if True
        """
        parts = []
        for name, patt in rules:
            parts.append(f"(?P<{name}>{patt})")
        self.regex = re.compile("|".join(parts))
        self.skip_whitespace = skip_whitespace

    def input(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def token(self):
        if self.pos >= len(self.text):
            return None
        m = self.regex.match(self.text, self.pos)
        if not m:
            raise SyntaxError(f"Illegal character at {self.line}:{self.col!r}")
        kind = m.lastgroup
        val  = m.group(kind)
        # advance position
        self.pos = m.end()
        nl = val.count("\n")
        if nl:
            self.line += nl
            self.col = len(val) - val.rfind("\n")
        else:
            self.col += len(val)
        if self.skip_whitespace and kind == "WS":
            return self.token()
        return Token(kind, val, self.line, self.col)

    def tokens(self):
        while True:
            tok = self.token()
            if tok is None:
                break
            yield tok

# Example usage:
if __name__ == "__main__":
    rules = [
        ("WS",          r"[ \t\n]+"),
        ("LPAR",        r"\("),
        ("RPAR",        r"\)"),
        ("LBRACE",      r"\{"),
        ("RBRACE",      r"\}"),
        ("SEMICOLON",   r";"),
        ("COMMA",       r","),
        ("PLUS",        r"\+"),
        ("MINUS",       r"-"),
        ("TIMES",       r"\*"),
        ("DIVIDE",      r"/"),
        ("ID",          r"[a-zA-Z][a-zA-Z0-9_]{0,19}"),
        ("ANDA_LITERAL",   r"[0-9]+"),
        ("ANDAMHIE_LITERAL", r"[0-9]+\.[0-9]+"),
        ("CHIKA_LITERAL",  r"\"([^\"\\]|\\.)*\""),
        # … add all other token defs from your grammar …
    ]
    lx = Lexer(rules)
    lx.input('naur anda x = 42;')
    for t in lx.tokens():
        print(t)
