import pandas as pd

def get_production(line):
    new_line = ''
    bars = 0
    for i in range(len(line)):
        if bars >= 2: new_line += line[i]
        if line[i] == '|':  bars += 1
    
    for i in range(len(new_line)):
        if new_line[i] == '|':
            new_line = new_line[:i] + '->' + new_line[i+7:-2]
            break
    # print(new_line.replace('Î»','λ'))
    return new_line

def conver_to_cfg():
    with open("Files/cfg/cfg.md", "r") as f:
        markdown_content = f.readlines()

    with open("Files/cfg/cfg.txt", "w") as f:
        for line in markdown_content[4:]:
            print(get_production(line.replace('\\', '')))
            f.write(get_production(line.replace('\\', '')) + '\n')

def get_first_set(non_terminals, productions):
    first_set = {nt: set() for nt in non_terminals}

    def first(symbol):
        if symbol not in non_terminals:
            return {symbol}
        if not first_set[symbol]:
            for production in productions:
                if production == '': continue
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

def get_follow_set(non_terminals, productions, first_set):
    follow_set = {nt: set() for nt in non_terminals}
    start_symbol = non_terminals[0]
    follow_set[start_symbol].add('$')

    def follow(symbol):
        print(symbol)
        for production in productions:
            if production == '': continue
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
                                print("Getting follow of next symbol")
                                follow_set[symbol].update(follow(next_sym))
                    else:
                        if head != symbol:
                            print("Getting follow of head")
                            follow_set[symbol].update(follow(head))
        return follow_set[symbol]

    for nt in non_terminals:
        follow(nt)

    return follow_set

def get_predict_set(productions, first_set, follow_set):
    predict_set = {}
    for production in productions:
        if production == '': continue
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

def convert_to_ebnf(non_terminals, productions):
    ebnf_dict = {}
    for production in productions:
        if production == '': continue
        head, body = production.split("->")
        head = head.strip().lstrip('<').rstrip('>').replace('-','_').replace('2', 'two').replace('3', 'three')
        temp_body = ''
        for token in body.split():
            if token in non_terminals:
                temp_body += f'{token.strip().lstrip('<').rstrip('>').replace('-','_').replace('2', 'two').replace('3', 'three')} '
            else:
                temp_body += f'{f'"{token}"' if token != 'Î»' else ''} '
        if ebnf_dict.get(head) is None:
            ebnf_dict[head] = [temp_body]
        else:
            ebnf_dict[head].append(temp_body)
    
    tokens = {
        '+=': 'PLUS_EQUAL',
        '-=': 'MINUS_EQUAL',
        "%=": 'MODULO_EQUAL',
        "/=": 'DIVIDE_EQUAL',
        "//=": 'FLOOR_EQUAL',
        "*=": 'TIMES_EQUAL',
        "**=": 'EXPONENTIATE_EQUAL',
        '**': 'EXPONENTIATE',
        '//': 'FLOOR',
        '>=': 'GREATER_EQUAL',
        '<=': 'LESS_EQUAL',
        '==': 'EQUAL_EQUAL',
        '!=': 'NOT_EQUAL',
        '&&': 'AND',
        '||': 'OR',
        '!': 'NOT',
        '--': 'MINUS_MINUS',
        '++': 'PLUS_PLUS',
        'id': 'ID',
        'anda_literal': 'ANDA_LITERAL',
        'andamhie_literal': 'ANDAMHIE_LITERAL',
        'chika_literal':'CHIKA_LITERAL',
    }
    ebnf = '%import common.WS\n%ignore WS\n\nstart: program\n'
    for key, value in ebnf_dict.items():
        ebnf += f'{key}: '
        for val in value:
            value = val
            for tok in tokens:
                if f'"{tok}"' in val:
                    value = value.replace(f'"{tok}"', tokens[tok])
            ebnf += f'{value} | '
        ebnf = ebnf[:-3] + '\n'
    for key, value in tokens.items():
        if key == 'id': ebnf += f'{value}:' + ' /(?!(eklabool|anda|andamhie|chika|givenchy|serve|pak|ganern|versa|betsung|ditech|forda|keri|lang|amaccana|gogogo|kween|shimenet|push|korik|eme|naur|from|to|step))/ /[a-zA-Z][a-zA-Z0-9_]{0,19}/\n'
        elif key == 'anda_literal': ebnf += f'{value}:' + ' /[0-9]+/\n'
        elif key == 'andamhie_literal': ebnf += f'{value}:' + ' /[0-9]+\\.[0-9]+/\n'
        elif key == 'chika_literal': ebnf += f'{value}:' + ' /"([^"\\\\]|\\\\.)*"/\n'
        else: ebnf += f'{value}: "{key}"\n'
    # ebnf += f'COMMENT: "/^" /(?s).*?(?:\^/|$)/'

    with open("Files/cfg/grammar.lark", "w") as f:
        f.write(ebnf)
    
