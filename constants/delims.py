from .atoms import ATOMS

DELIMS = {
    'amaccana_gogogo_delim': {';', *ATOMS['similar_delim']},
    'close_brace_delim': {';', ',', ')', '}', *ATOMS['alphabet'], *ATOMS['similar_delim']},
    'close_bracket_delim': {';', ',', *ATOMS['general_operators'], ')', '[', ']', '}', *ATOMS['similar_delim']},
    'close_parenthesis_delim': {';', ',', *ATOMS['general_operators'], ')', '[', ']', '{', '}', *ATOMS['similar_delim']},
    'control_flow_delim': {'(', *ATOMS['similar_delim']},
    'ditech_delim': {':', *ATOMS['similar_delim']},
    'bool_delim': {';', ',', '=', '!', '&', '|', ')', '}', *ATOMS['similar_delim']},
    'equal_comma_delim': {'"', '-', '!', '(', '{', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'id_delim': {';', ',', *ATOMS['general_operators'], '(', ')', '[', ']', '}', *ATOMS['similar_delim']},
    'int_float_delim': {';', ",", *ATOMS['arithmetic_operators'], '=', '!', ')', ']', '}', *ATOMS['similar_delim']},
    'kerilang_ganern_delim': {'{', *ATOMS['similar_delim']},
    'logical_not_delim': {'"', '-', '!', '(', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'minus_delim': {'(', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'most_symbol_delim': {'-', '(', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'open_brace_delim': {'"', '-', '!', '(', '}', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'open_bracket_delim': {'-', '(', ']', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'open_parenthesis_delim': {'"', '+', '-', '!', '(', ')', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'plus_and_or_delim': {'"', '-', '(', *ATOMS['alphanumeric'], *ATOMS['similar_delim']},
    'string_delim': {';', ',', '+', '=', '!', ')', '}', *ATOMS['similar_delim']},
    'terminator_delim': {*ATOMS['alphabet'], *ATOMS['similar_delim']},
    'unary_delim': {';', *ATOMS['general_operators'], ')', *ATOMS['alphabet'], *ATOMS['similar_delim']},
    'wiz_delim': {';', ',', '=', '!', ')', ']', '}', *ATOMS['similar_delim']}
}