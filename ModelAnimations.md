# Introduction #

Here it comes ;)


# Details #


structure of an animation file

Idea one:

animation\_name
> animation\_frame
> > animation\_vertices <list of tuples representing vertices> -- ie <(32, 45, 63), (46, 37, 25), etc.>


> bone\_start (x, y, z)

> bone\_end (x, y, z)

> rotate\_amount (x, y, z)

> move\_amount (x, y, z)

> stretch\_amount (x, y, z)

> 

Unknown end tag for &lt;/vertices&gt;



Then you can stack stuff so that animation frames affect more than one group of vertices.
The main good thing about this method is that for each animation you can specify different vertices to affect,
> thereby allowing a bit more natural of a look, but way more pain for teh programmers,
> and it will be much slower.


Second idea - simpler:



&lt;limb&gt;



> 

&lt;vertices&gt;



> bone\_start

> bone\_end



Unknown end tag for &lt;/limb&gt;






<animation\_name>


> 

<animation\_frame>


> > 

<limb\_name>




> rotate\_amount

> move\_amount

> stretch\_amount


I'm not entirely sure how to set up the structure of this right now - but you get the general gist of it.
Basically, for each model two or three files will be loaded - one will be loaded only once ;)
So, when it is time to load the models, the main game animation file will be loaded - this does not define any limbs!
It only defines movements.
Next, the OBJ itself will be loaded up, but not compiled yet.
Third, the specific animation file for this OBJ will be loaded.
This one will define limbs, will be combined with the master file,
> and can override animations - for more uniqueness.

Then the game will split the OBJ up into the limbs specified in the new, composite animation file,
> and then compile each individually.
Then the game will simply check which animation/frame to render,
> and the models will be rotated, moved and scaled to fit.
This method will be farely fast, and it will still allow nice animation IMO.


What we will need then is a program that will allow an artist to load their OBJ and
> section of the pieces into limbs.
Then allow them to set up the bones.
And finally to specify animation sequences.
I have an idea for that, but the good news is this doesn't "require" that, you can do it by hand,
> for now probably a simple box method will work - any vertice within bounds is added to said limb.



## Summary ##
Sorry, gotta run. This probably will look terrible in the wiki - but at least it is up ;)
Well, the indentation is off, and convert all the <> to brackets, for lists like in Python.
The wiki doesn't like those ;)

Cya Later