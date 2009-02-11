
def store(data):
    try:
        x = repr(data)
        exec x
        return x
    except:
        raise ValueError("%s is not suitable for storage"%data)

def load(data):
    if not data:
        return ""
    try:
        exec "val = " + data
        return val
    except:
        raise ValueError("%s is not a valid stored string"%data)

load(store("Welcome!"))
