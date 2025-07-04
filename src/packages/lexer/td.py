from constants import ATOMS,DELIMS

class State:
    def __init__(self, chars: list[str], branches: list[int] = [], end = False):
        self.chars = [chars] if type(chars) is str else chars
        self.branches = [branches] if type(branches) is int else branches
        self.isEnd = end

STATES = {
    0: State('initial', [1, 27, 35, 41, 48, 60, 70, 91, 106, 114, 119, 127, 145, 148, 154, 160, 166, 174, 182, 186, 190, 194, 198, 202, 205, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 266, 299]),
    1: State('a', [2, 10, 19]), 2: State('m', 3), 3: State('a', 4), 4: State('c', 5), 5: State('c', 6), 6: State('a', 7), 7: State('n', 8), 8: State('a', 9), 9: State(DELIMS['amaccana_gogogo_delim'], end = True),
                            10: State('n', 11), 11: State('d', 12), 12: State('a', [13, 14]), 13: State(ATOMS['similar_delim'], end = True),
                                                                                              14: State('m', 15), 15: State('h', 16), 16: State('i', 17), 17: State('e', 18), 18: State(ATOMS['similar_delim'], end = True),
                            19: State('d', 20), 20: State('e', 21), 21: State('l', 22), 22: State('e', [23, 24]), 23: State(DELIMS['control_flow_delim'], end = True),
                                                                                                            24: State('t', 25), 25: State('e', 26), 26: State(DELIMS['control_flow_delim'], end = True),
    27: State('b', 28), 28: State('e', 29), 29: State('t', 30), 30: State('s', 31), 31: State('u', 32), 32: State('n', 33), 33: State('g', 34), 34: State(ATOMS['similar_delim'], end = True),
    35: State('c', 36), 36: State('h', 37), 37: State('i', 38), 38: State('k', 39), 39: State('a', 40), 40: State(ATOMS['similar_delim'], end = True),
    41: State('d', 42), 42: State('i', 43), 43: State('t', 44), 44: State('e', 45), 45: State('c', 46), 46: State('h', 47), 47: State(DELIMS['ditech_delim'],),

    48: State('e', [49, 57]), 49: State('k', 50), 50: State('l', 51), 51: State('a', 52), 52: State('b', 53), 53: State('o', 54), 54: State('o', 55), 55: State('l', 56), 56: State(ATOMS['similar_delim'], end = True),
                              57: State('m', 58), 58: State('e', 59), 59: State(DELIMS['bool_delim'], end = True),
    60: State('f', [61, 66]), 61: State('o', 62), 62: State('r', 63), 63: State('d', 64), 64: State('a', 65), 65: State(DELIMS['control_flow_delim'], end = True),
                              66: State('r', 67), 67: State('o', 68), 68: State('m', 69), 69: State(ATOMS['similar_delim'], end = True),
    70: State('g', [71, 77, 85]), 71: State('a', 72), 72: State('n', 73), 73: State('e', 74), 74: State('r', 75), 75: State('n', 76), 76: State(DELIMS['kerilang_ganern_delim'], end = True),
                                  77: State('i', 78), 78: State('v', 79), 79: State('e', 80), 80: State('n', 81), 81: State('c', 82), 82: State('h', 83), 83: State('y', 84), 84: State(DELIMS['control_flow_delim'], end = True),
                                  85: State('o', 86), 86: State('g', 87), 87: State('o', 88), 88: State('g', 89), 89: State('o', 90), 90: State(DELIMS['amaccana_gogogo_delim'], end = True),
    91: State('k', [92, 96, 101]), 92: State('e', 93), 93: State('r', 94), 94: State('i', 95), 95: State(DELIMS['control_flow_delim'], end = True),
                                   96: State('o', 97), 97: State('r', 98), 98: State('i', 99), 99: State('k', 100), 100: State(DELIMS['bool_delim'], end = True),
                                  101: State('w', 102), 102: State('e', 103), 103: State('e', 104), 104: State('n', 105), 105: State(DELIMS['control_flow_delim'], end = True),
   106: State('l', [107]), 107: State('a', 108), 108: State('n', 109), 109: State('g', 110), 110: State(DELIMS['kerilang_ganern_delim'], end = True),
                         111: State('e', 112), 112: State('n', 113), 113: State(DELIMS['control_flow_delim'], end = True),



    114: State('n', 115), 115: State('a', 116), 116: State('u', 117), 117: State('r', 118), 118: State(ATOMS['similar_delim'], end = True),
    119: State('p', [120, 123]), 120: State('a', 121), 121: State('k', 122), 122: State(DELIMS['control_flow_delim'], end = True),
                                    123: State('u', 124), 124: State('s', 125), 125: State('h', 126), 126: State(DELIMS['push_delim'], end = True),
    127: State('s', [128, 133, 141]), 128: State('e', 129), 129: State('r', 130), 130: State('v', 131), 131: State('e', 132), 132: State(DELIMS['control_flow_delim'], end = True),
                                        133: State('h', 134), 134: State('i', 135), 135: State('m', 136), 136: State('e', 137), 137: State('n', 138), 138: State('e', 139), 139: State('t', 140), 140: State(ATOMS['similar_delim'], end = True),
                                        141: State('t', 142), 142: State('e', 143), 143: State('p', 144), 144: State(ATOMS['similar_delim'], end = True),
    145: State('t', 146), 146: State('o', 147), 147: State(ATOMS['similar_delim'], end = True),
    148: State('v', 149), 149: State('e', 150), 150: State('r', 151), 151: State('s', 152), 152: State('a', 153), 153: State(DELIMS['control_flow_delim'], end = True),

    154: State('+', [156, 158, 155]), 155: State(DELIMS['plus_and_or_delim'], end = True),
                                        156: State('+', 157), 157: State(DELIMS['unary_delim'], end = True),
                                        158: State('=', 159), 159: State(DELIMS['most_symbol_delim'], end = True),
    160: State('-', [162, 164, 161]), 161: State(DELIMS['minus_delim'], end = True),
                                        162: State('-', 163), 163: State(DELIMS['unary_delim'], end = True),
                                        164: State('=', 165), 165: State(DELIMS['most_symbol_delim'], end = True),
    166: State('*', [168, 170, 167]), 167: State(DELIMS['most_symbol_delim'], end = True),
                                        168: State('=', 169), 169: State(DELIMS['most_symbol_delim'], end = True),
                                        170: State('*', [171, 172]), 171: State(DELIMS['most_symbol_delim'], end = True),
                                                                        172: State('=', 173), 173: State(DELIMS['most_symbol_delim'], end = True),
    174: State('/', [176, 178, 305, 175]), 175: State(DELIMS['most_symbol_delim'], end = True),
                                            176: State('=', 177), 177: State(DELIMS['most_symbol_delim'], end = True),
                                            178: State('/', [179, 180]), 179: State(DELIMS['most_symbol_delim'], end = True),
                                                                            180: State('=', 181), 181: State(DELIMS['most_symbol_delim'], end = True),
    182: State('%', [184, 183]), 183: State(DELIMS['most_symbol_delim'], end = True),
                                    184: State('=', 185), 185: State(DELIMS['most_symbol_delim'], end = True),
    186: State('=', [188, 187]), 187: State(DELIMS['equal_comma_delim'], end = True),
                                    188: State('=', 189), 189: State(DELIMS['logical_not_delim'], end = True),
    190: State('!', [192, 191]), 191: State(DELIMS['logical_not_delim'], end = True),
                                    192: State('=', 193), 193: State(DELIMS['logical_not_delim'], end = True),
    194: State('<', [196, 195]), 195: State(DELIMS['most_symbol_delim'], end = True),
                                    196: State('=', 197), 197: State(DELIMS['most_symbol_delim'], end = True),
    198: State('>', [200, 199]), 199: State(DELIMS['most_symbol_delim'], end = True),
                                    200: State('=', 201), 201: State(DELIMS['most_symbol_delim'], end = True),
    202: State('&', 203), 203: State('&', 204), 204: State(DELIMS['plus_and_or_delim'], end = True),
    205: State('|', 206), 206: State('|', 207), 207: State(DELIMS['plus_and_or_delim'], end = True),
    208: State(',', 209), 209: State(DELIMS['equal_comma_delim'], end = True),
    210: State(';', 211), 211: State(DELIMS['terminator_delim'], end = True),
    212: State('(', 213), 213: State(DELIMS['open_parenthesis_delim'], end = True),
    214: State(')', 215), 215: State(DELIMS['close_parenthesis_delim'], end = True),
    216: State('[', 217), 217: State(DELIMS['open_bracket_delim'], end = True),
    218: State(']', 219), 219: State(DELIMS['close_bracket_delim'], end = True),
    220: State('{', 221), 221: State(DELIMS['open_brace_delim'], end = True),
    222: State('}', 223), 223: State(DELIMS['close_brace_delim'], end = True),
    224: State(':', 225), 225: State(ATOMS['similar_delim'], end = True),
    226: State([*ATOMS['alphabet']], [228, 227]), 227: State(DELIMS['id_delim'], end = True),
        228: State([*ATOMS['alphanumeric'], '_'], [230, 229]), 229: State(DELIMS['id_delim'], end = True),
            230: State([*ATOMS['alphanumeric'], '_'], [232, 231]), 231: State(DELIMS['id_delim'], end = True),
                232: State([*ATOMS['alphanumeric'], '_'], [234, 233]), 233: State(DELIMS['id_delim'], end = True),
                    234: State([*ATOMS['alphanumeric'], '_'], [236, 235]), 235: State(DELIMS['id_delim'], end = True),
                        236: State([*ATOMS['alphanumeric'], '_'], [238, 237]), 237: State(DELIMS['id_delim'], end = True),
                            238: State([*ATOMS['alphanumeric'], '_'], [240, 239]), 239: State(DELIMS['id_delim'], end = True),
                                240: State([*ATOMS['alphanumeric'], '_'], [242, 241]), 241: State(DELIMS['id_delim'], end = True),
                                    242: State([*ATOMS['alphanumeric'], '_'], [244, 243]), 243: State(DELIMS['id_delim'], end = True),
                                        244: State([*ATOMS['alphanumeric'], '_'], [246, 245]), 245: State(DELIMS['id_delim'], end = True),
                                            246: State([*ATOMS['alphanumeric'], '_'], [248, 247]), 247: State(DELIMS['id_delim'], end = True),
                                                248: State([*ATOMS['alphanumeric'], '_'], [250, 249]), 249: State(DELIMS['id_delim'], end = True),
                                                    250: State([*ATOMS['alphanumeric'], '_'], [252, 251]), 251: State(DELIMS['id_delim'], end = True),
                                                        252: State([*ATOMS['alphanumeric'], '_'], [254]), 253: State(DELIMS['id_delim'], end = True),
                                                            254: State([*ATOMS['alphanumeric'], '_'], [256, 255]), 255: State(DELIMS['id_delim'], end = True),
                                                                256: State([*ATOMS['alphanumeric'], '_'], [258, 257]), 257: State(DELIMS['id_delim'], end = True),
                                                                    258: State([*ATOMS['alphanumeric'], '_'], [260, 259]), 259: State(DELIMS['id_delim'], end = True),
                                                                        260: State([*ATOMS['alphanumeric'], '_'], [262, 261]), 261: State(DELIMS['id_delim'], end = True),                                                                                                                                                        
                                                                            262: State([*ATOMS['alphanumeric'], '_'], [264, 263]), 263: State(DELIMS['id_delim'], end = True),
                                                                                264: State([*ATOMS['alphanumeric'], '_'], [265]), 265: State(DELIMS['id_delim'], end = True),

    266: State(ATOMS['digit'], [268, 286, 267]), 267: State(DELIMS['int_float_delim'], end = True),
        268: State(ATOMS['digit'], [270, 286, 269]), 269: State(DELIMS['int_float_delim'], end = True),
            270: State(ATOMS['digit'], [272, 286, 271]), 271: State(DELIMS['int_float_delim'], end = True),
                272: State(ATOMS['digit'], [274, 286, 273]), 273: State(DELIMS['int_float_delim'], end = True),
                    274: State(ATOMS['digit'], [276, 286, 275]), 275: State(DELIMS['int_float_delim'], end = True),
                        276: State(ATOMS['digit'], [278, 286, 277]), 277: State(DELIMS['int_float_delim'], end = True),
                            278: State(ATOMS['digit'], [280, 286, 279]), 279: State(DELIMS['int_float_delim'], end = True),
                                280: State(ATOMS['digit'], [282, 286, 281]), 281: State(DELIMS['int_float_delim'], end = True),
                                    282: State(ATOMS['digit'], [284, 286, 283]), 283: State(DELIMS['int_float_delim'], end = True),
                                        284: State(ATOMS['digit'], [286, 285]), 285: State(DELIMS['int_float_delim'], end = True),
        286: State('.', 287),
            287: State(ATOMS['digit'], [289, 288]), 288: State(DELIMS['int_float_delim'], end = True),
                289: State(ATOMS['digit'], [291, 290]), 290: State(DELIMS['int_float_delim'], end = True),
                    291: State(ATOMS['digit'], [293, 292]), 292: State(DELIMS['int_float_delim'], end = True),
                        293: State(ATOMS['digit'], [295, 294]), 294: State(DELIMS['int_float_delim'], end = True),
                            295: State(ATOMS['digit'], [297, 296]), 296: State(DELIMS['int_float_delim'], end = True),
                               297: State(ATOMS['digit'], [298]), 298: State(DELIMS['int_float_delim'], end = True),
            
    299: State('"', [300, 301, 303]), 300: State(ATOMS['ascii_300'], [300, 301, 303]), 301: State('"', 302), 302: State(DELIMS['string_delim'], end = True),
                                    303: State('\\', 304), 304: State(ATOMS['ascii'], [300, 301, 302, 303]),

    305: State('^', [306, 309]), 306: State('^', [306, 307, 309]), 307: State('/', 308), 308: State(ATOMS['ascii'], end = True),
    309: State(ATOMS['ascii_309'], [306, 309])
}