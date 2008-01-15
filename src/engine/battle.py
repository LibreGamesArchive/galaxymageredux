"""Module representing the overall state of a battle."""

import observer
import unit

class Battle:
    """The Battle class keeps overall state for a battle."""
    
    clocktick = observer.Event()
    unit_turn_begin = observer.Event()
    unit_turn_end = observer.Event()
    
    def __init__(self):
        """
        TODO: Docstring
        """
        self.num_elapsed_clockticks = 0
        self.units_ready_to_act = []
        self.map_ = None
    
    def do_clocktick(self):
        """
        A clocktick is the smallest unit of time that can pass in a battle.
        Call any callbacks of objects that asked to be notified every clocktick
        """
        self.num_elapsed_clockticks += 1
        self.clocktick(self)
        return None
        
    def do_unit_turn(self, unit_):
        """
        Call any callbacks that occur at the beginning of a turn.
        Then tell the unit to take its turn.
        Then call any callbacks that occur at the end of a turn.
        Then decrement the unit's CT by the standard amount of CT spent every
        turn
        """
        assert(unit_.current_CT >= unit.unit_turn_ct_threshold)
        self.unit_turn_begin(unit_)
        unit_.begin_turn()
        #todo: call end of turn callbacks
        unit_.current_CT -= unit.unit_turn_ct_base_cost
        return None
            
    def queue_unit_turn(self, unit_):
        """
        Add a unit to the list of units ready to take a turn
        """
        assert(unit_.current_CT >= unit.unit_turn_ct_threshold)
        self.units_ready_to_act.append(unit_)
        return None
    
    def do_battle(self):
        """
        Run the battle.
        """
        while True:
            
            # Increment the state of the battle
            self.do_clocktick()
            
            # All units take their turns
            def _unit_get_CT(unit_):
                return unit_.current_CT
            self.units_ready_to_act.sort(key = _unit_get_CT)
            while len(self.units_ready_to_act) > 0:
            
                # Let the unit with the most CT take its turn
                self.do_unit_turn(self.units_ready_to_act.pop(0))
        
            # TODO: Temporary, keeps the battle from going on forever.
            # Remove this once a real way to end the battle is implemented.
            if self.num_elapsed_clockticks > 25:
                break
            
        return None
    
