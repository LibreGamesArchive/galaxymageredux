

class ReturnVals(object):
    def __init__(self):
        pass

def load(path, access={}):
##    try:
##        ret_val = ReturnVals()
##        eval(compile(open(path, 'rU').read(), '<%s>'%path, 'exec'),
##             access, {'store':ret_val})
##        return ret_val
##    except:
##        print 'exec mod <%s> failed!' % path
##        return False

    ret_val = ReturnVals()
    eval(compile(open(path, 'rU').read(), '<%s>'%path, 'exec'),
         access, {'store':ret_val})
    return ret_val
