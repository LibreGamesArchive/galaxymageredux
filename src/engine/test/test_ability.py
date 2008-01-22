import sys
sys.path.append("..")

import ability
import battle
import effect
import unit
import unittest

b = battle.Battle()

class PunchTestCase(unittest.TestCase):
    def setUp(self):
        self.barehand_punch = ability.Ability()
        self.barehand_punch.ct_cost = 20
        self.barehand_punch.num_uses = ability.Ability.INFINITE_USES
        self.barehand_punch.effects.append(effect.PhysicalAttack(10))
        self.s = unit.Unit("source", unit.Gender.NEUTER, b)
        self.s.statistics[unit.Statistic.PHYSICAL_ATTACK] = unit.Statistic(10)
        self.s.abilities.append(self.barehand_punch)
        self.t = unit.Unit("target", unit.Gender.NEUTER, b)
        self.t.statistics[unit.Statistic.MAX_HP] = unit.Statistic(1000)
        self.t.current_hp = \
            self.t.statistics[unit.Statistic.MAX_HP].get_effective_value()
    def testPunchAttack(self):
        while True:
            if self.s.use_ability(self.barehand_punch, [self.t]):
                self.assertEqual(self.t.current_hp, 900)
                break
        
if __name__ == '__main__':
    unittest.main()