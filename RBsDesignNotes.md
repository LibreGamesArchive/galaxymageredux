# Introduction #

Here I will write up my thoughts/designs for things, so others can see them, instead of just working from my own list, feel free to comment/modify it, since I can always just check for changes if necessary :)


# GoogleCode cleanup #
Someone really needs to either update or delete the old wiki pages that aren't accurate anymore.


# Network #

Lot's of things need to happen/be made.
The servers need to be fast, each being able to handle perhaps 50 games without noticeable lag.
Registration server - so when you create your own you can register it there, in turn the regserv will ensure your server can actually be reached (not just localhost), and if it can, will create an entry with whatever name you want and your parameters.

Parameters for regserv will be server\_name, server\_version, server\_max\_users, password (can be empty)
When you make your server, it will give you the choice of registering or not.
It will also spit out your online IP address.
Server's will maintain a connection to regserv except if they are in private mode.
If they lose connection to regserv **but** maintain server host, they will automatically go into private mode, storing data.
Operators of server can re-apply to regserv at their leisure.

Server terminal should really allow input to be gathered for controlling it.

Need to change network code to add callbacks for getting responses instead of having server/client send a request as response...

Restructure the server to function with states, where lobby is a state, and games are states.

# Security #
How do we want to handle distribution of mods?
ATM in-game there is no protection, you just have to trust the mod to not screw with your system.
A couple possibilities:
  * return to file scanning to weed out obvious issues (exec, import)
  * destroy modules access to global and local variables outside of their scope.
  * How do we allow the module to then access the game without allowing it to leak out to unauthorized areas?

Current thought on best system - server doesn't need to know what is in mod, it just funnels communications, so it is already secure from any threats from a mod.
If users don't have correct mod, they can't join a game.

Should we allow players to download mod data from the master? What if the master doesn't like that idea? Won't it slow down gameplay?

Should we have a mod database, where you can search and download from itself, either in-game or from a website?
How will we handle mod submissions - potentially there will be a lot.

Users can always just distribute mods themselves - probably for the best.
If we do that then you just trust the source of the mod.
If someone wants it on the database, we'll just ensure it is not gonna do something stupid...

I still think if there is a way to truly isolate the mod from the game, for safety it would be best. We can then file scan for Python commands we don't like (import, exec) and delete builtins for others (eval, import, etc.)
The issue with that is, how does the mod get information then - or change things?
For getting info, the engine could simply store everything in the mods main class - which then has a variable (mod) where the actual mod is, so you just grab the parent.
But how to access network commands then - end turn, unique commands, etc.?
Perhaps it's simple:
  * variables in main scenario - turn\_over (just turn to True when ending turn), etc.
  * sendCommand, execCommand, testCommand - stick network discussions into buffer that engine grabs and sends to network, master checks testCommand, and tells execCommand if alright...


# Graphics #
Need to convert over to OpenGL+3d engine...
First, need gui rewritten/updated, big issue is fonts, otherwise it is a simple conversion...
Second is handling map code/picking - just rip off of PYGGEL.
Third is map file parsing and a map maker...
Add RenderGroups to 3d engine - instead of builtin render\_2d, render\_3d, render\_always etc.
Make camera have a **real** pos so there can be a RenderGroupOrdered class for nice 3d blending.
Add a theme-image creator tool, and convert gui to using theme images (big sprite sheets with font/image data all inside, and controls for creating TextureRegions from that)...


# Map Engine #
Need to support multiple tile height, bridges/caves/etc...
Tiles will need to be autonomous structures, cubes with a quad-splintered triangle top.
Center of top is tile height, edges are average of neighboring tiles and this tiles' heights.
sides edges match top edges.
Sides hidden if not shown.
bottom is same as top.

Do we want "hard edges" or cliffs to be definable, or something set, like 2 tiles higher is sloped, 3+ is cliff?

pathing needs to check tiles internal pointers to neighbors

One -HUGE- issue with doing multiple layers, and really doing 3d at all, is how do we make units visible, or turn off terrain, or best, center the camera so that it views the player and not all the other junk?
Do we really have to resort to ODE and ray casting?

GUI - remember to place custom game widgets in a game definition - so they don't clog up the gui directory.
Themes - border/collision handling - update theme with new - widgets update\_theme method