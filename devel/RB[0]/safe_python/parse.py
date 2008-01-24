def test_safe(filename, acceptable_functions=[]):
    """tests all the function calls in a file against a set of acceptable ones.
       this function also does not allow importing of other modules.
       returns True, [] if there are only acceptable function calls,
       returns False and a list of bad function calls, if the test fails.
       OR returns False, "import" if there is an import statement"""
    text = open(filename, "rU").read()
    text.replace("\t", "\n")

    while "#" in text:
        text = text[0:text.index("#")] +\
               text[text.index("\n", text.index("#"))::]

    for i in text.split():
        if i == "import" or\
           i[-7::] == ":import" or\
           i[-7::] == ";import":
            return False, "import"

    #split all the text
    new = []
    cur = ""
    cur_string = False
    for i in text:
        if not cur_string:
            if i == "(":
                new.append(cur)
                cur = ""
                new.append("(")

            elif i == ")":
                new.append(cur)
                cur = ""
                new.append(")")
            else:
                if i == '"':
                    cur_string = True
                else:
                    cur += i

        else:
            if i == '"':
                cur_string = False
                cur += i
            else:
                cur += i

    if cur:
        new.append(cur)

    #remove anything that isn't a function call
    ok = []
    for i in xrange(len(new)):
        if new[i] == "(":
            last = new[i-1].split()[-1].split(".")[-1]
            if len(new[i-1].split()) >= 2:
                before_that = new[i-1].split()[-2].split(".")[-1]
            else:
                before_that = None
            #remove a function/class declaration, and tuple declarations, they are different!
            if not before_that in ["def", "class"] and\
               not last in ["print", "=", "in"]:
                ok.append(last)
            else:
                if before_that in ["def", "class"]:
                    acceptable_functions.append(last)

    for i in ok:
        if i in acceptable_functions:
            continue
        else:
            return False, ok

    return True, ok

print test_safe("test.py")
