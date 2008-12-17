import client

c = client.Client()
c.connect()
c.helper.dispatch("Hello?")
