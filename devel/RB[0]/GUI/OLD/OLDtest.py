#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#------------------------------------------------------------------------------
# demo code for Galaxy Mage Redux.
# this file is heavily commented, as it should be for demo code

# first of all, we only really need the GUI library. The rest is just
# used to make the demo work (obviously I don't really know OpenGL,
# most of my work is in parsers and languages!)
import pygame,os
from pygame.locals import *
import GUI

# this is the routine that needs to be passed to the GUI.
# given a bunch of GUI_RECTS, defined in the GUI (pretty simply),
# it blits them to the screen.
# actually it's a full screen update since the old graphics
# will need to be erased, but I let the gfx engine deal with it ;-)

# Performance guide for GL programmers:
# obviously we can think of many situations where we only
# want to update a really small area (like a when the mouse moves
# over a button) and yet still the whole screen is updated. If
# PyOpenGL cannot cope with this, then I am willing to rewrite the
# gui so it uses a smart dirty rectangles routine. But the code
# in the GUI is a bit easier doing it this way :-S
# update: and also, at least we would have a GUI this way for now!
def redraw_screen(GUI_RECTS):
	# clear the screen
	screen.fill((0,0,0))
	# go through the dirty rects and blit them
	for img in GUI_RECTS:
		screen.blit(img.image,img.rect)
	pygame.display.flip()

# we are going to set up some buttons on the screen. We'll have
# this routine be called when they are clicked, so we can see that
# things work as they should be.
# the arguments used are:
# the_button_that_was_clicked,x_offset,y_offset
# these are offsets into the button, not the screen: most of the
# these last 2 will never be used - but since we don't know what
# you'll be doing, we send it anyway.
# In general, always pass True if things worked out, and False if
# something went wrong. Helps in debugging, you see...!
def button_clicked(widget,x,y):
	print widget.text
	return(True)

# setup the screen.
# this line of code only ever needed for this demo.
screen=pygame.display.set_mode((640,480),HWSURFACE|DOUBLEBUF)

# init the GUI.
# as you can see, this line is pretty simple. It returns an
# instance of the GUI, so you'll need to remember this data
# and keep it somewhere for later reference.
GMR_GUI=GUI.PYTHON_GUI(redraw_screen)

# normally when you change the GUI, the screen automatically
# gets updated. Obviously when you set up a lot of things -
# like when we add a complex window - you won't want all of
# those updates. The solution is to lock the GUI until all
# updates have completed.
# You need to pass it a routine that redraws the screen
GMR_GUI.lock_updates()

# Ok, here goes some GUI building stuff.
# First of all, the GUI only really renders 3 things - windows,
# containers and menus. Here we will only deal with windows.
# first of all, get a window. The parameters in this call
# to create a window are:
# x_position,y_position,x_size,y_size,window_title,visible?
# if either of x_position or y_position are -1, the window is
# centered in the screen for you.
window=GUI.Window(-1,-1,300,160,"Test",True)

# most windows will contain some info and widgets, with a few
# buttons underneath. There is a helper routine to put the
# buttons on for you, and doing this means that the style of the
# windows is consistent.
# This helper routine needs a list of the buttons you want, so we
# need to start with an empty list
buttons=[]

# the buttons in this list are not actually real buttons (we try
# and make things as easy as possible at all times, and real buttons
# need extra detail), so they only need 3 paramaters:
# button_text,keypress,function_to_call_when_pressed
# the routine will turn this data into real buttons
buttons.append(GUI.button_details("OK",None,button_clicked))
buttons.append(GUI.button_details("Cancel",None,button_clicked))
# so thats the 2 buttons we need, now let the GUI do the hard work.
# it extends the bottom, adds a seperator line and spaces the
# buttons out; the first on the RHS and then the rest spaced out
# to the left. The last argument, if True, sets the last button
# (if there are more than 1) on the LHS
window.build_button_area(buttons,False)
# now we add the completed window to the GUI
GMR_GUI.add_window(window)

# do the same with another window, and add a label this time.
# firstly, to help us in the window construction, we'll make
# the label and button first
my_label=GUI.BuildLabel("This is a label")
# and a button
my_button=GUI.Button(0,0,"Xing")
my_button.callbacks.mouse_lclk=button_clicked
# Here's where the GUI suffers: you pretty much have to positon
# all the widgets yourself. Which means you end up with code like:
my_label.rect.x=8
my_button.rect.x=my_label.rect.w+16
my_button.rect.y=8
# granted, you could turn those numbers into constants.
# but I digress..
# get width, height and adjust
width=my_label.rect.w+my_button.rect.w+24
height=my_button.rect.h+16
my_label.rect.y=(height-my_label.rect.h)/2
window=GUI.Window(16,16,width,height,"Label",True)
# add the button and label
window.add_item(my_label)
window.add_item(my_button)
# finally we add the window to the GUI. You can see from this example
# that although the widgets themselves are pretty easy, managing the
# layout generally has to be done by hand, i.e. takes a bit of work
GMR_GUI.add_window(window)

# now lets have a window showing an image
img=GUI.BuildImage(pygame.image.load(
	os.path.normpath("./gfx/test.png")).convert())
# we set the window size to the image size.
# yet when you run the demo, it is easy to see that the window
# is bigger than the image: it contains it!
# when you build a window, it adds a border. This means that
# when you define a window, the size you ask for is always
# smaller than the actual render size.
window=GUI.Window(120,120,img.rect.w,img.rect.h,"Image",True)
window.add_item(img)
GMR_GUI.add_window(window)

# a window with a checkbox
chk=GUI.CheckBox(GMR_GUI.update_screen,40,12,True)
window=GUI.Window(300,100,chk.rect.w+80,chk.rect.h+24,"CheckBox",True)
window.add_item(chk)
GMR_GUI.add_window(window)

# we'll make the last one a simple slider control.
slider=GUI.Slider(GMR_GUI.update_screen,16,16,140,1,140,70)
window=GUI.Window(400,75,172,slider.rect.y+32,"Slider",True)
window.add_item(slider)
GMR_GUI.add_window(window)

# finally, we can unlock the GUI. This also forces a redraw, since
# we must have some GUI gfx undates to render (otherwise why lock
# it in the first place?).
GMR_GUI.unlock_updates()

c = pygame.time.Clock()

# this is the main loop. As you can see, it simply lets the GUI do
# all the work of capturing the events, 1 at a time. It can also
# update the screen by itself since we have given it a routine to
# do just that.
try:
        while(True):
                c.tick(999)
                GMR_GUI.check_inputs(pygame.event.wait())
except:
        print c.get_fps()

