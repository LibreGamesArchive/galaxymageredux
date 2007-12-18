"""Module representing a Unit"""

from Observer import *
from Battle import *


class Statistic(property):
	"""
	Class representing one of a unit's Statistics (Attack, Speed, MaxHP, etc.)
	"""
	def __init__( self ):
		self.Base = 0
		self.BattleModifier = 0
		self.StatusModifier = 0
		
	def _getBase( self ):
		return self._Base
	def _setBase( self, base ):
		self._Base = base
	Base = property(_getBase, _setBase)
	
	def _getBattleModifier( self ):
		return self._BattleModifier
	def _setBattleModifier( self, battleModifier ):
		self._BattleModifier = battleModifier
	CurrentMP = property(_getBattleModifier, _setBattleModifier)
		
	def _getStatusModifier( self ):
		return self._StatusModifier
	def _setStatusModifier( self, statusModifier ):
		self._StatusModifier = statusModifier
	StatusModifier = property(_getStatusModifier, _setStatusModifier)
	
	def GetEffectiveValue( self ):
		result  = self.Base
		result += self.BattleModifier
		result += self.StatusModifier
		
		#TODO: Do something about equipment here!
		
		return result


class Unit:
	"""Class Representing a Unit"""
	
	UNIT_TURN_CT_THRESHOLD = 100
	UNIT_TURN_CT_BASE_COST = 60
	
	
	def __init__( self, name, gender = "MALE" ):
		self.Name = name
		self.Gender = gender
		self.Statistics = { 
			"PhysicalAttack" : Statistic(),
			"MagicAttack" : Statistic(),
			"Speed" : Statistic(),
			"MaxHP" : Statistic(),
			"MaxMP" : Statistic() }
		self.CurrentHP = self.Statistics[ "MaxHP" ].GetEffectiveValue()
		self.CurrentMP = self.Statistics[ "MaxMP" ].GetEffectiveValue()
		self.CurrentCT = 0
		self.Equipment = { 
			"RightHand" : None,
			"LeftHand" : None,
			"Head" : None,
			"Body" : None,
			"Accessory" : None,
			#"Belt" : []  #How do we handle Belt?  Is it a list?
		}
		self.Abilities = []
		self.Statuses = []
	
	def _getCurrentHP( self ):
		return self._CurrentHP
	def _setCurrentHP( self, hp ):
		self._CurrentHP = hp
	CurrentHP = property(_getCurrentHP, _setCurrentHP)
	
	def _getCurrentMP( self ):
		return self._CurrentMP
	def _setCurrentMP( self, mp ):
		self._CurrentMP = mp
	CurrentMP = property(_getCurrentMP, _setCurrentMP)
		
	def _getCurrentCT( self ):
		return self._CurrentCT
	def _setCurrentCT( self, ct ):
		self._CurrentCT = ct
	CurrentCT = property(_getCurrentCT, _setCurrentCT)
	
	
	def Update( self, battle ):
		"""
		Callback that occurs every clocktick
		"""
		self.CurrentCT += self.Statistics[ "Speed" ].GetEffectiveValue()
		if self.CurrentCT >= Unit.UNIT_TURN_CT_THRESHOLD:
			battle.QueueUnitTurn( self )
	
	def BeginTurn( self ):
		"""
		Handle a turn
		"""
		print self.Name,"'s turn is beginning"
