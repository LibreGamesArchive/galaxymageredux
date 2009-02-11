import server

class User(object):
    def __init__(self, name=""):
        self.units = []
        self.money = 150
        self.name = name

class MyHelper(server.ServerHelper):
    def __init__(self):
        self.users = []
        self.whos_turn = 0

    def doEndTurn(self):
        self.whos_turn += 1
        if self.whos_turn >= len(self.users):
            self.whos_turn = 0

    def receiveData(self, transport, data):
        session = transport.sessionno
        cmd = data[0]
        args = data[1::]

        if cmd == "NewUser":
            self.users.append(User(args[0]))
        if cmd == "EndTurn":
            if self.users[self.whos_turn] == args[0]:
                self.doEndTurn()
