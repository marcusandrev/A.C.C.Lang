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
                integer_part, fractional_part = lexeme.split('.')
                # Strip leading zeroes from the integer part
                integer_part = integer_part.lstrip('0') or '0'
                # Clamp the integer part to a maximum of 10 digits
                if len(integer_part) > 10:
                    integer_part = '9999999999'
                # Truncate the fractional part to a maximum of 6 digits
                fractional_part = fractional_part[:6]
                # Strip trailing zeroes from the fractional part
                if fractional_part.rstrip('0') == '':
                    fractional_part = '0'
                else:
                    fractional_part = fractional_part.rstrip('0')
                lexeme = integer_part + ('.' + fractional_part if fractional_part else '')
                token_stream.append((lexeme, 'andamhie_literal'))
            else:
                # Strip leading zeroes from the integer part
                lexeme = lexeme.lstrip('0') or '0'
                # Clamp the integer part to a maximum of 10 digits
                if len(lexeme) > 10:
                    lexeme = '9999999999'
                token_stream.append((lexeme, 'anda_literal'))
            continue
        
        if lexeme[0] == '"':
            token_stream.append((lexeme, "chika_literal"))
            continue

        if lexeme[:2] == '/^':
            token_stream.append((lexeme, "comment"))
            continue
        
        token = id_map.get(lexeme, f"id_{len(id_map) + 1}")
        id_map[lexeme] = token
        token_stream.append((lexeme, token))

    if token_stream and token_stream[-1][1] == 'newline':
        token_stream.pop()

    return token_stream
