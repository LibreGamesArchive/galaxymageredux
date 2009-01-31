import newnet

class TestClient(newnet.Client):
    def update(self):
        line = raw_input(":->")
        if line == "q":
            c.close()
        else:
            c.avatar.callRemote("sendMessage", line)

c = TestClient("localhost", 44444, "test!")
c.connect()
