import basic
import realm

s = basic.Server()
r = realm.Realm(44444, s)
r.start()
