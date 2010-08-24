

from lib import SLG, SLS
print 'This server will serve on localhost'
print 'If your internet connection is configured correctly, it will also serve on ip:'
print SLS.get_my_server_ip()
print
port = raw_input('What port do you want to serve on? (leave blank for default - 54321): ')
if not port:
    port = SLG.main_server_port
s = SLG.Server()
s.start(int(port))
