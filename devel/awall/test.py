from test_setup import *

b.do_battle()
print alice.current_position
print m.map_panels[0][0][0].entity.name
costs = m.calculate_movement_costs_for_unit(alice)
for r in range(m.get_width()):
    print costs[r]
