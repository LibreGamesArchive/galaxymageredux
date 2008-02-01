
So here is the demo code.

Make sure you have Pygame + Python installed.
Make sure core.py is executable

  chmod +x core.py
 
Run the code

  ./core.py

Points to notice:

  Right mouse click anywhere in the window exits the program
  There is a bug in the slider knob render code
  There is a bug in that button highlights are rendered whenever
    the mouse is above them, even if the mouse is over another
    window at the same time
  There are probably other bugs, but nothing really big
  All the interesting comments on the code are in core.py


Mmmm - I think that's it for now. I'm a bit unhappy about having
to pass the update_screen() routine to the slider and checkbox,
and obviously the bugs above need to be sorted out. But hopefully
the essential character of the code will now be clear to you.

Feel free to give me any comments, ideas or suggestions. I'll do my
best to get this GUI up and working as you'd like it. I'm looking
at getting menus up next, followed by some widgets. A text input
box would probably be the most useful.

Finallly, I am aware that I probably havn't kept to the GMR coding
standards. Let me get the code working properly and I'll fix that.


