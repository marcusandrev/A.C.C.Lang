def _cNoArray_(value, op):
    if isinstance(value, list):
        raise TypeError(f"Runtime error: array value used with operator {op}")
    return value

def _cNone_(value, name):
    if value is None:
        raise NameError(f"Runtime error: variable '{name}' used before initialization")
    return value

def _cType_(expected, value):
    if expected == 'anda':
        try:
            v = int(value)
        except Exception:
            try:
                v = int(float(value))
            except Exception:
                raise TypeError("Type error: expected numeric value for type 'anda'")
        if v > 9999999999:
            v = 9999999999
        if v < -9999999999:
            v = -9999999999
        return v
    elif expected == 'andamhie':
        try:
            f = float(value)
        except Exception:
            try:
                f = float(int(value))
            except Exception:
                raise TypeError("Type error: expected numeric value for type 'andamhie'")
        import math
        f = math.trunc(f * 1000000) / 1000000
        if f > 9999999999.999999:
            f = 9999999999.999999
        if f < -9999999999:
            f = -9999999999.999999
        return f
    elif expected == 'eklabool':
        try:
            return False if int(value) == 0 else True
        except Exception:
            try:
                return False if float(value) == 0.0 else True
            except Exception:
                if isinstance(value, str):
                    return True
                else:
                    raise TypeError("Type error: expected numeric or string value for type 'eklabool'")
    elif expected == 'chika':
        if isinstance(value, str):
            return value
        else:
            raise TypeError("Type error: expected string value for type 'chika'")
    else:
        return value

def _cArray_(expected, arr):
    if isinstance(arr, list):
        return [_cArray_(expected, x) for x in arr]
    else:
        return _cType_(expected, arr)

def _cSameElemType_(expected, actual):
    if expected != actual:
        raise TypeError(
            f"Type mismatch in adele(): target list holds {expected} "
            f"but value is list[{actual}]"
        )

def _string_permutations(_input_string):
    _permutations = _cArray_('chika', [_cNone_(_input_string, 'input_string')[0]])
    print(_cNone_(_permutations, 'permutations'), end='')
    _start_val_0 = 1
    _end_val_0 = _cType_('anda', (_cNoArray_(_cType_('anda', len(_cNone_(_input_string, 'input_string'))), '-') - _cNoArray_(1, '-')))
    _step_val_0 = 1
    if _step_val_0 > 0:
        _end_bound_0 = _end_val_0 + 1
    else:
        _end_bound_0 = _end_val_0 - 1
    for _i in range(_start_val_0, _end_bound_0, _step_val_0):
        _char_to_inser = _cType_('chika', _cNone_(_input_string, 'input_string')[_cNone_(_i, 'i')])
        _new_permutations = []
        print((_cNoArray_("\nInserting character: ", '+') + _cNoArray_(_cNone_(_char_to_inser, 'char_to_inser'), '+')), end='')
        _start_val_1 = 0
        _end_val_1 = _cType_('anda', (_cNoArray_(_cType_('anda', len(_cNone_(_permutations, 'permutations'))), '-') - _cNoArray_(1, '-')))
        _step_val_1 = 1
        if _step_val_1 > 0:
            _end_bound_1 = _end_val_1 + 1
        else:
            _end_bound_1 = _end_val_1 - 1
        for _j in range(_start_val_1, _end_bound_1, _step_val_1):
            _perm = _cType_('chika', _cNone_(_permutations, 'permutations')[_cNone_(_j, 'j')])
            print((_cNoArray_("\n   Processing permutation: ", '+') + _cNoArray_(_cNone_(_perm, 'perm'), '+')), end='')
            _start_val_2 = 0
            _end_val_2 = _cType_('anda', len(_cNone_(_perm, 'perm')))
            _step_val_2 = 1
            if _step_val_2 > 0:
                _end_bound_2 = _end_val_2 + 1
            else:
                _end_bound_2 = _end_val_2 - 1
            for _k in range(_start_val_2, _end_bound_2, _step_val_2):
                _new_perm = _cType_('chika', "")
                _start_val_3 = 0
                _end_val_3 = _cType_('anda', (_cNoArray_(_cNone_(_k, 'k'), '-') - _cNoArray_(1, '-')))
                _step_val_3 = 1
                if _step_val_3 > 0:
                    _end_bound_3 = _end_val_3 + 1
                else:
                    _end_bound_3 = _end_val_3 - 1
                for _l in range(_start_val_3, _end_bound_3, _step_val_3):
                    _new_perm = _cType_('chika', _new_perm + _cType_('chika', _cNone_(_perm, 'perm')[_cNone_(_l, 'l')]))
                _new_perm = _cType_('chika', _new_perm + _cType_('chika', _cNone_(_char_to_inser, 'char_to_inser')))
                _start_val_4 = _cNone_(_k, 'k')
                _end_val_4 = _cType_('anda', (_cNoArray_(_cType_('anda', len(_cNone_(_perm, 'perm'))), '-') - _cNoArray_(1, '-')))
                _step_val_4 = 1
                if _step_val_4 > 0:
                    _end_bound_4 = _end_val_4 + 1
                else:
                    _end_bound_4 = _end_val_4 - 1
                for _l in range(_start_val_4, _end_bound_4, _step_val_4):
                    _new_perm = _cType_('chika', _new_perm + _cType_('chika', _cNone_(_perm, 'perm')[_cNone_(_l, 'l')]))
                _new_permutations.append(_cType_('chika', _cNone_(_new_perm, 'new_perm')))
                print((_cNoArray_((_cNoArray_((_cNoArray_("\n    Inserted at index ", '+') + str(_cNoArray_(_cNone_(_k, 'k'), '+'))), '+') + _cNoArray_(": ", '+')), '+') + _cNoArray_(_cNone_(_new_perm, 'new_perm'), '+')), end='')
        _permutations = _cArray_('chika', _cNone_(_new_permutations, 'new_permutations'))
        print("\n  Current permutations: ", end='')
        print(_cNone_(_permutations, 'permutations'), end='')
        print("\n", end='')
    print("\nAll permutations:\n", end='')
    print(_cNone_(_permutations, 'permutations'), end='')
    _start_val_5 = 0
    _end_val_5 = _cType_('anda', (_cNoArray_(_cType_('anda', len(_cNone_(_permutations, 'permutations'))), '-') - _cNoArray_(1, '-')))
    _step_val_5 = 1
    if _step_val_5 > 0:
        _end_bound_5 = _end_val_5 + 1
    else:
        _end_bound_5 = _end_val_5 - 1
    for _x in range(_start_val_5, _end_bound_5, _step_val_5):
        print((str(_cNoArray_(_cNone_(_permutations, 'permutations')[_cNone_(_x, 'x')], '+')) + _cNoArray_("\n", '+')), end='')

def _kween():
    _my_string = _cType_('chika', input('Enter a string: '))
    _string_permutations(_cNone_(_my_string, 'my_string'))

if __name__ == '__main__':
    _kween()
