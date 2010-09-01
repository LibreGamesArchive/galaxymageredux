"""Server and client for the server-list-server"""


import net, urllib

main_server_host = 'localhost' #change to real server later!
main_server_port = 54321

def get_my_server_ip():
    f = urllib.urlopen("http://checkip.dyndns.com")
    s = f.read()
    f.close()

    return s[s.find('<body>')+6:s.find('</body>')].split(":")[1].strip()

class Server(net.Server):
    def __init__(self):
        net.Server.__init__(self)

        self.server_list = {'...':('test','0.0.0.0','44444')}

    def join(self, avatar):
        self.avatars.append(avatar)

    def leave(self, avatar):
        self.avatars.remove(avatar)

    def requestNewAvatar(self):
        return SLSAvatar

    def registerGameServer(self, avatar, name, port, ip):
        self.server_list[avatar] = (name, port, ip)

    def getGameServerList(self, avatar):
        self.remote(avatar, 'sendGameServerList', self.server_list.values())

class SLSAvatar(net.BaseAvatar):
    def perspective_registerServer(self, name, port):
        ip = get_my_server_ip()
        self.server.registerGameServer(self, name, port, ip)
    def perspective_getGameServerList(self):
        self.server.getGameServerList(self)

class Client(net.Client):
    def remote_sendGameServerList(self, _list):
        pass
