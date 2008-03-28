"""Module representing a Unit"""
import ability

unit_turn_ct_threshold = 100
unit_turn_ct_base_cost = 60

class Gender:
    MALE, FEMALE, NEUTER = range(3)
    
class Statistic(object):
    """
    Class representing one of a unit's Statistics (Attack, Speed, MaxHP, etc.)
    """
    
    MAX_HP, \
    MAX_MP, \
    SPEED, \
    PHYSICAL_ATTACK, \
    MAGIC_ATTACK, \
    MOVE_RANGE, \
    JUMP_RANGE = range(7)
    
    def __init__(self, value=0):
        self.base = value
        self.battle_modifier = 0
        self.status_modifier = 0
    
    def get_effective_value(self):
        result  = self.base
        result += self.battle_modifier
        result += self.status_modifier
            
        #TODO: Do something about equipment here!
        
        return result


class Entity(object):
    """Docstring"""
    
    
    def __init__(self, name):
        self.name = name
        # Current position stores x, y, layer.
        # layer is used for overlapping terrain; it is usually 0, but
        # can be higher if the unit is on a bridge or something
        self.current_position = (-1, -1, -1)
        self.current_HP = 0
            
    def add_to_map(self, map_, x_position, y_position, layer):
        self.current_position = (x_position, y_position, layer)
        map_.map_panels[x_position][y_position][layer].entity = self
        
class Unit(Entity):
    """Class Representing a Unit"""
   
    def __init__(self, name, gender, battle):
        super(Unit, self).__init__(name)
        self.gender = gender
        self.statistics = { 
            Statistic.PHYSICAL_ATTACK : Statistic(),
            Statistic.MAGIC_ATTACK    : Statistic(),
            Statistic.SPEED           : Statistic(),
            Statistic.MAX_HP          : Statistic(),
            Statistic.MAX_MP          : Statistic(),
            Statistic.MOVE_RANGE      : Statistic(),
            Statistic.JUMP_RANGE      : Statistic() }
        self.current_HP = \
            self.statistics[Statistic.MAX_HP].get_effective_value()
        self.current_MP = \
            self.statistics[Statistic.MAX_MP].get_effective_value()
        self.current_CT = 0
        self.equipment = { 
            "RightHand" : None,
            "LeftHand" : None,
            "Head" : None,
            "Body" : None,
            "Accessory" : None,
            #"Belt" : []  #How do we handle Belt?  Is it a list?
        }
        self.abilities = []
        self.statuses = []
        battle.clocktick.add_callback(self.update)
    
    def update(self, battle):
        """
        Callback that occurs every clocktick
        """
        self.current_CT += \
            self.statistics[Statistic.SPEED].get_effective_value()
        if self.current_CT >= unit_turn_ct_threshold:
            battle.queue_unit_turn(self)
    
    def use_ability(self, ability_, target_units):
        """
        Use an ability on each of the units in target_units
        Return True if the ability had an effect on at least one of them,
        False otherwise.
        """
        # We should have made sure that the ability still had uses left already
        assert(ability_.num_uses == ability.Ability.INFINITE_USES or\
            ability_.num_uses > 0 )
        
        # Decrement the user's mp and ct
        self.current_MP -= ability_.mp_cost
        self.current_CT -= ability_.ct_cost
        if ability_.num_uses != ability.Ability.INFINITE_USES:
            ability_.num_uses -= 1
        
        # Carry out the ability on each target
        did_something = False
        for target in target_units:
            for effect in ability_.effects:
                result_list = effect.execute(self, target)
                if result_list.is_successful and len(result_list.results) > 0:
                    did_something = True
                    for result in result_list.results:
                        result.apply()

        return did_something
    
    def begin_turn(self):
        """
        Handle a turn
        """
        #todo: This is just temporary
        print "%s's turn is beginning" % self.name

