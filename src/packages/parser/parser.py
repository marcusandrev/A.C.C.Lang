class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        print("parser initialized")
        self._tokens = [token for token in tokens if token[1] not in ['whitespace','newline']] # Removes whitespace and newline tokens
        print(self._tokens)
        self._index = 0

    def curr_token(self):
        if self._index + 1 > len(self._tokens): return None
        return self._tokens[self._index][1]

    def next_token(self):
        if self._index + 1 >= len(self._tokens): return None
        return self._tokens[self._index + 1][1]

    def is_EOF(self):
        return self.curr_token() == None

    def advance(self, count = 1):
        self._index = min(self._index + count, len(self._tokens))

    def reverse(self, count = 1):
        self._index = max(0, self._index - count)

    def start(self):
        while not self.is_EOF():
            curr_token = self.curr_token()
            next_token = self.next_token()

            if curr_token in ['anda', 'andamhie', 'chika', 'eklabool']:
                print(curr_token)
                self.advance()
                self.parse_function()
            
            if curr_token == 'shimenet':
                pass
            else:
                self.advance()

    def parse_function(self):
        if self.curr_token().split('_')[0] == "id":
            print(self.curr_token())
            self.advance()
        else:
            print("Error: Expected id but got", self.curr_token())
            return
        
        if res := self.parse_args():
            print(res)
    
    def parse_args(self):
        if self.curr_token() == "(":
            self.advance()
            self.parse_args()
        else:
            print("Error: Expected ( but got", self.curr_token())
            return

# if __name__ == '__main__':
#     p = parser()