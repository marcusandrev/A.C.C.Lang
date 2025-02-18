from lark import Lark

class Parser:
    def __init__(self, token_stream):
        self._token_stream = token_stream
        self.log = ''
        self._source_code = ''
        for token in self._token_stream:
            if token[1] == 'whitespace': self._source_code += ' '
            elif token[1] == 'newline': self._source_code += '\n'
            elif token[1][:2] == 'id': self._source_code += 'id'
            else: self._source_code += token[1]
        print(self._source_code)

    def get_first_set(self, non_terminals, productions):
        first_set = {nt: set() for nt in non_terminals}

        def first(symbol):
            if symbol not in non_terminals:
                return {symbol}
            if not first_set[symbol]:
                for production in productions:
                    head, body = production.split("->")
                    head = head.strip()
                    body = body.strip().split()
                    if head == symbol:
                        if body[0] == 'Î»':
                            first_set[symbol].add('λ')
                        else:
                            for sym in body:
                                sym_first = first(sym)
                                first_set[symbol].update(sym_first - {'λ'})
                                if 'λ' not in sym_first:
                                    break
                            else:
                                first_set[symbol].add('λ')
            return first_set[symbol]

        for nt in non_terminals:
            first(nt)

        return first_set

    def get_follow_set(self, non_terminals, productions, first_set):
        follow_set = {nt: set() for nt in non_terminals}
        start_symbol = non_terminals[0]
        follow_set[start_symbol].add('$')

        def follow(symbol):
            for production in productions:
                head, body = production.split("->")
                head = head.strip()
                body = body.strip().split()
                for i, sym in enumerate(body):
                    if sym == symbol:
                        if i + 1 < len(body):
                            next_sym = body[i + 1]
                            if next_sym not in non_terminals:
                                follow_set[symbol].update({next_sym})
                            else: 
                                follow_set[symbol].update(first_set[next_sym] - {'λ'})
                                if 'λ' in first_set[next_sym]:
                                    follow_set[symbol].update(follow(next_sym))
                        else:
                            if head != symbol:
                                follow_set[symbol].update(follow(head))
            return follow_set[symbol]

        for nt in non_terminals:
            follow(nt)

        return follow_set

    def get_predict_set(self, productions, first_set, follow_set):
        predict_set = {}
        for production in productions:
            head, body = production.split("->")
            head = head.strip()
            body = body.strip().split()
            if body[0] == 'Î»':
                predict_set[production] = follow_set[head]
            else:
                predict_set[production] = set()
                if first_set.get(body[0]) is None:
                    predict_set[production].add(body[0])
                else:
                    predict_set[production].update(first_set[body[0]] - {'λ'})
                    if 'λ' in first_set[body[0]]:
                        predict_set[production].update(follow_set[body[0]])
        return predict_set

    def convert_to_ebnf(self, non_terminals, productions):
        ebnf_dict = {}
        for production in productions:
            head, body = production.split("->")
            head = head.strip().lstrip('<').rstrip('>').replace('-','_')
            temp_body = ''
            for token in body.split():
                if token in non_terminals:
                    temp_body += f'{token.strip().lstrip('<').rstrip('>').replace('-','_')} '
                else:
                    temp_body += f'{f'"{token}"' if token != 'Î»' else ''} '
            if ebnf_dict.get(head) is None:
                ebnf_dict[head] = [temp_body]
            else:
                ebnf_dict[head].append(temp_body)
        
        ebnf = '%import common.WS\n%ignore WS\n\n'
        for key, value in ebnf_dict.items():
            ebnf += f'{key}: '
            for val in value:
                ebnf += f'{val} | '
            ebnf = ebnf[:-3] + '\n'
        with open("Files/cfg/grammar.lark", "w") as f:
            f.write(ebnf)

    def parse(self, input_string, non_terminals, productions, predict_set):
        stack = ['$']
        stack.append(non_terminals[0])
        input_string = input_string.split() + ['$'] # a = 1 ; $
        index = 0

        while stack:
            top = stack.pop()
            if top == 'Î»': # Skip null
                continue
            if top == input_string[index]: # Match terminal
                index += 1
            elif top in non_terminals:
                for production in productions:
                    head, body = production.split("->")
                    head = head.strip()
                    body = body.strip().split()
                    if head == top and input_string[index] in predict_set[production]:
                        stack += body[::-1]
                        break
                else:
                    return False
            else:
                return False
        return len(input_string) == index

    def start(self):
        non_terminals = []
        productions = []

        print("Starting the parser")

        with open("Files/cfg/cfg.txt", "r") as f:
            lines = f.readlines()

            for line in lines:  # Get all non-terminals and productions
                production = line.split("->")[0].strip()
                if production not in non_terminals:
                    non_terminals.append(production)
                productions.append(line.strip())

        # first_set = self.get_first_set(non_terminals, productions)
        # follow_set = self.get_follow_set(non_terminals, productions, first_set)
        # predict_set = self.get_predict_set(productions, first_set, follow_set)

        # print(f'{"_"*35}FIRST SET{"_"*35}')
        # for set in first_set:
        #     print(f'{set}: {first_set[set]}')

        # print(f'{"_"*35}FOLLOW SET{"_"*35}')
        # for set in follow_set:
        #     print(f'{set}: {follow_set[set]}')

        # print(f'{"_"*35}PREDICT SET{"_"*35}')
        # for set in predict_set:
        #     print(f'{set.replace("Î»", "λ")}: {predict_set[set]}')

        # self.convert_to_ebnf(non_terminals, productions)

        with open("Files/cfg/grammar.lark", "r") as file:
            grammar = file.read()

        parser = Lark(grammar, parser="earley")

        try:
            parse_tree = parser.parse(self._source_code)
            print(parse_tree)
        except Exception as e:
            print(f"Parsing error: {e}")
            print(dir(e))
            self.log = str(e)

        # input_string = "shimenet kween ( ) { anda id = anda_literal ; }"
        # if parse(input_string, non_terminals, productions, predict_set):
        #     print("No Error")
        # else:
        #     print("SYNTAX ERROR")