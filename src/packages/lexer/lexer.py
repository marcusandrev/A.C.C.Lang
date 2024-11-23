# Reading of the lexemes                ✓
# Helper functions
# - reserve words   (expect_reserved)   ✓
# - identifiers     (expect_id)         ✓
# - string          (expect_string)     ✓
# - comment         (expect_comment)    ✓
# - int/float       (expect_int_float)  ✓
# - error handling                      X

from constants import ATOMS,DELIMS

def print_lex(source: str):
    if not source[0:]: # Quit the program if source code is empty
        print("quitting")
        exit(1)

    # source = " ".join(argv[1:])
    lex = Lexer(source)
    lex.start()
    print(f"{'-'*10}LEXEME{'-'*10 + ' '*5 + '-'*10}TOKEN{'-'*10}")
    for lexeme, token in lex.token_stream:
        print(f'{lexeme:^26}{' '*5}{token:^25}')

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.token_stream: list[dict] = []
        self.id_map: dict = {}
    
    ## TRACKING CHARACTERS
    def curr_char(self):
        if self.index >= len(self.source): return "\0"
        return self.source[self.index]
    def next_char(self):
        if self.index + 1 >= len(self.source): return "\0"
        return self.source[self.index + 1]
    def is_EOF(self):
        return self.curr_char() == "\0"

    def advance(self, count = 1):
        self.index = min(self.index + count, len(self.source))
    def reverse(self, count = 1):
        self.index = max(0, self.index - count)
    
    def start(self):
        while not self.is_EOF():
            if self.curr_char() in [" ", "\t", "\n"]: #, "\r"]:
                # self.token_stream.append("WHITESPACE")
                self.advance()
                continue
            
            # if self.curr_char() == ' ':
            #     self.token_stream.append((" ","WHITESPACE"))
            #     self.advance()
            #     continue
            
            # elif self.curr_char() == '\n':
            #     self.token_stream.append((r"\n", "NEWLINE"))
            #     self.advance()
            #     continue

            # amaccana, anda, andamhie, IDENTIFIER
            elif "a" == self.curr_char():
                if self.expect_reserved("amaccana", DELIMS['amaccana_gogogo_delim']): continue
                elif self.expect_reserved("anda", ATOMS['similar_delim']): continue
                elif self.expect_reserved("andamhie", ATOMS['similar_delim']): continue
                else: self.expect_id()
            
            # betsung, IDENTIFIER
            elif "b" == self.curr_char():
                if self.expect_reserved("betsung", ATOMS['similar_delim']): continue
                else: self.expect_id()
            
            # chika, chorva, IDENTIFIER
            elif "c" == self.curr_char():
                if self.expect_reserved("chika", ATOMS['similar_delim']): continue
                else: self.expect_id()
                # elif self.expect_reserved("chorva"): continue
            
            # ditech, IDENTIFIER
            elif "d" == self.curr_char():
                if self.expect_reserved("ditech", DELIMS['ditech_delim']): continue
                else: self.expect_id()
            
            # eklabool, eme, IDENTIFIER
            elif "e" == self.curr_char():
                if self.expect_reserved("eklabool", ATOMS['similar_delim']): continue
                elif self.expect_reserved("eme", ATOMS['value_delim']): continue
                else: self.expect_id()
            
            # forda, from, IDENTIFIER
            elif "f" == self.curr_char():
                if self.expect_reserved("forda", DELIMS['control_flow_delim']): continue
                elif self.expect_reserved("from", ATOMS['similar_delim']): continue
                else: self.expect_id()
            
            # ganern, givenchy, gogogo, IDENTIFIER
            elif "g" == self.curr_char():
                if self.expect_reserved("ganern", DELIMS['kerilang_ganern_delim']): continue
                elif self.expect_reserved("givenchy", DELIMS['control_flow_delim']): continue
                elif self.expect_reserved("gogogo", DELIMS['amaccana_gogogo_delim']): continue
                else: self.expect_id()

            # keri, korik, kween, IDENTIFIER
            elif "k" == self.curr_char():
                if self.expect_reserved("keri", DELIMS['control_flow_delim']): continue
                elif self.expect_reserved("korik", DELIMS['value_delim']): continue
                elif self.expect_reserved("kween", DELIMS['control_flow_delim']): continue
                else: self.expect_id()

            elif "l" == self.curr_char():
                if self.expect_reserved("lang", DELIMS['kerilang_ganern_delim']): continue
                else: self.expect_id()

            # naur, IDENTIFIER
            elif "n" == self.curr_char():
                if self.expect_reserved("naur", ATOMS['similar_delim']): continue
                else: self.expect_id()

            # pak, push, IDENTIFIER
            elif "p" == self.curr_char():
                if self.expect_reserved("pak", DELIMS['control_flow_delim']): continue
                elif self.expect_reserved("push", DELIMS['control_flow_delim']): continue
                else: self.expect_id()

            # serve, shimenet, step, IDENTIFIER
            elif "s" == self.curr_char():
                if self.expect_reserved("serve", DELIMS['control_flow_delim']): continue
                elif self.expect_reserved("shimenet", ATOMS['similar_delim']): continue
                elif self.expect_reserved("step", ATOMS['similar_delim']): continue
                else: self.expect_id()

            # to, IDENTIFIER
            elif "t" == self.curr_char():
                if self.expect_reserved("to", ATOMS['similar_delim']): continue
                else: self.expect_id()
            
            # versa, IDENTIFIER
            elif "v" == self.curr_char():
                if self.expect_reserved("versa", DELIMS['control_flow_delim']): continue
                else: self.expect_id()
            
            # wiz, IDENTIFIER
            elif "w" == self.curr_char():
                if self.expect_reserved("wiz", DELIMS['wiz_delim']): continue
                else: self.expect_id()

            # IDENTIFIER
            elif self.curr_char().isalpha():
                print("working identifier")
                self.expect_id()

            # NUMBER
            elif self.curr_char().isdigit():
                self.expect_int_float()

            # PLUS SIGN
            elif self.curr_char() == '+':
                if self.expect_reserved('+', DELIMS['plus_and_or_delim'], symbol=True): continue 
                elif self.expect_reserved('++', DELIMS['unary_delim'], symbol=True): continue
                elif self.expect_reserved('+=', DELIMS['most_symbol_delim'], symbol=True): continue

            # MINUS SIGN
            elif self.curr_char() == '-':
                if self.expect_reserved('-', DELIMS['minus_delim'], symbol=True): continue 
                elif self.expect_reserved('--', DELIMS['unary_delim'], symbol=True): continue
                elif self.expect_reserved('-=', DELIMS['most_symbol_delim'], symbol=True): continue

            # ASTERISK
            elif self.curr_char() == '*':
                if self.expect_reserved('*', DELIMS['most_symbol_delim'], symbol=True): continue 
                elif self.expect_reserved('*=', DELIMS['most_symbol_delim'], symbol=True): continue
                elif self.expect_reserved('**', DELIMS['most_symbol_delim'], symbol=True): continue
                elif self.expect_reserved('**=', DELIMS['most_symbol_delim'], symbol=True): continue
           
            # SLASH
            elif self.curr_char() == '/':
                if self.expect_comment(): continue
                elif self.expect_reserved('/', DELIMS['most_symbol_delim'], symbol=True): continue 
                elif self.expect_reserved('/=', DELIMS['most_symbol_delim'], symbol=True): continue
                elif self.expect_reserved('//', DELIMS['most_symbol_delim'], symbol=True): continue
                elif self.expect_reserved('//=', DELIMS['most_symbol_delim'], symbol=True): continue

            # MODULO
            elif self.curr_char() == '%':
                if self.expect_reserved('%', DELIMS['most_symbol_delim'], symbol=True): continue 
                elif self.expect_reserved('%=', DELIMS['most_symbol_delim'], symbol=True): continue

            # EQUAL
            elif self.curr_char() == '=':
                if self.expect_reserved('=', DELIMS['equal_comma_delim'], symbol=True): continue 
                elif self.expect_reserved('==', DELIMS['logical_not_delim'], symbol=True): continue
              
            # LOGICAL NOT
            elif self.curr_char() == '!':
                if self.expect_reserved('!', DELIMS['logical_not_delim'], symbol=True): continue 
                elif self.expect_reserved('!=', DELIMS['logical_not_delim'], symbol=True): continue
            
            # LESS THAN
            elif self.curr_char() == '<':
                if self.expect_reserved('<', DELIMS['most_symbol_delim'], symbol=True): continue 
                elif self.expect_reserved('<=', DELIMS['most_symbol_delim'], symbol=True): continue

            # GREATER THAN
            elif self.curr_char() == '>':
                if self.expect_reserved('>', DELIMS['most_symbol_delim'], symbol=True): continue 
                elif self.expect_reserved('>=', DELIMS['most_symbol_delim'], symbol=True): continue

            # LOGICAL AND
            elif self.curr_char() == '&':
                if self.expect_reserved('&&', DELIMS['plus_and_or_delim'], symbol=True): continue

            # LOGICAL OR
            elif self.curr_char() == '|':
                if self.expect_reserved('||', DELIMS['plus_and_or_delim'], symbol=True): continue

            # COMMA
            elif self.curr_char() == ',':
                self.expect_reserved(',', DELIMS['equal_comma_delim'], symbol=True) 

            # PERIOD
            # elif self.curr_char() == '.':
            #     self.expect_reserved('.', symbol=True) 

            # SEMICOLON
            elif self.curr_char() == ';':
                self.expect_reserved(';', DELIMS['terminator_delim'], symbol=True) 

            # OPENING PARENTHESIS
            elif self.curr_char() == '(':
                self.expect_reserved('(', DELIMS['open_parenthesis_delim'], symbol=True) 

            # CLOSING PARENTHESIS
            elif self.curr_char() == ')':
                self.expect_reserved(')', DELIMS['close_parenthesis_delim'], symbol=True) 

            # OPENING BRACKET
            elif self.curr_char() == '[':
                self.expect_reserved('[', DELIMS['open_bracket_delim'], symbol=True) 

            # CLOSING BRACKET
            elif self.curr_char() == ']':
                self.expect_reserved(']', DELIMS['close_bracket_delim'], symbol=True) 

            # OPENING CURLY BRACE
            elif self.curr_char() == '{':
                self.expect_reserved('{', DELIMS['open_brace_delim'], symbol=True) 

            # CLOSING CURLY BRACE
            elif self.curr_char() == '}':
                self.expect_reserved('}', DELIMS['close_brace_delim'], symbol=True) 

            elif self.curr_char() == '"':
                self.expect_string()

            else:
                print(f"unknown character: {self.curr_char()}")
                self.advance()

    def expect_reserved(self, expected: str, delims: list = [], symbol = False) -> bool:
        """
        generic lexer for reserved words/symbols.
        handles possible identifiers that contain reserved words in its name
        """
        res = ""
        for char in expected:
            if self.curr_char() != char:
                self.reverse(len(res))
                return False
            res += char
            self.advance()

        # currently, cursor is at delimiter
        # check if word is IDENTIFIER if it is not a res symbol
        if self.curr_char() not in delims and not symbol:
            self.reverse(len(res))
            return False
        self.token_stream.append((res,res))
        return True

    def expect_id(self) -> bool:
        """
        lexer for identifiers
        handles reserved words impostors
        """
        name = ""
        while self.curr_char().isalnum() or self.curr_char() == '_':
            name += self.curr_char()
            self.advance()
        # if name in reserved:
        #     self.reverse(len(name))
        #     return False

        token = self.id_map.get(name, f'ID_{len(self.id_map) + 1}')
        self.id_map[name] = token

        self.token_stream.append((name, token))
        return True
    
    def expect_comment(self):
        comment = ''
        if self.curr_char() + self.next_char() == '/^':
            while self.curr_char() != '\0':
                comment += self.curr_char()
                if self.curr_char() == '^' and self.next_char() == '/':
                    comment += '/'
                    self.advance(2)   
                    break
                self.advance()

            self.token_stream.append((comment,'COMMENT'))
            return True
        
        return False

    def expect_string(self):
        self.advance()
        string = '"'
        escape = False
        while self.curr_char() != '"' and self.curr_char() != '\0':
            string += self.curr_char()
            self.advance()

            if self.curr_char() == '\\' and self.next_char() == '"':
                string += self.curr_char() + self.next_char()
                self.advance(2)
            
            if self.curr_char() == '"':
                string += self.curr_char()
                self.advance()
                break

        self.token_stream.append((string,'CHIKA_LITERAL'))
        return True

    def expect_int_float(self):
        """
        lexer for integers
        """
        num = ""
        while self.curr_char().isdigit():
            num += self.curr_char()
            self.advance()
        
        if self.curr_char() != '.':
            self.token_stream.append((num,'ANDA_LITERAL'))
            return

        num += '.'
        self.advance()
        while self.curr_char().isdigit():
            num += self.curr_char()
            self.advance()
        self.token_stream.append((num,'ANDAMHIE_LITERAL'))

        

if __name__ == "__main__":
    print("Starting")