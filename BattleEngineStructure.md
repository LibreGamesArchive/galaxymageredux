# Introduction #

These are ideas and for the design and representation of the game's battle engine.  What is listed below is not final and not set in stone; they are only ideas for how best to represent the data that the engine will need to keep track of in order to run a battle.

Once we start coding, I'd like to see if we can use pydoc or some similar tool to generate documentation rather than try to keep this page and the code in sync (which won't happen, no matter how hard we try).

The battle engine is modeled after the event listener design pattern.  Many of the objects in the engine can register themselves as listeners for particular events, and they will be notified when such an event occurs.  Here are some sample events that might be used:

  * **CLOCKTICK** - A clocktick is the smallest unit of time that occurs in the battle engine.
  * **UNIT\_TURN\_BEGIN**(unit) - This event occurs whenever a unit's turn begins.
  * **UNIT\_USES\_ABILITY**(sourceUnit, targetUnit, ability) - This event occurs when sourceUnit uses an ability on targetUnit.
  * **UNIT\_DIES** ...
etc.

There might also be events related to the GUI.

  * **ABILITY\_SELECTED\_FROM\_MENU**(unit, target, ability) - I see this as being the trigger upon which units carry out actions.  This is different from the UNIT\_USES\_ABILITY event; there may be commands which, when selected, cause the unit to use one of several abilities (think "Elemental" from FFT) or else abilities that do not need to be selected from the menu (reaction abilities).

# Details #

## Ability ##
This class represents an ability that is explicitly "used", but it need not necessarily be manually activated.  The trigger for the ability could be it being selected from the menu, or the trigger might be being attacked, or any number of other things.

### Members ###
  * **Trigger** _Event_ This is the event upon which this ability is used.
  * **SPCost** _integer_ The number of SP required to use this ability
  * **CTCost** _integer_ The amount by which the user's CT is decremented after using this ability.  This should probably be the same for most abilities, but certain abilities might have a "cooldown" period after their use, while others might allow for action again shortly after being used.
  * **ChargeTime** _integer_ The number of clockticks between when this ability is selected and when it actually "goes off."  This is used for "slow actions," such as spells in FFT.
  * **NumberOfUses** _integer_ The number of times this ability can be used.  This could represent the amount of ammunition available for a firearm, or it could be used to mark that an ability can only be used a set number of times (i.e. you can only cast SuperUltimateSpellOfDoom once every battle).  There is a special value, UNLIMITED, that specifies that the ability can be used as many times as the character has MP for.  TODO: Do we also want to specify a maximum for this?
  * **HorizontalRange** _integer_ The horizontal range for an ability is the number of panels away from the caster that can be targeted.  Horizontal range of 0 means that the ability is centered on the caster.
  * **VerticalRangeUp** _integer_ The vertical range for an ability is the number of panels above or below the caster that can be targeted.  Vertical range of 0 means that the ability must be targeted at a panel at the same height as the caster.  Measurement is conducted from the center of the caster's panel to the center of the target panel.
  * **VerticalRangeDown** _integer_ The upward vertical range may be different from the downward vertical range.
  * **AOEPattern** _enum_ The pattern of panels that this ability hits.  The following are some examples, along with a what they look like at various horizontal ranges.  These need not all be used, and others can be specified instead as needed.
```
    Sorry, drawing multi-line ascii art
    within tables is a bit difficult on
    a wiki.
                   0       1       2
    Pattern	
                                   X
                           X      XXX
     CROSS         X      XXX    XXXXX
                           X      XXX
                                   X
    
    
                                 XXXXX
                          XXX    XXXXX
     BOX           X      XXX    XXXXX
                          XXX    XXXXX
                                 XXXXX
     
     LINE          X       XX      XXX
     (direction can be chosen by user)
    
                                     X
                            X       XX
     CONE          X       XX      XXX
                            X       XX
                                     X
     (direction can be chosen by user)
```
  * **HorizontalAOE** _integer_ The horizontal area of effect for an ability is the number of panels next to the targeted panel that are also affected by the ability.  It is the number along the horizontal axis in the table above.
  * **VerticalAOE** _integer_ The vertical area of effect for an ability is the maximum height difference between a panel and the targeted panel for the panel to be affected by the ability.  Sorry for the terrible wording, but I think most people know what this is.

