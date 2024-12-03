# This file is used to define the tokens of acclang

reserved = {
    'amaccana','anda','andamhie',
    'betsung',
    'chika',
    'ditech',
    'eklabool', 'eme',
    'forda', 'from',
    'ganern', 'givenchy', 'gogogo',
    'keri', 'korik', 'kween',
    'lang',
    'naur',
    'pak', 'push',
    'serve', 'shimenet', 'step',
    'to',
    'versa',
    'wiz',
    '+', '++', '+=',
    '-', '--', '-=',
    '*', '*=', '**', '**=',
    '/', '/=', '//', '//=',
    '%', '%=',
    '=', '==',
    '!', '!=',
    '<', '<=',
    '>', '>=',
    '&&',
    '||',
    ',',
    '.',
    ';',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
}

def tokenize(lexemes: list[str]):
    token_stream = []
    id_map = {}
    for lexeme in lexemes:
        if lexeme == ' ':
            token_stream.append((lexeme, 'whitespace'))
            continue
        
        if lexeme == r'\n':
            token_stream.append((lexeme, 'newline'))
            continue

        if lexeme in reserved:
            token_stream.append((lexeme, lexeme))
            continue

        if lexeme.replace('.', '', 1).isdigit():
            if '.' in lexeme:
                token_stream.append((lexeme, 'andamhie_literal'))
            else:
                token_stream.append((lexeme, 'anda_literal'))
            continue
        
        token = id_map.get(lexeme, f"id_{len(id_map) + 1}")
        id_map[lexeme] = token
        token_stream.append((lexeme, token))

    if token_stream and token_stream[-1][1] == 'newline':
        token_stream.pop()

    return token_stream
