from constants import ATOMS,DELIMS
from .error_handler import UnknownCharError, DelimError, UnclosedString, UnclosedComment, UnfinishedAndamhie
from .td import STATES
from .token import tokenize

# Lexer.token_stream stores lexemes and tokens
# Lexer.log stores the error log

class Lexer:
    def __init__(self, source: str):
        source = source.splitlines()
        self._source = [line + '\n' if x != len(source)-1 else line for x, line in enumerate(source)] # Converts source into a list of lines
        self._index = 0, 0
        self._lexemes: list[str] = []
        self.token_stream: list[dict] = []
        self.log = ""
        print(self._source)
    
    ## TRACKING CHARACTERS
    def curr_char(self):
        if self._index[1] >= len(self._source[-1]) and self._index[0] >= len(self._source) - 1: return "\0"
        return self._source[self._index[0]][self._index[1]]

    def is_EOF(self):
        return self.curr_char() == "\0"

    def advance(self, count = 1):
        # self._index = min(self._index + count, len(self._source))
        for i in range(count):
            if self._index[0] >= len(self._source) and self._index[1] >= len(self._source[0]): return
            if self._index[1] >= len(self._source[self._index[0]]) - 1 and self._index[0] < len(self._source)-1:
                self._index = min(self._index[0] + 1, len(self._source)), 0
            else: self._index = self._index[0], self._index[1] + 1

    def reverse(self, count = 1):
        # self._index = max(0, self._index - count)
        for i in range(count):
            if self._index[1] > 0: self._index = self._index[0], self._index[1] - 1
            elif self._index[0] > 0: self._index = max(0, self._index[0] - 1), len(self._source[self._index[0] - 1]) - 1
    
    def start(self):
        metadata = []
        while not self.is_EOF():
            metadata.append(self._index)
            curr_char = self.curr_char()
            if curr_char == ' ':
                self._lexemes.append(' ')
                self.advance()
                continue
            elif curr_char == '\n':
                self._lexemes.append(r'\n')
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
            elif type(lexeme) is UnfinishedAndamhie:
                print(lexeme)
                self.log += str(lexeme) + '\n'
                continue
            elif type(lexeme) in [UnclosedString]:
                print(lexeme)
                self.log += str(lexeme) + '\n'
                self.advance(len(''.join(self._source)))
            else: self._lexemes.append(lexeme)
                
        self.token_stream = tokenize(self._lexemes, metadata)
                
    def lexemize(self, curr_state: int = 0):
        branches = STATES[curr_state].branches
        for state in branches:
            curr_char = self.curr_char()
            if curr_char not in STATES[state].chars:
                if STATES[state].isEnd:
                    if state != branches[-1] and state >= 153: continue
                    if curr_char not in [*ATOMS['alphanumeric'], '_'] or state >= 153: # For reserved words
                        return DelimError(self._source[self._index[0]], self._index, STATES[state].chars)

                # For unclosed string, unclosed comment, and unfinished andamhie literal
                if curr_char == '\0' and not STATES[state].isEnd:
                    if state >= 300 and state <= 304:
                        return UnclosedString(self._source[self._index[0] - 1], self._index)

                    if state >= 306 and state <= 309: # Unclosed comment will be returned
                        return ''
                    
                if state == 287 and len(branches) == 1 and not STATES[state].isEnd:
                    return UnfinishedAndamhie(self._source[self._index[0]], self._index, STATES[state].chars)

                continue

            print(f"{curr_state} -> {state}: {curr_char if len(STATES[state].branches) > 0 else "end state"}")
            if len(STATES[state].branches) == 0: # The lexeme will be returned
                if state <= 225: return ('','') # For reserved symbols
                return ''  # For others

            self.advance()
            lexeme = self.lexemize(state)

            if type(lexeme) is str: return curr_char + lexeme
            if type(lexeme) is tuple: return (curr_char + lexeme[0], curr_char + lexeme[0])
            if type(lexeme) is DelimError: return lexeme
            if type(lexeme) is UnfinishedAndamhie: return lexeme
            if type(lexeme) is UnclosedString:
                self.reverse()
                return UnclosedString(self._source[self._index[0]], self._index)
            if state <= 153:
                self.reverse()
                
        if curr_state == 0: return UnknownCharError(self._source[self._index[0]], self._index)
        if curr_state in [202, 205]: 
            self.reverse()
            return UnknownCharError(self._source[self._index[0]], self._index)
        if curr_state >= 154 and curr_state <= 225: return DelimError(self._source[self._index[0]], self._index, STATES[state].chars)
        return None
    

if __name__ == "__main__":
    print("Starting")