import sys

class _RangeError(Exception): pass

def get_string(message, name="string", default=None, minimum_length=0, maximum_length=80, force_lower=False):
    """
    Funkcja pobierajaca i walidujaca z konsoli ciag tekstu
    """
    message += ": " if default is None else " [%s]: " % (default)
    while True:
        try:
            line = raw_input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("%s nie moze byc pusta" % (name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("%s musi miec co najmniej %s i najwyzej %s znakow" % (name, minimum_length, maximum_length))
            return line if not force_lower else line.lower()
        except ValueError, err:
            print(err)


def get_integer(message, name="integer", default=None, minimum=None, maximum=None, allow_zero=True):
    """
    Funkcja pobierajaca i walidujaca z konsoli liczbe
    """    
    message += ": " if default is None else " [%d]: " % (default)
    while True:
        try:
            line = raw_input(message)
            if not line and default is not None:
                return default
            x = int(line)
            if x == 0:
                if allow_zero:
                    return x
                else:
                    raise _RangeError("%s nie moze byc rowne 0" % (name))
            if ((minimum is not None and minimum > x) or
                (maximum is not None and maximum < x)):
                raise _RangeError("%s musi byc pomiedzy %s i %s lacznie z %s" % (name, minimum, maximum, (" 0" if allow_zero else "")))
            return x
        except _RangeError, err:
            print(err)
        except ValueError, err:
            print("%s musi byc typu calkowitego" % (name))
