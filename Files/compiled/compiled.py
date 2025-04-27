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

def _kween():
    _input = _cType_('chika', input('Enter a string: '))
    _name = None
    _name = _cType_('chika', input('Enter a string: '))
    print(_cType_('anda', (_cNone_(_input, 'input') + _cNone_(_name, 'name'))), end='')

if __name__ == '__main__':
    _kween()
