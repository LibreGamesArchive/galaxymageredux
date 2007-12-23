"""Module representing a Unit"""


unit_turn_ct_threshold = 100
unit_turn_ct_base_cost = 60

class Gender:
    MALE, FEMALE, NEUTER = range(3)
    
class Statistic(property):
    """
    Class representing one of a unit's Statistics (Attack, Speed, MaxHP, etc.)
    """
    
    
    MAX_HP, \
    MAX_MP, \
    SPEED, \
    PHYSICAL_ATTACK, \
    MAGIC_ATTACK, \
    MOVEMENT_RANGE, \
    JUMP_RANGE = range(7)
    
    def __init__(self):
        self.base = 0
        self.battle_modifier = 0
        self.status_modifier = 0
    
    def get_effective_value(self):
        result  = self.base
        result += self.battle_modifier
        result += self.status_modifier
            
        #TODO: Do something about equipment here!
        
        return result


class Entity:
    """Docstring"""
    
    
    def __init__(self):
        # Current position stores x, y, layer.
        # layer is used for overlapping terrain; it is usually 0, but
        # can be higher if the unit is on a bridge or something
        self.current_position = (-1, -1, -1)
            
    def add_to_map(self, map_, x_position, y_position, layer):
        self.current_position = (x_position, y_position, layer)
        map_.map_panels[x_position][y_position][layer].entity = self

class Unit(Entity):
    """Class Representing a Unit"""
   
    def __init__(self, _name, _gender):
        self.name = _name
        self.gender = _gender
        self.statistics = { 
            Statistic.PHYSICAL_ATTACK : Statistic(),
            Statistic.MAGIC_ATTACK    : Statistic(),
            Statistic.SPEED           : Statistic(),
            Statistic.MAX_HP          : Statistic(),
            Statistic.MAX_MP          : Statistic(),
            Statistic.MOVEMENT_RANGE  : Statistic(),
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
   
    def _calculate_move_costs(self, map_):
        print "Not implemented"
    
    def update(self, battle):
        """
        Callback that occurs every clocktick
        """
        self.current_CT += \
            self.statistics[Statistic.SPEED].get_effective_value()
        if self.current_CT >= unit_turn_ct_threshold:
            battle.queue_unit_turn(self)
    
    def begin_turn(self):
        """
        Handle a turn
        """
        print self.name,"'s turn is beginning"
