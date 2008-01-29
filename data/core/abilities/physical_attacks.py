import sys, os
sys.path.append(os.path.join('..', '..', '..', 'src', 'engine'))

import ability
import effect

"""
A basic unarmed attack ability.

No special trigger
No MP cost
Default CT cost
No charge time
Unlimited uses
Horizontal range: exactly 1
Vertical range: <=2 up, <=3 down
No area of effect
Performs a very weak physical attack.
"""
barehanded_punch = ability.Ability()
barehanded_punch.name = "Barehanded Punch"
barehanded_punch.min_h_range = 1
barehanded_punch.max_h_range = 1
barehanded_punch.min_v_range_up = 0
barehanded_punch.max_v_range_up = 2
barehanded_punch.min_v_range_down = 0
barehanded_punch.max_v_range_down = 3
barehanded_punch.effects.append(effect.PhysicalAttack(1))
