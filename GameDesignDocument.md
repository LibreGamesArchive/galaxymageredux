# Introduction #
GalaxyMage Redux Game Design Document

This is the game design document to help developers stay on the same page as they progress through each phase in development. Please note that this document is very much still a _work in progress_.

# Details #

## Basic Overview ##

GalaxyMage Redux is intended to be a cross-platform, networked and open source game that follows in the footsteps of GalaxyMage, which was in turn inspired by such games as Final Fantasy Tactics, Disgaea, Bahamut Lagoon, and so on. Redux will support singleplayer quick battles and campaigns (with plot driven battles), and multiplayer quick battles in hotseat and network play.


## Factions ##

_TBD_

## Unit Statistics ##

Every unit has the following:

  * **Name:** Random or chosen at creation
  * **Class:**  The unit’s base class.  Determines base stats like HP, SP, Move, Jump,
  * **Hit Points:**  Remaining life of the unit
  * **Skill Points:**  Points for using skills and magic
  * **Move:**  Determines how many tiles a unit may move per turn
  * **Jump:**  Determines the maximum height difference a unit can move between
  * **Speed:**  How fast and often a unit gets to have an action in battle
  * **Skills:**  Each unit may choose from the list that their unit class has, up to four.
  * **Point Cost:** Useful to determine the general strength of the unit; based upon the skills, equipment, and other things that affect point score.



## Equipment ##

  * **Weapon:**  Some classes are limited to using only certain type of weapons while others can wield any or none.
  * **Body Armor:**  Classes are limited to choosing an armor that fits into their category: Heavy, Medium or Light. Some classes may not wear any armor.
  * **Shield:**  Provides a chance to block, some units cannot equip shields
  * **Helmet:**  Helmets provide protection from different types of ailments such as confusion, blindness, etc.
  * **Shoes:**  Shoes provide an enhancement to speed, move, or jump, or a combination thereof
  * **Accessory:**  Provides an additional effect that can be of any type


## Stats With Equipment ##

  * **Attack:**  Determined from a unit’s class, equipment, and any abilities that they may be under. The base amount of damage a unit will do.
  * **Defense:**  Determined from a unit's class and armor.
  * **Evade:**  Determined from a unit’s class, speed, equipment, and any abilities that they may be under. Percentage chance of dodging an attack.
  * **Charge Time:**  Used only in battle, this represents the time until the unit's next action

## Battle ##

Battles will take place on a 3D map with units represented by 3D characters. The player(s) take turns attacking each other and fighting towards a goal predefined before the fight starts.  Example goals would be: Destroy All Opponents, Destroy All Opponent Commanders, King of Hill for X Turns, Capture the Flag X Times, or Survive for X Turns, or other more complicated objectives (generally campaign objectives). Not every team on the same map need have the same goal. For example, one team may have the goal of Destoy All Opponents and the opposite team may have a goal of Survive for X Turns.

Battle turns take place based on the speed of units participating. Faster units will receive more turns in the long run than a slow unit would.


An example speed loop:

An archer has 10 speed, while a fighter has 7. For every iteration of the speed loop (a unit finishes its turn) they would add their speed to their charge time. So Turn 2, the archer would have 20 CT, and the fighter would have 14. When the CT gets to a predetermined amount (lets say 25 for this example, but most likely will be 100 or even 1000) that unit gets a turn and any additional CT is wrapped around.

You can see that just a little bit of extra speed greatly affects the amount of turns a unit can get. The archer almost gets 3 turns for the fighter’s 2 just because the archer’s speed is 3 higher.

Some skills will also have a Charge Time. For example, say a mage casts a fire spell that has a charge time of 20. The unit who is performing the task, a mage, has a speed of 9. During the time that the attack is charging the unit who is performing the attack cannot gain any CT. Instead, any CT they would have gotten goes into the attack’s CT. So it would take two iterations of the speed loop in order to perform this attack. So watch out! If the mage’s target moved during that time the attack would have been wasted. It is important to pay attention to enemy’s CT and speed too.

Basic attacks and many skills will not have a CT and will be performed immediately.


For any attack, the direction the attack is coming from affects the amount of damage and the chance to evade. A unit that is attacked on the front has a +Speed x 2% chance to avoid and any damage is reduced by 20%. Any attack from the sides adds +Speed% evade to the attacked unit and a reduction by 10% if it hits. An attack from the rear negates 95% chance of evasion (or max of 5% evasion by attacked unit) and no chance of damage reduction. Actual figures subject to change.

## Camera ##

In general, the camera will act like the cameras from FFT or Disgaea, except with a perspective view (rather than orthogonal). While the camera is locked to the center of the map, the player can orbit the camera in 90 degree intervals (4 angles of the field) and arbitrarily tilt. The player could also change to a top down view, which should be used in difficult terrain like walls and mountains. The camera may be switched to a free view that allows full orbit and zoom of the battlefield.

## Party Building System ##

The multiplayer features a party building system intended to simulate the normal process of levelling up which would happen in campaign mode. This should make the multiplayer experience even more in-depth by providing a unique customizable army to play with. Players will be able to save and share armies so that particular combinations can be reused during multiplayer games.


The Party Building System works off points. The player should have a good idea of what their target total points should be, for example 400 would be for small games, while 5000 would be for large games.  Then, choosing from the unit list the player builds their army, adding equipment, skills, enhancements, and others. Each additional unit and every addition to a unit costs a certain amount of points.


**Things that affect the point score:**

  * **Unit Class:** Some classes are more expensive than others
  * **Equipment:** Each piece of equipment adds additional points, the cost of the piece of equipment is proportional to the abilities it provides
  * **Skills:** Some skills are more expensive than others based on their overall effectiveness
  * **Stat Increases:** Player can also manually increase certain stats of the unit at a cost comparable to the amount of increase. (Example: 2 increases would be 5 points each, but a 3rd would be 10 points.  This is to discourage "super" units)
  * **Items:** Any items such as health potions, charge (aka mana) potions, etc that you bring into battle


## Skills Attributes ##

Every skill has the following attributes:

  * **Damage Max:**  Max amount of damage the attack can do under normal circumstances
  * **Damage Min:**  Minimum amount of damage the attack can do under normal circumstances. Note: For a healing skill, use negative numbers
  * **Height:** The maximum amount of height difference that the skill can reach (from the unit's current height)
  * **Min Range:**  Minimum amount of tiles away from user that the attack may hit
  * **Max Range:** Maximum amount of tiles away from user that the attack may hit
  * **Area of Effect:**  Area around target that the skill will affect.
  * **Area of Effect Height:**  Difference in height that the skill can affect within area of effect

> Note: If a skill has a 2 AoE Height, then it cannot affect a tile with 9 height if the target tile is at 6 height. (9 – 6 > 2) It could affect it if the AoE Height was 3.

  * **Enhancements:**  List of beneficial effects that the skill may add to the affected target. (Examples: Haste, Protect, etc.)
  * **Ailments:**  List of detrimental effects that the skill may add to the affected target  (Examples: Poison, Slow, etc.)



## Tile Attributes ##

A tile is one square on the field. It has things such as:

  * **Height:**  Represented in increments of 0.5, between 1 and infinity, within reason.
  * **Object:** Optional, the name of an object to be placed on the tile, example: tree, rock, etc.
  * **Type:**  This is the type of terrain, such as grass, dirt, stone, etc..

## Map Attributes ##

The map is a collection of tiles arranged in a certain way as described in the the file structure of the map.

  * **Height:**  Number of tiles tall.
  * **Width:**  Number of tiles wide.
  * **Team Placement Area:**  Each player's placement area for putting down troops.