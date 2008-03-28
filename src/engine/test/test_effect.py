"""Unit tests for effect module"""

import sys
sys.path.append("..")

import effect
import unit
import unittest
import battle

b = battle.Battle()

class EffectResultTestCase(unittest.TestCase):
    def setUp(self):
        self.t = unit.Unit("target", unit.Gender.NEUTER, b)
        self.t.statistics[unit.Statistic.MAX_HP] = unit.Statistic(1000)
        self.t.current_hp = \
            self.t.statistics[unit.Statistic.MAX_HP].get_effective_value()
    def testReduceHPResult(self):
        hundredDamage = effect.ReduceHPResult(self.t, 100)
        hundredDamage.apply()
        self.assertEqual(self.t.current_hp, 900)
        thousandDamage = effect.ReduceHPResult(self.t, 1000)
        thousandDamage.apply()
        self.assertEqual(self.t.current_hp, 0)
        
        
        
class EffectTestCase(unittest.TestCase):
    def setUp(self):
        self.s = unit.Unit("source", unit.Gender.NEUTER, b)
        self.s.statistics[unit.Statistic.PHYSICAL_ATTACK] = unit.Statistic(10)
        self.t = unit.Unit("target", unit.Gender.NEUTER, b)
        self.t.statistics[unit.Statistic.MAX_HP] = unit.Statistic(1000)
        self.t.current_hp = \
            self.t.statistics[unit.Statistic.MAX_HP].get_effective_value()
    def testPhysicalAttack(self):
        tenPower = effect.PhysicalAttack(10)
        results = tenPower.execute(self.s, self.t)
        results.apply_results()
        # Check whether the attack hit
        if results.is_successful:
            self.assertEqual(self.t.current_hp, 900)
        else:
            self.assertEqual(self.t.current_hp, 1000)
        
if __name__ == '__main__':
    unittest.main()