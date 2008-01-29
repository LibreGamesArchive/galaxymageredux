import sys, os
sys.path.append("..")

import ability
import battle
import effect
import unit
import unittest

sys.path.append(os.path.join('..', '..', '..', 'data', 'core', 'abilities'))
import physical_attacks
import attack_spells

b = battle.Battle()

class PunchTestCase(unittest.TestCase):
    def setUp(self):
        self.s = unit.Unit("source", unit.Gender.NEUTER, b)
        self.s.statistics[unit.Statistic.PHYSICAL_ATTACK] = unit.Statistic(10)
        self.s.statistics[unit.Statistic.MAGIC_ATTACK] = unit.Statistic(10)
        self.s.abilities.append(physical_attacks.barehanded_punch)
        self.s.abilities.append(attack_spells.magic_zot)
        self.t = unit.Unit("target", unit.Gender.NEUTER, b)
        self.t.statistics[unit.Statistic.MAX_HP] = unit.Statistic(1000)
        self.t.current_hp = \
            self.t.statistics[unit.Statistic.MAX_HP].get_effective_value()
    def testPunchAttack(self):
        while True:
            if self.s.use_ability(physical_attacks.barehanded_punch, [self.t]):
                self.assertEqual(self.t.current_hp, 990)
                break
    def testMagicZot(self):
        while True:
            if self.s.use_ability(attack_spells.magic_zot, [self.t]):
                self.assertEqual(self.t.current_hp, 950)
                break
        
if __name__ == '__main__':
    unittest.main()