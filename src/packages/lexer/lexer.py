from constants import ATOMS,DELIMS
from .error_handler import UnknownCharError, DelimError, UnclosedString, UnclosedComment
from .td import STATES
from .token import tokenize

# Lexer.token_stream stores lexemes and tokens
# Lexer.log stores the error log

def print_lex(source: str):
    if not source[0:]: # Quit the program if source code is empty
        print("quitting")
        exit(1)

    lex = Lexer(source)
    lex.start()

    print(lex.log)

    print(f"{'-'*10}LEXEME{'-'*10 + ' '*5 + '-'*10}TOKEN{'-'*10}")
    for lexeme, token in lex.token_stream:
        print(f'{lexeme:^26}{' '*5}{token:^25}')

class Lexer:
    def __init__(self, source: str):
        source = source.splitlines()
        self._source = [line + '\n' if x != len(source)-1 else line for x, line in enumerate(source)] # Converts source into a list of lines
        self._index = 0, 0
        self._id_map: dict = {}
        self._lexemes: list[str] = []
        self.token_stream: list[dict] = []
        self.log = ""
        print(self._source)
    
    ## TRACKING CHARACTERS
    def curr_char(self):
        if self._index[0] >= len(self._source): return "\0"
        return self._source[self._index[0]][self._index[1]]
    def next_char(self):
        # if self._index[0] + 1 >= len(self._source): return "\0"
        # return self._source[self._index + 1]

        if self._index[1] + 1 >= len(self._source[self._index[0]]):
            if self._index[0] + 1 >= len(self._source): return "\0"
            else: return self._source[self._index[0] + 1][0]
        else: return self._source[self._index[0]][self._index[1] + 1]

    def is_EOF(self):
        return self.curr_char() == "\0"

    def advance(self, count = 1):
        # self._index = min(self._index + count, len(self._source))
        for i in range(count):
            if self._index[0] >= len(self._source): return
            if self._index[1] >= len(self._source[self._index[0]]) - 1: self._index = min(self._index[0] + 1, len(self._source)), 0
            else: self._index = self._index[0], self._index[1] + 1

    def reverse(self, count = 1):
        # self._index = max(0, self._index - count)
        for i in range(count):
            if self._index[1] > 0: self._index = self._index[0], self._index[1] - 1
            elif self._index[0] > 0: self._index = max(0, self._index[0] - 1), len(self._source[self._index[0] - 1]) - 1
    
    def start(self):
        while not self.is_EOF():
            curr_char = self.curr_char()
            next_char = self.curr_char()
            if curr_char == ' ':
                # self._lexemes.append(' ')
                self.advance()
                continue
            elif curr_char == '\n':
                # self._lexemes.append(r'\n')
                self.advance()
                continue
            
            lexeme = self.lexemize()
            if type(lexeme) is UnknownCharError:
                print(lexeme)
                self.log += str(lexeme) + '\n'
                self.advance()
            elif type(lexeme) is DelimError:
                print(lexeme)
                self.log += str(lexeme) + '\n'
                continue
            elif type(lexeme) in [UnclosedString, UnclosedComment]:
                print(lexeme)
                self.log += str(lexeme) + '\n'
                self.advance(len(''.join(self._source)))
            else: self._lexemes.append(lexeme)
                
        self.token_stream = tokenize(self._lexemes)
                
    def lexemize(self, curr_state: int = 0):
        branches = STATES[curr_state].branches
        for state in branches:
            curr_char = self.curr_char()
            if curr_char not in STATES[state].chars:
                if STATES[state].isEnd:
                    if state != branches[-1] and state >= 146: continue
                    if curr_char not in [*ATOMS['alphanumeric'], '_'] or state >= 146:
                        return DelimError(self._source[self._index[0]], self._index, STATES[state].chars)

                # For unclosed string
                if curr_char == '\0' and not STATES[state].isEnd:
                    if state >= 274 and state <= 278:
                        return UnclosedString(self._source[self._index[0] - 1], self._index)

                    if state >= 280 and state <= 284:
                        return UnclosedComment(self._source[self._index[0] - 1], self._index)

                continue

            print(f"{curr_state} -> {state}: {curr_char if len(STATES[state].branches) > 0 else "end state"}")
            if len(STATES[state].branches) == 0: return '' # The lexeme will be returned

            self.advance()
            lexeme = self.lexemize(state)

            if type(lexeme) is str: return curr_char + lexeme
            if type(lexeme) is DelimError: return lexeme
            if type(lexeme) is UnclosedString:
                self.reverse()
                return UnclosedString(self._source[self._index[0]], self._index)
            if type(lexeme) is UnclosedComment:
                self.reverse()
                return UnclosedComment(self._source[self._index[0] - 1], self._index)
            if state <= 146:
                self.reverse()
                
        if curr_state == 0: return UnknownCharError(self._source[self._index[0]], self._index)
        return None

if __name__ == "__main__":
    print("Starting")