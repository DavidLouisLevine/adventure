def MakeTuple(t):
    return t if type(t) is tuple else (t, )

def StartsWith(s, b):
    if len(b) > len(s):
        return False
    return s[:len(b)] == b
