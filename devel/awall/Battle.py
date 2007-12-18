"""Module representing the overall state of a battle."""

from Observer import *
from Unit import *

class Battle:
	"""The Battle class keeps overall state for a battle."""
	
	Clocktick = Event()
	UnitTurnBegin = Event()
	UnitTurnBegin = Event()
	
	def __init__( self ):
		"""
		TODO: Docstring
		"""
		self.NumElapsedClockticks = 0
		self.UnitsReadyToAct = []
	
	def DoClocktick( self ):
		"""
		A clocktick is the smallest unit of time that can pass in a battle.
		Call any callbacks of objects that asked to be notified every clocktick
		"""
		self.NumElapsedClockticks += 1
		self.Clocktick( self )
		return None
		
	def DoUnitTurn( self, unit ):
		"""
		Call any callbacks that occur at the beginning of a turn.
		Then tell the unit to take its turn.
		Then call any callbacks that occur at the end of a turn.
		Then decrement the unit's CT by the standard amount of CT spent every turn
		"""
		assert( unit.CurrentCT >= Unit.UNIT_TURN_CT_THRESHOLD )
		self.UnitTurnBegin( unit )
		unit.BeginTurn()
		unit.CurrentCT -= Unit.UNIT_TURN_CT_BASE_COST
		return None
		
	def QueueUnitTurn( self, unit ):
		"""
		Add a unit to the list of units ready to take a turn
		"""
		assert ( unit.CurrentCT >= Unit.UNIT_TURN_CT_THRESHOLD )
		self.UnitsReadyToAct.append( unit )
		return None
	
	def DoBattle( self ):
		"""
		Run the battle.
		"""
		while True:
			
			# Increment the state of the battle
			self.DoClocktick()
			
			# All units take their turns
			def _unitGetCT( unit ):
				return unit.CurrentCT
			self.UnitsReadyToAct.sort( key = _unitGetCT )
			while len( self.UnitsReadyToAct ) > 0:
				
				# Let the unit with the most CT take its turn
				self.DoUnitTurn( self.UnitsReadyToAct.pop( 0 ) )
			
			# Temporary, keeps the battle from going on forever.
			# Remove this once a real way to end the battle is implemented.
			if self.NumElapsedClockticks > 25:
				break
		
		return None
	
