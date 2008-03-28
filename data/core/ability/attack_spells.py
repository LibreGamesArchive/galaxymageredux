import sys, os
sys.path.append(os.path.join('..', '..', '..', 'src', 'engine'))

from ability import Ability
import effect

"""
A basic magic spell

No special trigger
Costs 5 MP
Default CT cost
No charge time (TODO: change this)
Unlimited uses
Horizontal range: 0-3
Vertical range: unlimited
No area of effect
Performs a weak magical attack.
"""
magic_zot = Ability()
magic_zot.name = "Magic Zot"
magic_zot.mp_cost = 5
magic_zot.min_h_range = 0
magic_zot.max_h_range = 3
magic_zot.min_v_range_down = Ability.UNLIMITED_RANGE
magic_zot.max_v_range_down = Ability.UNLIMITED_RANGE
magic_zot.min_v_range_up = Ability.UNLIMITED_RANGE
magic_zot.max_v_range_up = Ability.UNLIMITED_RANGE
magic_zot.effects.append(effect.MagicAttack(5))