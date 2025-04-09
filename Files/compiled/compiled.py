def truncate_andamhie(value):
    import math
    return math.trunc(value * 1000000) / 1000000

def check_type_acclang_specific(expected, value):
    if expected == 'anda':
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except ValueError:
                raise TypeError("Type error: expected numeric value for type 'anda'")
    elif expected == 'andamhie':
        try:
            f = float(value)
            import math
            return math.trunc(f * 1000000) / 1000000
        except ValueError:
            try:
                f = float(int(value))
                import math
                return math.trunc(f * 1000000) / 1000000
            except ValueError:
                raise TypeError("Type error: expected numeric value for type 'andamhie'")
    elif expected == 'eklabool':
        try:
            return False if int(value) == 0 else True
        except ValueError:
            try:
                return False if float(value) == 0.0 else True
            except ValueError:
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

def check_array_type_acclang_specific(expected, arr):
    if isinstance(arr, list):
        return [check_array_type_acclang_specific(expected, x) for x in arr]
    else:
        return check_type_acclang_specific(expected, arr)

def kween():
    x = check_type_acclang_specific('andamhie', 1.000005)
    y = check_type_acclang_specific('andamhie', input('Enter a decimal value: '))
    print(truncate_andamhie((x + y)))

if __name__ == '__main__':
    kween()