TODO: We need some way of representing flags such as IsMagical, IsWeaponBased, and other things that various aspects of the game might care about.  This could be done with a bunch of booleans, or with a list of "flags," or some other way?

What would be the most extensible way to do this?  Ideally, adding another flag shouldn't require any modifications to any existing abilities (i.e. it should the flag should default to "false" or "absent" unless it is explicitly specified).

Various example flags:
  * IsMagical
  * IsWeaponBased
  * IsOffensive
  * ...

## Effect ##
This class represents something that can happen during a battle. It could be used to represent a basic attack, what happens when an ability is used, what happens when an item is used, or even the effect of a trap or something.  This was one of the messiest and ugliest parts of the original GM code, and I'd like to redesign it from the ground up, but I'm not sure what's the best way to do this.  Any ideas?

## Item ##

UPDATE: Ajhager has suggested that items be implemented as Abilities; equippables would bestow support abilities (for the FFT-savvy, Battle Boots would give the ability "Move + 1"), consumables would be abilities with a single use, etc.  I like this idea, but I think it needs to be discussed a bit more in IRC to iron out the quirks.  If we decide to go with it, the stuff below will be out of date.

This class represents an item. I'd like to do away with the concept of an "inventory" inside of battle, and instead require all items that can be used in battle to be "equipped" to a unit's "belt" in order to be accessible (there can be several slots for items on a unit's belt, so a unit will be able to carry multiple items into battle).  Therefore, I am going to treat all items as "equippable," whether they are things like swords or armor that are traditionally equippable, or things like heal potions or shuriken that are traditionally not.  See class Unit below for more details of how the belt works.
  * **StatModifiers** _array, maps stat->integer_ An array of modifications to each stat due to equipping this piece of equipment. Note that these values can be negative.  For example, heavy armor might give a reduction to Speed.
  * **WeaponPower** _integer_ The power of this item when used as a weapon.  This is seperate from the item's boost to physical attack power.  I'm a big fan of how weapons work in FFT, so I'm going for a system similar to that. For items that cannot (or should not) be used as weapons, this value is 0.  Note that some items might have nonzero values despite them not being able to be equipped to either hand; this could represent the damage dealt by them when thrown, used, invoked, etc.
  * **EffectUponUse** _Effect_ The effect of the item when used, invoked, etc. For items that cannot be used this way, this value is None.
  * **Consumable** _boolean_ Whether or not this item is consumed upon use.
  * **StackSize** _integer_ How many copies of this item can fit into a single equipment slot.  For example, a single equipment slot might be able to contain 10 arrows, 4 shuriken, 2 healing potions, or a single sword.


## Map ##
Class describing a Map.  This is the entire battlefield on which a battle takes place.  There is only one active Map at any given time.
  * **Panels** _array, maps (x,y,z)->MapPanel_ Array of panels with their x, y, and z coordinates. The z-coordinate is NOT the elevation of the panel.  It is used for multi-level battlefields to distinguish between the levels (i.e. if there is an overhang in one part of the battlefield, z=0 would be for the ground and z=1 would be for the ledge above the ground). Get elevation with Panels[x](x.md)[y](y.md)[z](z.md).Elevation.

TODO: What else does this class need?

## MapPanel ##
Class describing a single panel on a Map.  A panel may be occupied by one or zero units at any given time.

  * **Elevation** _integer_ The elevation of a panel.
  * **Depth** _integer_ The depth of the surface at this point.  If the depth is 0, the surface is solid.  If the depth is 2, units sink into the surface such that their effective elevation is 2 less than the elevation of this panel.  FFT only gave depth to water, but there's no reason other surfaces like lava, quicksand, etc. can't also have depth.
  * **Surface** _Material_ The Material this map panel is made of.
  * **Unit** _Unit_ The Unit standing on thes MapPanel, or None if nobody is present.
    * TODO: Allow this to be either a Unit or an Obstacle (rock, tree, etc.) once there is some way to represent the latter.

## Material ##
Class describing a material from which a MapPanel could be made. Materials will be static objects; examples presumably will include Material.Dirt, Material.Grass, Material.Lava, etc.
  * **Passable** _boolean_ Whether units can pass through MapPanels made of this material.  It is possible for specific units to have exceptions to this rule (i.e. flying units may pass over spiky panels)
  * **Stoppable** _boolean_ Whether units can stop on MapPanels made of this material.  It may be possible for units to be allowed to pass over terrain even if they can't stop on it.
  * **OnPass** _function(Unit)_ Whenever a unit passes through or stops on a MapPanel made of this material, the appropriate function is called on that unit.  The function could be null (in which case there is no effect) or else it could do something like cause damage, add poison, give the unit an item, etc.
  * **OnStop** _function(Unit)_ See above

## Status Effect ##
Class representing a status effect in effect on a unit.  This is a base class that is extended by each specific type of status. For example, there will be a class called Poison that extends this but overrides some relevant methods.

Status Effects may register themselves as event listeners for any event upon which they want to have an effect.  For example, Poison might listen for UNIT\_TURN\_BEGIN and take some HP away from the unit.  Protect might register itself with UNIT\_USES\_ABILITY and, if the ability is physical and the target has Protect, reduce the power by 50%.

  * **Duration** _integer_ The remaining duration of the status. There is a special value, PERMANENT (= 0) that is used to indicate that the status never expires on its own, although it may still be able to be removed forcefully.
  * **IsRemovable** _boolean_ Whether or not the status can be removed forcefully (i.e. Dispel, Remedy, etc.)
  * **Power** _integer_ The "power" of the status.  The exact meaning of this depends on the status itself.  For poison, this might determine the percentage of the unit's HP that gets sapped every time it acts. For AtkUp, this might be the percentage increase in the unit's attack power. I'm envisioning that this would be something between 0 and 100, but there's no reason we couldn't go outside those bounds if we decided to allow it.
  * **AbilityFilter** _function(ability)_ This function determines what abilities the unit is allowed to use while under the effects of this status.  This function takes an ability and returns true if the ability can be used while this status is in effect and false otherwise. For example, "Silence" might return false for all magic and true for everything else. A status that does not affect abilities would return true for everything.

## Unit ##
Class representing a Unit in combat.  We may want to have a base Unit class, and then derive a UnitInBattle and UnitOutsideOfBattle class from those.
  * **Gender** _enum, one of MALE, FEMALE, NEUTER, or whatever else_ Unit's gender
  * **Statistics** _array, maps (stat,modifier)->integer_ Unit's stats.  Spelled out as "statistics" instead of "stats" to avoid confusion with the word "status." This is a 2D array.  Along one axis is the set of a unit's stats:
    * PhysicalAtk
    * MagicAtk
    * Speed
    * MaxHP
    * MaxSP (skill points, not speed)
> Note that current HP and current SP are not part of this.  Along the other axis is the various factors contributing to the effective value:
    * BaseValue (i.e. My character's innate Speed is 6 )
    * BattleModifier (i.e. An ability that gives +1 Speed until end of battle)
    * StatusModifier (i.e. My character is hasted for an additional +4 Speed )
> EquipmentBonus is not included here, as it is a property of the equipment rather than the character. Note that the values in this table can be negative.  For example, if a character gets hit by the status "Slow", their StatusBonus to Speed might be negative.
  * **CurrentHP** _integer_ The unit's current HP
  * **CurrentSP** _integer_ The unit's current SP
  * **CurrentCT** _integer_ The unit's current CT
  * **Equipment** _array, maps slot->Item_ What the unit is equipping.  The "slots" in question could be anything, but here are some for now:
    * **RightHand** (generally a weapon)
    * **LeftHand** (sometimes a weapon, sometimes a shield, sometimes empty)
    * **Head** (generally a hat of sorts, occasionally a frog)
    * **Body** (generally armor of sorts)
    * **Accessory** (why do rings and boots always take up the same slot? :-p)
    * **Belt** The belt slots are generally occupied by comsumable or "in battle" items.  The exact type of item that gets equipped here depends on what the character is capable of doing, and could range from healing items for medics to shuriken for ninja to spare swords for warriors.  The exact number of these slots will vary by unit.
  * **CanEquip** _function(slot, Item)_ Returns true if a unit can equip the given item in the given slot and false otherwise.  Needs to be present in battle, to handle the case where a unit changes equipment mid-battle.
  * **Abilities** _list of Ability_ A list of all the abilities the unit has.
  * **Statuses** _list of Status_ A list of all the statuses in effect on the unit