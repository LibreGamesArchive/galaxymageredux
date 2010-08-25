"""test_safe function from PYGGEL game engine"""

def test_safe_file(filename, acceptable_functions=[]):
    """tests all the function calls in a file against a set of acceptable ones.
       this function also does not allow importing of other modules.
       returns True, [] if there are only acceptable function calls,
       returns False and a list of bad function calls, if the test fails.
       OR returns False, "import" if there is an import statement"""
    text = open(filename, "rU").read()
    text.replace("\r", "\n")

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
                cur+=i

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
            last_full = new[i-1].split()[-1]
            if last == "(" or True in [last.endswith(__i) for __i in (", ", ",", ": ", ":","=")]:
                continue
            if len(new[i-1].split()) >= 2:
                before_that = new[i-1].split()[-2].split(".")[-1]
            else:
                before_that = None
            #remove a function/class declaration, and tuple declarations, they are different!
            if not before_that in ["def", "class"] and\
               not last_full in ["print", "=", "in"]:
                ok.append(last_full)
            else:
                if before_that in ["def", "class"]:
                    acceptable_functions.append(last)

    bad = []
    for i in ok:
        if i in acceptable_functions:
            continue
        else:
            bad.append(i)

    if bad:
        return False, bad

    return True, []

def split_text_by_dels(text, delimiters=[" "]):
    words = text.split(delimiters[0])
    for i in delimiters[1::]:
        new = []
        for word in words:
            new.extend([x for x in word.split(i) if x])
        words = new
    return words

def test_safe_file2(filename, ban_vars=[]):
    """tests all the function calls in a file against a set of acceptable ones.
       this function also does not allow importing of other modules.
       returns True, [] if there are only acceptable function calls,
       returns False and a list of bad function calls, if the test fails.
       OR returns False, "import" if there is an import statement"""
    text = open(filename, "rU").read()
    text.replace("\r", "\n")

    while "#" in text:
        text = text[0:text.index("#")] +\
               text[text.index("\n", text.index("#"))::]

    for i in text.split():
        if i == "import" or\
           i[-7::] == ":import" or\
           i[-7::] == ";import":
            return False, "import"

    words = split_text_by_dels(text, (' ', '\n', '\r', '\r\n',
                                      '(', ':', ')', ';', '[', ']',
                                      '{', '}', ","))

    words_no_strings = []
    have_string1 = False
    have_string2 = False
    for i in words:
        if i.startswith('"') and not have_string2:
            have_string1 = True
        if i.startswith("'") and not have_string1:
            have_string2 = True
        if not (have_string1 or have_string2):
            words_no_strings.append(i)
        if i.endswith('"') and have_string1:
            have_string1 = False
        if i.endswith("'") and have_string2:
            have_string2 = False


    bad = []
    for i in words_no_strings:
        if i in ban_vars or i.split('.')[0] in ban_vars:
            bad.append(i)

    if bad:
        return False, bad
    return True, []
