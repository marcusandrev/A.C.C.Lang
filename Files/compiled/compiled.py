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

def _kween():
    _n1 = None
    _n2 = None
    _n3 = None
    _n4 = None
    _n5 = None
    _choice = None
    _temp = None
    print("Enter 5 numbers:\n", end='')
    _n1 = _cType_('anda', input('Number 1: '))
    _n2 = _cType_('anda', input('Number 2: '))
    _n3 = _cType_('anda', input('Number 3: '))
    _n4 = _cType_('anda', input('Number 4: '))
    _n5 = _cType_('anda', input('Number 5: '))
    _choice = _cType_('anda', input('\nChoose sorting order (1=Ascending, 2=Descending): '))
    if (_cNoArray_(_cNone_(_choice, 'choice'), '==') == _cNoArray_(1, '==')):
        if (_cNoArray_(_cNone_(_n1, 'n1'), '>') > _cNoArray_(_cNone_(_n2, 'n2'), '>')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '>') > _cNoArray_(_cNone_(_n3, 'n3'), '>')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '>') > _cNoArray_(_cNone_(_n4, 'n4'), '>')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '>') > _cNoArray_(_cNone_(_n5, 'n5'), '>')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '>') > _cNoArray_(_cNone_(_n3, 'n3'), '>')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '>') > _cNoArray_(_cNone_(_n4, 'n4'), '>')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '>') > _cNoArray_(_cNone_(_n5, 'n5'), '>')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n3, 'n3'), '>') > _cNoArray_(_cNone_(_n4, 'n4'), '>')):
            _temp = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n3, 'n3'), '>') > _cNoArray_(_cNone_(_n5, 'n5'), '>')):
            _temp = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n4, 'n4'), '>') > _cNoArray_(_cNone_(_n5, 'n5'), '>')):
            _temp = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        print("\nSorted in ascending order: ", end='')
        print(_cNone_(_n1, 'n1'), end='')
        print(" ", end='')
        print(_cNone_(_n2, 'n2'), end='')
        print(" ", end='')
        print(_cNone_(_n3, 'n3'), end='')
        print(" ", end='')
        print(_cNone_(_n4, 'n4'), end='')
        print(" ", end='')
        print(_cNone_(_n5, 'n5'), end='')
        print("\n", end='')
    elif (_cNoArray_(_cNone_(_choice, 'choice'), '==') == _cNoArray_(2, '==')):
        if (_cNoArray_(_cNone_(_n1, 'n1'), '<') < _cNoArray_(_cNone_(_n2, 'n2'), '<')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '<') < _cNoArray_(_cNone_(_n3, 'n3'), '<')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '<') < _cNoArray_(_cNone_(_n4, 'n4'), '<')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n1, 'n1'), '<') < _cNoArray_(_cNone_(_n5, 'n5'), '<')):
            _temp = _cType_('anda', _cNone_(_n1, 'n1'))
            _n1 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '<') < _cNoArray_(_cNone_(_n3, 'n3'), '<')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '<') < _cNoArray_(_cNone_(_n4, 'n4'), '<')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n2, 'n2'), '<') < _cNoArray_(_cNone_(_n5, 'n5'), '<')):
            _temp = _cType_('anda', _cNone_(_n2, 'n2'))
            _n2 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n3, 'n3'), '<') < _cNoArray_(_cNone_(_n4, 'n4'), '<')):
            _temp = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n3, 'n3'), '<') < _cNoArray_(_cNone_(_n5, 'n5'), '<')):
            _temp = _cType_('anda', _cNone_(_n3, 'n3'))
            _n3 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        if (_cNoArray_(_cNone_(_n4, 'n4'), '<') < _cNoArray_(_cNone_(_n5, 'n5'), '<')):
            _temp = _cType_('anda', _cNone_(_n4, 'n4'))
            _n4 = _cType_('anda', _cNone_(_n5, 'n5'))
            _n5 = _cType_('anda', _cNone_(_temp, 'temp'))
        print("\nSorted in descending order: ", end='')
        print(_cNone_(_n1, 'n1'), end='')
        print(" ", end='')
        print(_cNone_(_n2, 'n2'), end='')
        print(" ", end='')
        print(_cNone_(_n3, 'n3'), end='')
        print(" ", end='')
        print(_cNone_(_n4, 'n4'), end='')
        print(" ", end='')
        print(_cNone_(_n5, 'n5'), end='')
        print("\n", end='')
    else:
        print("\nInvalid choice.\n", end='')

if __name__ == '__main__':
    _kween()