if __name__ == "__main__":
    conver_to_cfg()

    non_terminals = []
    productions = []

    print("Starting the program")
    with open("Files/cfg/cfg.txt", "r") as f:
        lines = f.readlines()

        for line in lines:  # Get all non-terminals and productions
            production = line.split("->")[0].strip()
            if production not in non_terminals:
                non_terminals.append(production)
            productions.append(line.strip())

    first_set = get_first_set(non_terminals, productions)
    follow_set = get_follow_set(non_terminals, productions, first_set)
    predict_set = get_predict_set(productions, first_set, follow_set)

    print(f'{"_"*35}FIRST SET{"_"*35}')
    for set in first_set:
        print(f'{set}: {first_set[set]}')

    first_set_keys = [f'First({first})' for first in first_set.keys()]
    df = pd.DataFrame({'No.':[i for i in range(1, len(first_set_keys) + 1)],
                                 'Production': first_set_keys,
                                 '':['->' for i in range(1, len(first_set) + 1)],
                                 'First Set': first_set.values()})
    df.to_excel("Files/cfg/first_set.xlsx", index=False)

    print(f'{"_"*35}FOLLOW SET{"_"*35}')
    for set in follow_set:
        print(f'{set}: {follow_set[set]}')
    
    follow_set_keys = [f'Follow({follow})' for follow in follow_set.keys()]
    df = pd.DataFrame({'No.':[i for i in range(1, len(follow_set_keys) + 1)],
                                 'Production': follow_set_keys,
                                 '':['->' for i in range(1, len(first_set) + 1)],
                                 'Follow Set': follow_set.values()})
    df.to_excel("Files/cfg/follow_set.xlsx", index=False)

    print(f'{"_"*35}PREDICT SET{"_"*35}')
    for set in predict_set:
        print(f'{set.replace("Î»", "λ")}: {predict_set[set]}')

    df = pd.DataFrame({'No.':[i for i in range(1, len(predict_set) + 1)],
                                 'Production': predict_set.keys(),
                                 '':['->' for i in range(1, len(predict_set) + 1)],
                                 'Predict Set': predict_set.values()})
    df.to_excel("Files/cfg/predict_set.xlsx", index=False)

    production_column = []
    set_column = []
    for key, value in predict_set.items():
        head, body = key.split("->")
        print('Head is:', head)
        print('Body is:', body)
        if 'Î»' in body:
            print('NULL')
            production_column.append(f'First(λ-λ) U Follow({head})')
            set_column.append(f'Follow({head})')
        else:
            print('NOT NULL')
            prod = ''
            for i in body.split():
                prod += f'{i} '
            prod = prod.rstrip(' ')
            production_column.append(f'First({prod})')
            set_column.append(f'First({body.split()[0]})')

    df = pd.DataFrame({'No.':[i for i in range(1, len(predict_set) + 1)],
                                 'Production': production_column,
                                 'set': set_column,
                                 'Predict Set': predict_set.values()})
    df.to_excel("Files/cfg/predict_set_docu.xlsx", index=False)

    convert_to_ebnf(non_terminals, productions)