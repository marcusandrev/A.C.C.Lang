def check_type_acclang_compiler_specific(expected, value):
    if expected == 'anda':
        try:
            return int(value)
        except ValueError:
            return int(float(value))
        except ValueError:
            raise TypeError("Type error: expected numeric value for type 'anda'")
    elif expected == 'andamhie':
        try:
            return float(value)
        except ValueError:
            return float(int(value))
        except ValueError:
            raise TypeError("Type error: expected numeric value for type 'andamhie'")
    elif expected == 'eklabool':
        try:
            value = int(value)
            return False if value == 0 else True
        except ValueError:
            value = float(value)
            return False if value == 0.0 else True
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
def kween():
    print(((True or False) + 5))

if __name__ == '__main__':
    kween()