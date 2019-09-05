def TupleDownTo(t, depth=0):
    if depth == 0:
        return type(t) is tuple
    elif type(t) is tuple:
        return TupleDownTo(t[0], depth - 1)
    else:
        return False

def MakeTuple(t, depth=0):
    return t if TupleDownTo(t, depth) else (t, )

def StartsWith(s, b):
    if len(b) > len(s):
        return False
    return s[:len(b)] == b
