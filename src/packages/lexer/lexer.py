
source_code = "anda count = 1;"

def main():
    if not source_code[0:]: # Quit the program if source code is empty
        print("quitting")
        exit(1)

    # source = " ".join(argv[1:])
    lex = Lexer(source_code)
    lex.start()
    for token in lex.tokens: print(token)

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.tokens: list[str] = []
    
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
                self.tokens.append("WHITESPACE")
                self.advance()

            # amaccana, anda, andamhie, IDENTIFIER
            elif "a" == self.curr_char():
                if self.expect_reserved("amaccana"): continue
                elif self.expect_reserved("anda"): continue
                elif self.expect_reserved("andamhie"): continue
                elif self.expect_reserved("awch"): continue
                else: self.expect_id()
            
            # betsung, IDENTIFIER
            elif "b" == self.curr_char():
                if self.expect_reserved("betsung"): continue
                else: self.expect_id()
            
            # chika, chorva, IDENTIFIER
            elif "c" == self.curr_char():
                if self.expect_reserved("chika"): continue
                elif self.expect_reserved("chorva"): continue
                else: self.expect_id()
            
            # ditech, IDENTIFIER
            elif "d" == self.curr_char():
                if self.expect_reserved("ditech"): continue
                else: self.expect_id()
            
            # eklabool, eme, IDENTIFIER
            elif "e" == self.curr_char():
                if self.expect_reserved("eklabool"): continue
                elif self.expect_reserved("eme"): continue
                else: self.expect_id()
            
            # forda, from, IDENTIFIER
            elif "f" == self.curr_char():
                if self.expect_reserved("forda"): continue
                elif self.expect_reserved("from"): continue
                else: self.expect_id()
            
            # ganern, givenchy, gogogo, IDENTIFIER
            elif "g" == self.curr_char():
                if self.expect_reserved("ganern"): continue
                elif self.expect_reserved("givenchy"): continue
                elif self.expect_reserved("gogogo"): continue
                else: self.expect_id()

            # keri, korik, kween, IDENTIFIER
            elif "k" == self.curr_char():
                if self.expect_reserved("keri"): continue
                elif self.expect_reserved("korik"): continue
                elif self.expect_reserved("kween"): continue
                else: self.expect_id()

            # naur, IDENTIFIER
            elif "n" == self.curr_char():
                if self.expect_reserved("naur"): continue
                else: self.expect_id()

            # pak, push, IDENTIFIER
            elif "p" == self.curr_char():
                if self.expect_reserved("pak"): continue
                elif self.expect_reserved("push"): continue
                else: self.expect_id()

            # serve, shimenet, step, IDENTIFIER
            elif "s" == self.curr_char():
                if self.expect_reserved("serve"): continue
                elif self.expect_reserved("shimenet"): continue
                elif self.expect_reserved("step"): continue
                else: self.expect_id()

            # to, IDENTIFIER
            elif "t" == self.curr_char():
                if self.expect_reserved("to"): continue
                else: self.expect_id()
            
            # versa, IDENTIFIER
            elif "v" == self.curr_char():
                if self.expect_reserved("versa"): continue
                else: self.expect_id()
            
            # wiz, IDENTIFIER
            elif "w" == self.curr_char():
                if self.expect_reserved("wiz"): continue
                else: self.expect_id()

            # IDENTIFIER
            elif self.curr_char().isalpha():
                print("working identifier")
                self.expect_id()

            # PLUS SIGN
            elif self.curr_char() == '+':
                if self.expect_reserved('+', symbol=True): continue 
                elif self.expect_reserved('++', symbol=True): continue
                elif self.expect_reserved('+=', symbol=True): continue

            # MINUS SIGN
            elif self.curr_char() == '-':
                if self.expect_reserved('-', symbol=True): continue 
                elif self.expect_reserved('--', symbol=True): continue
                elif self.expect_reserved('-=', symbol=True): continue

            # ASTERISK
            elif self.curr_char() == '*':
                if self.expect_reserved('*', symbol=True): continue 
                elif self.expect_reserved('*=', symbol=True): continue
                elif self.expect_reserved('**', symbol=True): continue
                elif self.expect_reserved('**=', symbol=True): continue
           
            # SLASH
            elif self.curr_char() == '/':
                if self.expect_reserved('/', symbol=True): continue 
                elif self.expect_reserved('/=', symbol=True): continue
                elif self.expect_reserved('//', symbol=True): continue
                elif self.expect_reserved('//=', symbol=True): continue

            # MODULO
            elif self.curr_char() == '%':
                if self.expect_reserved('%', symbol=True): continue 
                elif self.expect_reserved('%=', symbol=True): continue

            # ASSIGNMENT
            elif self.curr_char() == '=':
                if self.expect_reserved('=', symbol=True): continue 
                elif self.expect_reserved('==', symbol=True): continue
              
            # LOGICAL NOT
            elif self.curr_char() == '!':
                if self.expect_reserved('!', symbol=True): continue 
                elif self.expect_reserved('!=', symbol=True): continue

            # LOGICAL AND
            elif self.curr_char() == '&':
                if self.expect_reserved('&', symbol=True): continue 
                elif self.expect_reserved('&&', symbol=True): continue

            # LOGICAL OR
            elif self.curr_char() == '|':
                if self.expect_reserved('|', symbol=True): continue 
                elif self.expect_reserved('||', symbol=True): continue
            
            # LESS THAN
            elif self.curr_char() == '<':
                if self.expect_reserved('<', symbol=True): continue 
                elif self.expect_reserved('<=', symbol=True): continue

            # GREATER THAN
            elif self.curr_char() == '>':
                if self.expect_reserved('>', symbol=True): continue 
                elif self.expect_reserved('>=', symbol=True): continue

            # COMMA
            elif self.curr_char() == ',':
                self.expect_reserved(',', symbol=True) 

            # PERIOD
            elif self.curr_char() == '.':
                self.expect_reserved('.', symbol=True) 

            # SEMICOLON
            elif self.curr_char() == ';':
                self.expect_reserved(';', symbol=True) 

            # OPENING PARENTHESIS
            elif self.curr_char() == '(':
                self.expect_reserved('(', symbol=True) 

            # CLOSING PARENTHESIS
            elif self.curr_char() == ')':
                self.expect_reserved(')', symbol=True) 

            # OPENING BRACKET
            elif self.curr_char() == '[':
                self.expect_reserved('[', symbol=True) 

            # CLOSING BRACKET
            elif self.curr_char() == ']':
                self.expect_reserved(']', symbol=True) 

            # OPENING CURLY BRACE
            elif self.curr_char() == '{':
                self.expect_reserved('{', symbol=True) 

            # CLOSING CURLY BRACE
            elif self.curr_char() == '}':
                self.expect_reserved('}', symbol=True) 

            # NUMBER
            elif self.curr_char().isdigit():
                self.expect_int()

            else:
                print(f"unknown character: {self.curr_char()}")
                self.advance()

    def expect_reserved(self, expected: str, symbol = False) -> bool:
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
        if self.curr_char().isalpha() and not symbol:
            self.reverse(len(res))
            return False
        self.tokens.append(res)
        return True

    def expect_id(self) -> bool:
        """
        lexer for identifiers
        handles reserved words impostors
        """
        name = ""
        while self.curr_char().isalpha():
            name += self.curr_char()
            self.advance()
        # if name in reserved:
        #     self.reverse(len(name))
        #     return False
        self.tokens.append(name)
        return True

    def expect_int(self):
        """
        lexer for integers
        """
        num = ""
        while self.curr_char().isdigit():
            num += self.curr_char()
            self.advance()
        self.tokens.append(num)

if __name__ == "__main__":
    # print("Starting")
    main()