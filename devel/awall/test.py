from test_setup import *

print "Testing speed and turn ordering..."
b.do_battle()
print "\n"

print "Testing unit movement..."
print "Alice is at", alice.current_position
print "The unit at (0, 0, 0) is %s" % m.map_panels[0][0][0].entity.name

path = m.move_unit(alice, (2, 1, 0))
print "Alice moves through", path
print "Alice is at", alice.current_position
print "The unit at (0, 0, 0) is %s" % m.map_panels[0][0][0].entity
print "The unit at (2, 1, 0) is %s" % m.map_panels[2][1][0].entity.name