def TupleDownTo(t, depth=0):
    if depth == 0:
        return type(t) is tuple
    elif type(t) is tuple:
        return TupleDownTo(t[0], depth - 1)
    else:
        return False

def MakeTuple(t, depth=0):
    return t if TupleDownTo(t, depth) else (t, )

# Returns None if string s doesn't start with any of the strings in tuple b
# Otherwise, returns the index after the match
def StartsWith(s, b):
    b = MakeTuple(b)
    for bb in b:
        if len(bb) <= len(s) and s[:len(bb)] == bb:
            return len(bb)
    return None
