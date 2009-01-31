import newnet

c = newnet.Client("localhost", 44444, "test!")

def mainloop():
    line = raw_input(":->")
    if line == "q":
        c.close()
    else:
        c.avatar.perspective_sendMessage(line)

c.update = mainloop
c.connect()
