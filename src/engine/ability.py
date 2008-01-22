class AreaOfEffectPattern(object):
    
    CROSS, BOX, LINE, CONE = range(4)
    
    def __init__(self, pattern, h_size, v_size):
        self.pattern = pattern
        self.h_size = h_size
        self.v_size = v_size


class Ability(object):
    """This class represents an ability that is explicitly "used", but it need
    not necessarily be manually activated. The trigger for the ability could be
    it being selected from the menu, or the trigger might be being attacked, or
    any number of other things."""
    
    INFINITE_USES = -1
    
    def __init__(self):
        self.trigger = None
        self.mp_cost = 0
        self.ct_cost = 0
        self.charge_time = 0
        self.num_uses = 0
        self.h_range = 0
        self.v_range_up = 0
        self.v_range_down = 0
        self.aoe_pattern = AreaOfEffectPattern(AreaOfEffectPattern.CROSS, 1, 0)
        self.effects = []
    
    def is_fast_action(self):
        return self.charge_time == 0
