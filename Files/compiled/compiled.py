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
            raise OverflowError("Overflow error: value exceeds maximum for type 'anda'")
        if v < -9999999999:
            raise OverflowError("Overflow error: value exceeds minimum for type 'anda'")
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
            raise OverflowError("Overflow error: value exceeds maximum for type 'andamhie'")
        if f < -9999999999:
            raise OverflowError("Overflow error: value exceeds minimum for type 'andamhie'")
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

def _cEnsureArray_(value, name):
    if not isinstance(value, list):
        raise TypeError(f"Runtime error: cannot append to non-array '{name}'")
    return value

def _myFunc(_msgs):
    _start_val_0 = 0
    _end_val_0 = _cType_('anda', (_cNoArray_(_cType_('anda', len(_cNone_(_msgs, 'msgs'))), '-') - _cNoArray_(1, '-')))
    _step_val_0 = 1
    if _step_val_0 > 0:
        _end_bound_0 = _end_val_0 + 1
    else:
        _end_bound_0 = _end_val_0 - 1
    for _i in range(_start_val_0, _end_bound_0, _step_val_0):
        print((str(_cNoArray_(_cNone_(_msgs, 'msgs')[_cNone_(_i, 'i')], '+')) + _cNoArray_("\n", '+')), end='')

def _kween():
    _myFunc(["Hello", "World!"])

if __name__ == '__main__':
    try:
        _kween()
    except Exception as e:
        print()
        print(e)
