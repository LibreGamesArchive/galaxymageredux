"""
Effect module.
This module contains objects used for representing something that one unit
can do to another.  The Effect class represents something that a unit does,
and the EffectResult class represents the result of said Effect.
"""

import unit

class Effect(object):
    def __init__(self):
        pass
    def execute(self):
        return None
    
class PhysicalAttack(Effect):
    def __init__(self, power):
        super(PhysicalAttack, self).__init__()
        self.power = power
        
    def execute(self, source, target):
        if (True): #TODO: Check accuracy/evasion
            results = []
            results.append(ReduceHPResult(target, \
                source.statistics[unit.Statistic.PHYSICAL_ATTACK]\
                .get_effective_value() * self.power))
            return EffectResultList(True, results)
        else:
            return EffectResultList(False, [])

class MagicAttack(Effect):
    def __init__(self, power):
        super(MagicAttack, self).__init__()
        self.power = power
        
    def execute(self, source, target):
        if (True): #TODO: Check accuracy/evasion
            results = []
            results.append(ReduceHPResult(target, \
                source.statistics[unit.Statistic.MAGIC_ATTACK]\
                .get_effective_value() * self.power))
            return EffectResultList(True, results)
        else:
            return EffectResultList(False, [])




class EffectResult(object):
    def __init__(self, entity):
        self.entity = entity
    
    def apply(self):
        pass

class ReduceHPResult(EffectResult):
    def __init__(self, entity, amount):
        super(ReduceHPResult, self).__init__(entity)
        self.amount = amount
    
    def apply(self):
        self.entity.current_hp -= self.amount
        if self.entity.current_hp < 0:
            self.entity.current_hp = 0
            
            
class EffectResultList(object):
    def __init__(self, is_successful, results):
        self.is_successful = is_successful
        self.results = results
    def apply_results(self):
        # Only do something if the effect didn't miss
        if self.is_successful:
            for result in self.results:
                result.apply()