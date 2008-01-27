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

# get modules
import sys,pygame,os
from pygame.locals import *
from GUI_Defines import *

# helper classes go here

# class that holds the dirty rectangle updates
class dirty_rect:
	def __init__(self,pic,rec):
		self.image=pic
		self.rect=rec

def null_routine(x):
	"""Null routine for use in locking the GUI"""
	pass

# data storage goes here because other routines need to see it
# just stops us passing round pointers all day long
images=[]
fonts=[]

# there is a simple (?) class that we need for the GUI
class PYTHON_GUI:
	def __init__(self,redraw):
		self.windows=[]
		self.id_next=0
		self.unused_id=[]
		self.redraw_routine=redraw
		self.lock_hold=None

		# now load all (!) the images we need
		# start with all the images that have an alpha
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/slider_knob.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/number_select.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/arrow_up.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/arrow_down.png")).convert_alpha())
		# now we have the menu icons
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/open.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/save.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/preferences.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/exit.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/senate.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/military.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/statistics.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/about.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/help.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/new.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/debug.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/console.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/icons/city.png")).convert_alpha())
			
		# now the non-alpha images
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/img_music.png")).convert_alpha())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_tl.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_lft.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_bl.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_bot.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_br.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_rgt.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_tr.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_top.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_lft_lg.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_bot_lg.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_rgt_lg.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/win_top_lg.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/button.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/button_high.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/check_yes.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/check_no.png")).convert())
	
		# more gui graphics (yes, this *is* a long list :-( )
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/scrollbar_top.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/scrollbar_bottom.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/schan_mid.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/schan_top.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/schan_bot.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/schand_bulk.png")).convert())
		# graduated bar images
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/gradbar64.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/gradbar96.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/gradbar128.png")).convert())
		# optionmenu images
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/optionmenu_lhand.png")).convert())
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/optionmenu_rhand.png")).convert())
		# a final test image
		images.append(pygame.image.load(os.path.normpath("./gfx/gui/test_image.png")).convert())
	
		# set up the fonts and that's it!
		pygame.font.init()
		fonts.append(pygame.font.Font(os.path.normpath("./gfx/Vera.ttf"),FONT_STD))

		self.moving_window = False

	def lock_updates(self):
		"""These next 2 routines are used for mass updating of the GUI
		   Normally we redraw to the screen when something has changed,
		   but when we add lots of items all together, we'ed like to
		   stop this mass updating and do it when ready. This routine
		   stops the updating"""
		self.lock_hold=self.redraw_routine
		self.redraw_routine=null_routine
		return(True)
	
	def unlock_updates(self):
		"""Update screen as normal after GUI updates; also update the
		   current screen now"""
		self.redraw_routine=self.lock_hold
		# we always update the screen after an update
		self.update_screen()
		return(True)

	def get_new_id(self):
		"""Returns new id number - always unique - and
		   updates itself ready for next time"""
		# we may have old ones to reuse
		if(len(self.unused_id)>0):
			# use an old id number
			return(self.unused_id.pop())
		self.id_next+=1
		return(self.id_next-1)

	def update_screen(self):
		"""Build all rectangles and blit to screen"""
		# any images at all?
		if(len(self.windows)==0):
			return(False)
		new_images=[]
		# get all windows that are visible
		for i in self.windows:
			if(i.visible==True):
				new_images.append(dirty_rect(i.image,i.rect))
		# were any visible?
		if(len(new_images)==0):
			return(False)
		# yes, so first invert the list
		new_images.reverse()
		self.redraw_routine(new_images)
		return(True)

	# now a function to add a window
	# it has it's own function because it has to return the index number
	# of the created window
	def add_window(self,window):
		"""Call to add a window to the gui window list. It always goes
		   on the top of the window pile, and thus if modal traps all
		   user input. Returns the id number of the window in the list,
		   so you can amend the window afterwards"""
		# give the id number
		window.id_number=self.get_new_id()
		# get the window to draw itself
		window.image=window.draw_window()
		self.windows.append(window)
		# and we'll need to redraw the screen
		self.update_screen()
		# always return the windows id number
		return(window.id_number)

	def delete_window_id(self,window_id):
		"""Match the window to the id number and delete it"""
		index=0
		for i in self.windows:
			if(i.id_number==window_id):
				# delete the window and return
				self.windows.pop(index)
				return(True)
			index+=1
		# failed to match id number
		return(False)
		
	def delete_window(self,id_value):
		"""Remove the given window from the window list and the screen"""
		# add the id number to the used list
		self.unused_id.append(id_value)
		# now find the window and delete it
		# remove the dirty rect
		# update the screen
		return(True)

	def raise_to_top(self,id_value):
		"""Find the given window, if possible, and raise to the top
		   of the window list. Returns true if that happened,
		   false otherwise"""
		# match the id number
		index=0
		for i in self.windows:
			if(id_value==i.id_number):
				# found the match
				# only do something if index!=0
				if(index!=0):
					# perform the swap and exit
					self.windows.insert(0,self.windows.pop(index))
					return(True)
				else:
					return(False)
			index+=1
		# no matching id found
		return(False)

	def move_window(self, win, x, y):
                self.raise_to_top(win.id_number)
                win.rect.x += x
                win.rect.y += y
                self.update_screen()
                return True

	# use this function to test the mouse against all objects
	# that is, all windows and menus
	def test_mouse(self,x,y,action,event=None):
		"""test_mouse returns False if nothing got called
		   Otherwise it handles checking the action against all
		   of the widgets, menus and windows that are active"""
		quit=False
		first=True
		# go through the windows one by one

		if action == MOUSE_LCLK:
                        self.moving_window = False
		if self.moving_window:
                        if event and event.type == MOUSEMOTION:
                                self.move_window(self.moving_window, *event.rel)
                else:
                        for foo in self.windows:
                                if quit==True:
                                        return(False)
                                # if this is a modal window, then stop after processing:
                                quit=foo.modal
                                # is the mouse pointer inside the window, or is there any window at all?
                                if((foo.rect.collidepoint(x,y)==True)and(foo.visible==True)):
                                        # firstly, if we click over a window that is not the top
                                        # one, then we first of all bring that window into focus
                                        # and then carry the click event down
                                        if((first==False)and(action==MOUSE_LCLK)):
                                                # focus this window
                                                self.raise_to_top(foo.id_number)
                                                # and redraw the screen
                                                self.update_screen()
                                        # the next thing to do is check that the window
                                        # itself is not being moved
                                        # what's the height of the title bar?
                                        wheight=images[WIN_TOP].get_height()
                                        # remove the offsets and see if we are in the top bar
                                        # we already know that we fit in the x dimension, so just check the y
                                        # of course, the event we are checking for is a mouse ldown
                                        if((y<(foo.rect.y+wheight))and(action==MOUSE_LDOWN)):
                                                # ok, we we are in the top win menu bar
                                                # we'll move all of this to another routine
        ##					self.move_window(foo)
                                                self.moving_window = foo
                                                # when completed, this routine is over!
                                                return(True)
                                        # check all of the points inside the window
                                        for bar in foo.items:
                                                if bar.active==True:
                                                        # don't forget to include the offsets into the window
                                                        x_off=x-foo.rect.x
                                                        y_off=y-foo.rect.y
                                                        if bar.rect.collidepoint(x_off,y_off)==True:						
                                                                # get offset into widget
                                                                x_widget=x_off-bar.rect.x
                                                                y_widget=y_off-bar.rect.y
                                                                # now test to see if we need to make a call
                                                                if((action==MOUSE_OVER)and(bar.callbacks.mouse_over!=mouse_over_std)):
                                                                        # widget asked for callback on mouse over
                                                                        bar.callbacks.mouse_over(bar,x_widget,y_widget)
                                                                        return(True)
                                                                elif((action==MOUSE_LCLK)and(bar.callbacks.mouse_lclk!=mouse_lclk_std)):
                                                                        # widget asked for callback on mouse left click								
                                                                        bar.callbacks.mouse_lclk(bar,x_widget,y_widget)
                                                                        return(True)
                                                                elif((action==MOUSE_LCLK)and
                                                                                 (bar.callbacks.mouse_dclick!=mouse_dclick_std)and
                                                                                 (self.dclick_handle!=bar)):
                                                                        # widget wants a double-click: this was the first one, so we need
                                                                        # to keep an eye out for the next click
                                                                        self.dclick_handle=bar
                                                                        # set our timer so we get an event later
                                                                        pygame.time.set_timer(EVENT_DC_END,DCLICK_SPEED)
                                                                        return(False)
                                                                elif((action==MOUSE_LCLK)and
                                                                                 (bar.callbacks.mouse_dclick!=mouse_dclick_std)and
                                                                                 (self.dclick_handle==bar)):	 
                                                                        # it's a real bona-fida double-click
                                                                        # firstly clear all double-click data, then run the code
                                                                        pygame.time.set_timer(EVENT_DC_END,0)
                                                                        self.dclick_handle=None
                                                                        bar.callbacks.mouse_dclick(bar,x_widget,y_widget)
                                                                        return(True)
                                                                elif(action==MOUSE_DCLICK):
                                                                        # obviously we got a double-click where it wasn't needed
                                                                        pygame.time.set_timer(EVENT_DC_END,0)
                                                                        self.dclick_handle=None
                                                                        return(False)
                                                                elif((action==MOUSE_LDOWN)and(bar.callbacks.mouse_ldown!=mouse_ldown_std)):
                                                                        # widget asked for callback on mouse left down
                                                                        bar.callbacks.mouse_ldown(bar,x_widget,y_widget)
                                                                        return(True)
                                                                elif((action==MOUSE_RCLK)and(bar.callbacks.mouse_rclk!=mouse_rclk_std)):
                                                                        # whilst still debugging, I've left this one out
                                                                        print "Do a mouse right click on ",bar.describe
                                                                        return(True)
                                                                # and then exit
                                                                return(False)
                                
                                        # if we get here, then we detected an event inside a window
                                        # other windows don't get a look in here
                                        # we know nothing happend because we are here :-s
                                        return(False)
                                # no longer on the first window
                                first=False
		# nothing happened? at least inform the last routine
		return(False)

	# routine captures what event we got, then passes that message along
	# to the testing routine (i.e. this code only checks if a MOUSE event
	# happened, the later function checks if we got a GUI event)
	def check_inputs(self,event):
		"""check_inputs() is called on a loop whilst the game is waiting
		   for user input (i.e. most of the time). It doesn't actually do
		   anything with the input except pass the event along to somewhere
		   else, so think of it more like a sorting office for the post"""
		# lets start with the simple case: handling keypress values
		if(event.type==KEYDOWN):
			# ignore keypresses for now :)
			action=MOUSE_NONE
		# catch other stuff here, before we process the mouse
		action=MOUSE_NONE
		# was it the end of a double-click check?
		if(event.type==EVENT_DC_END):
			# kill timer and handle data
			pygame.time.set_timer(EVENT_DC_END,0)
			self.dclick_handle=None
			return(True)
		# worst of all, could be an instant quit!
		if(event.type==pygame.QUIT):
			sys.exit()

		# menu redraw checks go here

		if(event.type!=NOEVENT):
			# if it's a rmb down, then possibly exit
			if((event.type==MOUSEBUTTONDOWN)and(event.button==3)):
				if(RMOUSE_END==True):
					sys.exit(False)
			# was it left mouse button up?
			elif((event.type==MOUSEBUTTONUP)and(event.button==1)):
				x,y=pygame.mouse.get_pos()
				action=MOUSE_LCLK
				self.test_mouse(x,y,action,event)
			# some things (like sliders) respond to a mousedown event
			elif((event.type==MOUSEBUTTONDOWN)and(event.button==1)):
				x,y=pygame.mouse.get_pos()
				action=MOUSE_LDOWN
				self.test_mouse(x,y,action,event)
			else:
				# have we moved?
				if(event.type==MOUSEMOTION):
					x,y=pygame.mouse.get_pos()
					action=MOUSE_OVER
					if(self.test_mouse(x,y,action,event)==False):
						self.check_button_highlights(x,y)
			if(action==MOUSE_NONE):
				return(False)
			else:
				# at least something happened	
				return(True)

	def check_button_highlights(self,x,y):	
		"""Check all of the buttons inside the top-layer window to see
		   if any need to be highlighted. Returns True if anything
		   on the screen needed to be updated
		   If another button is highlighted and we need to highlight
		   another, make sure the other changes back"""
		# make sure we have something to test against first
		if(len(self.windows)==0):
			return(False)
		# otherwise, go through all the windows		
		for foo in self.windows:
			for bar in foo.items:
				if((bar.active==True)and(bar.wtype==WT_BUTTON)):
					xoff=x-foo.rect.x
					yoff=y-foo.rect.y
					if(bar.rect.collidepoint(xoff,yoff)==True):
						# don't forget to test here if it's actually visible or not... ;-)
						if(bar.visible==False):
							return(False)
						# already highlighted?
						if(bar.highlight==True):
							return(False)
						else:
							# update the screen
							bar.highlight=True
							bar.image=bar.pressed
							# update that window as well
							bar.parent.image=bar.parent.draw_window()
							self.update_screen()						
							return(True)
					if((bar.highlight==True)and(bar.wtype==WT_BUTTON)):
						# an old highlight needs rubbing out
						bar.highlight=False
						bar.image=bar.non_pressed
						# update that window as well
						bar.parent.image=bar.parent.draw_window()
						self.update_screen()
						return(True)
		# didn't find a thing!
		return(False)

# at the moment, you have to allow for the borders when you create a new window
# sorry about, it's definitly on the TODO list

# a simple class that defines button text, active key and event to run
# when adding buttons to bottom of a window
class button_details:
	def __init__(self,text,key,event):
		"""Set key to None if you don't want a keypress to be
		   added to the keyboard callbacks"""
		self.text=text
		self.key=key
		self.event=event

# define a Window
class Window:
	"""Builds a window. Pass -1 for x or y if you
	   want the window centered"""
	def __init__(self,x,y,width,height,title,draw):
		self.id_number=None
		self.active=True
		self.visible=draw
		self.modal=False
		# set this to false if you want added items to NOT be
		# offset by the border widths
		self.border_offset=True
		self.describe="Window"
		# use info as a storage for any of your own stuff
		# (you can use it to pass variables between function callbacks, for example)
		self.info=None
		# if any widgets need to store data, then we put it here:
		self.data=[]
		self.rect=pygame.Rect((x,y,width,height))
	
		self.rect.w+=(2*WINSZ_SIDE)
		self.rect.h+=WINSZ_TOP+WINSZ_BOT
		# if the passed values for x and y are -1 then
		# place the window at the centre of the screen
		self.centre=False
		if((x==-1)or(y==-1)):
			self.centre_window()
			self.centre=True

		self.caption=title
		# finally, we need a list of the items...
		self.items=[]
		# get an image of the required size
		self.image=pygame.Surface((self.rect.w,self.rect.h))
		# now lets actually draw the window, if needed
		if draw==True:
			# flood fill it with grey and get a standard rectangle
			self.image.fill(BGUI_COL)
			foo=pygame.Rect((0,0,0,0))
			# ok, we start with the sides, with some clever blitting
			# basically blit 4*4 images until you can only do 4*1 ones
			foo.x=0
			foo.y=images[WIN_TL].get_height()
			lrg_draw=int((self.rect.h-foo.y)/4)
			sml_draw=(self.rect.h-foo.y)-(lrg_draw*4)
			offset=self.rect.w-images[WIN_RGT].get_width()
			for bar in range(lrg_draw):
				# blit the large images
				self.image.blit(images[WIN_LFT_LG],foo)
				foo.x+=offset
				self.image.blit(images[WIN_RGT_LG],foo)
				foo.x-=offset	
				foo.y+=4
			# ok, now the final small ones
			if sml_draw!=0:
				for bar in range(sml_draw):
					self.image.blit(images[WIN_LFT],foo)
					foo.x+=offset
					self.image.blit(images[WIN_RGT],foo)
					foo.x-=offset
					foo.y+=1
			# same sort of routine for the top and bottom
			foo.y=0
			foo.x=images[WIN_TL].get_width()
			lrg_draw=int((self.rect.w-foo.x)/4)
			sml_draw=(self.rect.w-foo.x)-(lrg_draw*4)
			offset=self.rect.h-images[WIN_BOT].get_height()
			for bar in range(lrg_draw):
				# again, the large blits (as can be seen from their name)
				self.image.blit(images[WIN_TOP_LG],foo)
				foo.y+=offset
				self.image.blit(images[WIN_BOT_LG],foo)
				foo.y-=offset
				foo.x+=4
			# then the small top/bottom fillers
			if sml_draw!=0:
				for bar in range(sml_draw):
					self.image.blit(images[WIN_TOP],foo)
					foo.y+=offset
					self.image.blit(images[WIN_BOT],foo)
					foo.y-=offset
					foo.x+=1
			# now draw in all of the corners
			foo=pygame.Rect((0,0,0,0))
			self.image.blit(images[WIN_TL],foo)
			foo.y=self.rect.h-images[WIN_BL].get_height()
			self.image.blit(images[WIN_BL],foo)
			foo.x=self.rect.w-images[WIN_BR].get_width()
			self.image.blit(images[WIN_BR],foo)
			foo.y=0
			self.image.blit(images[WIN_TR],foo)
			# right, all that's left to do is draw the text over the title bar
			# firstly render the text in it's own little gfx area
			fonts[FONT_VERA].set_bold(True)
			bar=fonts[FONT_VERA].render(title,True,COL_WINTITLE)
			fonts[FONT_VERA].set_bold(False)
			# set it to centre of title bar
			foo.x=((self.rect.w+images[WIN_TL].get_width())-bar.get_width())/2
			foo.y=((images[WIN_TL].get_height()-bar.get_height())/2)+1
			# render to image
			self.image.blit(bar,foo)
		else:
			# just in case we ever accidentally blit it, we define it anyway:
			self.image=pygame.Surface((0,0))

	def display_window_details(self):
		"""Simple debug routine"""
		print " Window:",self.rect
		for i in self.items:
			print "  Item is:",i.describe
			print "     Rect:",i.rect
	
	def centre_window(self):
		"""Call to reset the rect co-ordinates to the centre
		   of the screen"""
		self.rect.x=(SCREEN_WIDTH-self.rect.w)/2
		self.rect.y=(SCREEN_HEIGHT-self.rect.h)/2
		return(True)
	
	# add an item to the list with this code
	# you may wonder why we essentially rename a python function here.
	# The answer is consistency. We add window items with the same name.
	# also we may wish to extend this function at some point in the future
	def add_item(self,new_item):
		"""Function to add a widget to the window""" 
		self.items.append(new_item)
		# we add to the last item, index is thus len()-1
		index=len(self.items)-1
		# we now have a valid parent to add
		self.items[index].parent=self
		# calling routine will not know about the border, or at least
		# not care about it, so we manually offset into the window
		# you can change this by resetting self.border_offset
		if(self.border_offset==True):
			self.items[index].rect.x+=WINSZ_SIDE
			self.items[index].rect.y+=WINSZ_TOP
		return(index)

	def draw_window(self):
		"""Routine draws the entire window and returns the image"""
		win_img=pygame.Surface((self.rect.w,self.rect.h))
		# blit the current window border across
		win_img.blit(self.image,(0,0))
		# now draw all the items
		for foo in self.items:
			if foo.visible==True:
				x1=foo.rect.x
				y1=foo.rect.y
				win_img.blit(foo.image,(foo.rect.x,foo.rect.y))		
		# thats it! pretty simple really.
		return(win_img)

	def build_button_area(self,button_list,lhs=False):
		"""Function to add buttons to bottom of a window. The window's size
			 is amended to take account of this. The routine adds the buttons,
			 and also the sep unit used.
			 Pass a list of button_details. If the list is empty, nothing is done
			 The buttons are taken but .pop(0), so index 0 is first to be done
			 The final parameter asks to place the last button on the extreme
			 left hand side if equal to True. 
			 Returns a list of index numbers to the buttons if if all ok, False
			 otherwise (and False leaves window as it was to start with)"""
		# any buttons at all?
		if(len(button_list)==0):
			# don't do a thing - thats fine by us!
			return(True)
		bindex=[]
		# ok, let's start to panic here :-o
		# Firstly, we need to work out how many buttons can fit on 1 line
		# get the real width of the window minus it's sides
		width=self.rect.w-(2*WINSZ_SIDE)
		# and the button size:
		bwidth=images[BUTTON_STD].get_width()

		# the basic button layout is as follows:
		# The height of the new window part is as follows:
		# we add a sep bar immediatly below. This is always 2 pixels in height
		# The button holding area below this is always 2*BUTTON_HEIGHT,
		# with the buttons being placed in the centre.
		# The buttons are added from right to left, and from top to bottom
		# they are spaced, with from left to right, (SPACER*2),button etc...
		# firstly, have we enough room for 1 button even?
		if(width<((SPACER*4)+bwidth)):
			# cant do it, so return false
			if(DEBUG_MODE==True):
				print "[GUI]: Couldn't add buttons (window too small)"
			return(False)
		# how many buttons can we add then?
		padding=(SPACER*2)
		totb=(width-padding)/(bwidth+SPACER)
		# hopefully we can get away with only one level of buttons:
		if(totb>=(len(button_list))):
			# yes, all buttons go on the one line
			# start by extending the size of the window and rebuilding the image
			extend_height=(images[BUTTON_STD].get_height()*2)+2
			self.rect.h+=extend_height
			new_image=pygame.Surface((self.rect.w,self.rect.h))
			new_image.fill(BGUI_COL)
			# blit most of the old image:
			new_image.blit(self.image,(0,0),
				(0,0,self.rect.w,self.rect.h-(WINSZ_BOT+extend_height)))
			# blit bottom to the bottom (!)
			new_image.blit(self.image,(0,self.rect.h-WINSZ_BOT),
				(0,self.rect.h-(WINSZ_BOT+extend_height),self.rect.w,WINSZ_BOT))
			# we know need to draw in the sides that are missing.
			# area to draw is actually pretty small. We can assume that there
			# is enough space already on the present window to draw from
			# boy, it sure makes the code a heck of a lot smaller :-)			
			new_image.blit(self.image,(0,(self.rect.h-(extend_height+WINSZ_BOT))),
				(0,WINSZ_TOP,WINSZ_SIDE,extend_height+1))
			new_image.blit(self.image,
				(self.rect.w-WINSZ_SIDE,(self.rect.h-(extend_height+WINSZ_BOT))),
				(self.rect.w-WINSZ_SIDE,WINSZ_TOP,WINSZ_SIDE,extend_height+1))

			# new image is now complete, copy it across
			self.image=new_image
			
			# now we can start to add the various parts. Easiest of all is the sep bar
			# you may question the maths here (how do we know the length is going to be
			# big enough?), but all we after is a width >(2*SPACER), ok (if SPACER is
			# fairly small) because we already tested for button width earlier
			self.add_item(Seperator(
				SPACER,self.rect.h-(extend_height+WINSZ_TOP),
				(self.rect.w-(2*(WINSZ_SIDE+SPACER)))))
				
			# now we add the buttons
			xpos=width-((2*SPACER)+images[BUTTON_STD].get_width())
			ypos=(self.rect.h-(extend_height+WINSZ_TOP))
			ypos+=(extend_height-images[BUTTON_STD].get_height())/2
			while(len(button_list)>0):	
				# get the next button
				button=button_list.pop(0)
				# could be the last button...
				if((len(button_list)==0)and(lhs==True)):
					# amend xpos - real easy
					# TODO: fix horrible -4 hack
					xpos=(SPACER*2)-4
				# build the button
				bwidget=Button(xpos,ypos,button.text)
				bwidget.active=True
				# and then add it
				bindex.append(self.add_item(bwidget))
				# might as well add the callback now...
				# nasty bug, at least check we have a function...
				if(button.event!=None):
					bwidget.callbacks.mouse_lclk=button.event
				# and the keystuff, if needed:
				#if(button.key!=None):
				#	self.lgui.keyboard.add_key(button.key,KMOD_BASE,button.event)
				# reset x position
				xpos-=(2*SPACER)+images[BUTTON_STD].get_width()
		else:
			# TODO: 2 lines of buttons not implemented yet
			# possibly they may never be, as it can look pretty ugly, IMHO
			if(DEBUG_MODE==True):
				print "[GUI]: >1 lines of buttons not implemented in build_button_area()"
			return(False)
		# one last thing. Recentre the window?
		if(self.centre==True):
			self.centre_window()
		# everything went ok. it seems. I leave it to the calling code to
		# deal with making the window modal, etc...
		return(bindex)

class Container():
	"""The container is essentially a window where the window part
	   is not drawn. This means that they cannot be moved (as they
	   have no border to click on)"""
	def __init__(self):
		pass

# what follows is the base class used for the callback functions of the widgets. Every
# widget has one, and you can modify the widgets by pointing mouse_* to different functions
class Callbacks:
	"""Simple class holding callbacks for widgets."""
	def __init__(self,description):
		self.mouse_over=mouse_over_std
		self.mouse_ldown=mouse_ldown_std
		self.mouse_rdown=mouse_rdown_std
		self.mouse_dclick=mouse_dclick_std
		self.mouse_lclk=mouse_lclk_std
		self.mouse_rclk=mouse_rclk_std
		self.describe=description

# now follows widget definitions

# now individual classes for the items contained within the window
# this is the base class that you will only use to generate custom widgets
# in almost all cases you'll use the widgets defined by the library
class Widget:
	"""Base class for widgets: All other widgets should build on this one"""
	def __init__(self,x,y,width,height):
		self.active=True
		self.visible=True
		self.rect=pygame.Rect(x,y,width,height)
		self.wtype=WT_ROOT
		# add callbacks
		self.callbacks=Callbacks("Widget_Callback")
		# set an image up for later
		self.image=False
		# following used to store the parent window of the
		# widget... False if there is no valid parent
		self.parent=False
		self.describe="Widget"
		
# and the simplest of all - a seperator bar
# regardless of width, they all have a height of 2
class Seperator:
	"""Seperator class states and stores details for a seperator"""
	def __init__(self,x,y,width):
		#self.lgui=gui
		self.active=False
		self.visible=True
		self.rect=pygame.Rect(x,y,width,2)
		self.wtype=WT_SEP
		self.image=pygame.Surface((width,2))
		# now blit the 2 colours to the image
		pygame.draw.line(self.image,SEP_DARK,(0,0),(width,0),1)
		pygame.draw.line(self.image,SEP_LIGHT,(0,1),(width,1),1)
		# even sep bars have callbacks!
		self.callbacks=Callbacks("Seperator_Callbacks")
		self.parent=False
		self.describe="Seperator"

# and now a button
class Button:
	"""Init routine to create a button widget. Call with
		 x and y positons, and the text on the button. Returns a
		 button widget item for you to use.
		 Buttons are automagically highlighted when the mouse is
	     over them"""
	def __init__(self,x,y,text):
		self.active=True
		self.visible=True
		self.highlight=False
		self.wtype=WT_BUTTON
		width=images[BUTTON_STD].get_width()
		height=images[BUTTON_STD].get_height()
		self.rect=pygame.Rect(x,y,width,height)
		self.callbacks=Callbacks("Button_Callbacks")
		# get the image, please!
		self.non_pressed,self.pressed=self.draw_button(text)
		# save the text
		self.text=text
		self.image=self.non_pressed
		self.parent=False
		self.describe="Button"
		
	# function to draw a standard button
	def draw_button(self,text):
		"""Just call with the text you want displayed, the
			 routine will draw the button for you. Returns
			 the image that has been drawn AND the highlight button"""
		# make a copy of the button bitmap and the highlight one
		foo=pygame.Surface((images[BUTTON_STD].get_width(),
			images[BUTTON_STD].get_height()))
		bar=pygame.Surface((images[BUTTON_STD].get_width(),
			images[BUTTON_STD].get_height()))
		area=pygame.Rect((0,0,foo.get_width(),foo.get_height()))
		foo.blit(images[BUTTON_STD],area)
		bar.blit(images[BUTTON_HIGH],area)
		# render the text
		txt=fonts[FONT_VERA].render(text,True,COL_BUTTON)
		# centre the text and overlay it
		x=(images[BUTTON_STD].get_width()-txt.get_width())/2
		y=(images[BUTTON_STD].get_height()-txt.get_height())/2
		area=pygame.Rect((x,y,bar.get_width(),bar.get_height()))
		foo.blit(txt,area)
		bar.blit(txt,area)
		return(foo,bar)

# a label is just a plain piece of text
class Label:
	"""Label class stores details for a simple label"""
	def __init__(self,x,y,width,height,text):
		self.active=False
		self.visible=True
		self.rect=pygame.Rect(x,y,width,height)
		self.wtype=WT_LABEL
		self.background_colour=BGUI_COL
		self.text_colour=COL_BLACK
		self.font=FONT_VERA
		self.justification=LEFT_JUSTIFY
		self.text=text
		self.callbacks=Callbacks("Label_Callback")
		# render the image text
		if(self.build_label()==False):
			# well, something went wrong, lets create an empty gfx
			self.image=pygame.Surface((self.rect.w,self.rect.h))
			self.image.fill(self.background_colour)
		self.parent=False
		self.describe="Label"
	
	# code for the following routine taken from the Pygame code repository.
	# written by David Clark, amended by Chris Smith
	def build_label(self):
		"""Called to redraw the text on the label
		   Returns false (and displays message on console) if
		   the new text will not fit the image. (possible on low res)"""
		final_lines=[]
		requested_lines=self.text.splitlines()
		# Create a series of lines that will fit on the provided rectangle
		for requested_line in requested_lines:
			if(fonts[self.font].size(requested_line)[0]>self.rect.w):
				words=requested_line.split(' ')
				# if any of our words are too long to fit, return.
				for word in words:
					if(fonts[self.font].size(word)[0]>=self.rect.w):
						if(DEBUG_MODE==True):
							print "[GUI]: Error: Word (",word,") was too long in label"
							print "              Width was more than ",self.rect.w
						# it went bad :(
						return(False)
				# Start a new line
				accumulated_line=""
				for word in words:
					test_line=accumulated_line+word+" "
					# Build the line while the words fit.
					if(fonts[self.font].size(test_line)[0]<self.rect.w):
						accumulated_line=test_line
					else:
						final_lines.append(accumulated_line)
						accumulated_line=word+" "
				final_lines.append(accumulated_line)
			else:
				final_lines.append(requested_line)
		# Let's try to write the text out on the surface.
		self.image=pygame.Surface((self.rect.w,self.rect.h))
		self.image.fill(self.background_colour)
		accumulated_height=0
		for line in final_lines:
			if(accumulated_height+fonts[self.font].size(line)[1]>=self.rect.h):
				print "[GUI]: Error: Text string too tall in label"
				print "              ah=",accumulated_height," h=",self.rect.h
				return(False)
			if(line!=""):
				tempsurface=fonts[self.font].render(line,1,self.text_colour)
				if self.justification==LEFT_JUSTIFY:
					self.image.blit(tempsurface,(0,accumulated_height))
				elif self.justification==CENTRE_HORIZ:
					self.image.blit(tempsurface,((self.rect.w-tempsurface.get_width())/2,accumulated_height))
				elif self.justification==RIGHT_JUSTIFY:
					self.image.blit(tempsurface,(self.rect.w-tempsurface.get_width(),accumulated_height))
				else:
					if(DEBUG_MODE==True):
						print "[GUI]: Error: Invalid justification value in label"
					return(False)
			accumulated_height+=fonts[self.font].size(line)[1]
		return(True)

# a simple 2d image
class Image:
	"""Image class states and stores details for a simple image
	   A pretty simple routine
	   You'll normally use the BuildImage routine to get an image"""	
	def __init__(self,x,y,width,height,image):
		self.active=True
		self.visible=True
		self.rect=pygame.Rect(x,y,width,height)
		self.wtype=WT_IMAGE
		# add the usual callbacks
		self.callbacks=Callbacks("SPQR_Image_Callback")
		# image will be cropped if it's bigger than the supplied co-ords
		self.image=pygame.Surface((width,height))
		self.image.blit(images[image],(0,0))
		self.parent=False
		self.describe="SPQR_Image"

# here's where the more complex routines start. First of, still a fairly
# easy one - a clickable checkbox
# since the checkbox needs to update the screen, we pass another
# parameter - the GUI update routine
class CheckBox:
	def __init__(self,ucode,x,y,initial):
		"""You need to pass the following parameters to the init() routine:
		   x,y - the offset into the window
		   initial - a boolean describing the start status of the widget,
		   True meaning that there is a tick in the box"""
		self.update=ucode
		self.rect=(x,y,CHKBOX_SIZE,CHKBOX_SIZE)
		self.active=True
		self.visible=True
		# width and height are taken from defines
		self.rect=pygame.Rect(x,y,CHKBOX_SIZE,CHKBOX_SIZE)
		self.wtype=WT_CHECK
		# status is the inital boolean value
		self.status=initial
		# add callbacks
		self.callbacks=Callbacks("CheckBox_Callback")
		# automatically add it's own click callback
		self.callbacks.mouse_lclk=self.clicked
		# sometimes you'll need to call another routine as well
		# as updating the graphic. Let's set that here as blank
		self.after_click=null_routine
		self.after_click_status=False
		# set an image up for later
		if(self.status==True):
			self.image=images[CHECK_YES]
		else:
			self.image=images[CHECK_NO]
		# following used to store the parent window of the
		# widget... False if there is no valid parent
		self.parent=False
		self.describe="CheckBox"
	
	def clicked(self,handle,x,y):
		"""Called by the gui routine when clicked. Just
		   updates it's own gfx. In the parent window"""
		if(self.status==True):
			self.status=False
			self.image=images[CHECK_NO]
		else:
			self.status=True
			self.image=images[CHECK_YES]
		# the image will have to be updated.
		# just update the window image
		# a slight optimization: just update the window image, rather
		# than re-drawing the whole window
		self.parent.image.blit(self.image,(self.rect.x,self.rect.y))
		# update screen here
		self.update()
		# do we need to do anything else?
		if(self.after_click_status==True):
			# yes, do it
			self.after_click(lgui,handle,xpos,ypos)
		return(True)
		
	def add_after_click(self,routine):
		"""Add routine to be called when left mouse clicked"""
		self.after_click_status=True
		self.after_click=routine
		return(True)

# a classic slider widget
class Slider:
	"""Slider class states and stores details for a slider
	   This is where the widgets start to get complicated
	   Call with the following arguments:
	   ucode - routine that updates the screen
	   x/y   - position of slider in window
	   width - width of entire widget
	   start - value on lhs of widget
	   end   - value on rhs of widget
	   initial - initial value of slider"""
	def __init__(self,ucode,x,y,width,start,end,initial):
		self.update=ucode
		self.active=True
		self.visible=True
		# width is at least what the gfx width is
		if(width<images[GUI_SLIDER].get_width()):
			width=images[GUI_SLIDER].get_width()
		self.rect=pygame.Rect(x,y,width,images[GUI_SLIDER].get_height())
		# we have to check wether the slider knob is being pressed
		# or if it's some other part of the widget 
		self.knob_rect=pygame.Rect(0,0,
			images[GUI_SLIDER].get_width(),images[GUI_SLIDER].get_height())
		self.wtype=WT_SLIDER
		# some more specific slider variables
		# just check the range is ok
		if(start>end):
			# swap the values
			tmp=start
			start=end
			end=tmp
		self.left_value=start
		self.right_value=end
		# also, check initial is ok, else we place it at one end
		if(initial<start):
			initial=start
		elif(initial>end):
			initial=end
		self.current_value=initial
		# remember that the width of the bar is width of widget -
		# width of slider, since the slider 'overhangs' the bar at
		# both ends of the bar (the left part on the left, and the same
		# on the right, by half the slider width)
		self.slide_bar_width=self.rect.w-images[GUI_SLIDER].get_width()
		self.pixel_increment=(float)(end-start)/(float)(width)
		# add callbacks
		self.callbacks=Callbacks("Slider_Callback")
		# mainly with a slider you'll let it do it's own thing
		self.callbacks.mouse_ldown=self.slider_mouse_ldown
		# set an image up for later
		self.image=pygame.Surface((width,self.rect.h))
		self.draw_slider()
		# following used to store the parent window of the
		# widget... False if there is no valid parent
		self.parent=False
		# sometimes you'll want to call a function every time the
		# slider value is set... here are the dat points
		self.update_function_valid=False
		self.update_function=null_routine
		self.describe="Slider"

	def draw_slider(self):
		"""Helper routine, draws the slider knob. Called by both
		   the initial routine and the slider callback function"""
		# There are 3 parts here: the slider itself, and then the
		# bars to the left (in blue) and to the right (in normal colors)
		# start by flood filling the gui color
		self.image.fill(BGUI_COL)
		# now draw the bars in
		spoint=(float)(self.current_value)/(float)(self.right_value-self.left_value)
		spoint=(int)(spoint*self.slide_bar_width)
		# make sure bars are in middle of slider
		yoff=(images[GUI_SLIDER].get_height()/2)-2
		# also, allow for fact slide bar is not as long as the widget width
		# becuase the slider know 'overhangs'. To make things easier, we just
		# adjust the middle point by half the slider knob width
		spoint+=images[GUI_SLIDER].get_width()/2
		# blue bar is from left hand side up to the spoint
		pygame.draw.line(self.image,SLIDER_BDARK,(0,yoff),(spoint,yoff),1)
		pygame.draw.line(self.image,SLIDER_BDARK,(0,yoff),(0,yoff+4),1)
		pygame.draw.line(self.image,SLIDER_BDARK,(0,yoff+4),(spoint,yoff+4),1)
		pygame.draw.line(self.image,SLIDER_LIGHT,(1,yoff+1),(spoint,yoff+1),1)
		pygame.draw.line(self.image,SLIDER_MEDIUM,(1,yoff+2),(spoint,yoff+2),1)
		pygame.draw.line(self.image,SLIDER_DARK,(1,yoff+3),(spoint,yoff+3),1)
		# thats the left hand side taken care of, now the right...
		pygame.draw.line(self.image,SLIDER_BLIGHT,(spoint,yoff),(self.rect.w-1,yoff),1)
		pygame.draw.line(self.image,SLIDER_BLIGHT,(self.rect.w-1,yoff),(self.rect.w-1,yoff+4),1)
		pygame.draw.line(self.image,SLIDER_BLIGHT,(spoint,yoff+4),(self.rect.w-1,yoff+4),1)
		pygame.draw.line(self.image,SLIDER_BMED1,(spoint,yoff+1),(self.rect.w-1,self.rect.y+1),1)
		pygame.draw.line(self.image,SLIDER_BMED2,(spoint,yoff+2),(self.rect.w-1,self.rect.y+2),1)
		pygame.draw.line(self.image,SLIDER_BMED2,(spoint,yoff+3),(self.rect.w-1,self.rect.y+3),1)
		# that was a lot of line drawing... now we just have to blit the
		# slider bar itself, in the right place
		xpos=spoint-(images[GUI_SLIDER].get_width()/2)
		self.image.blit(images[GUI_SLIDER],(xpos,0))
		# set knob_rect so we can catch events as well
		self.knob_rect.x=xpos
		# and that's it! updating is all up to you...
		return(True)

	def get_value(self):
		"""Returns current setting of slider. Although internally value
		   is sometimes a float, this always returns an int"""
		return((int)(self.current_value))

	def set_update_function(self,code):
		"""Set callback function, called every time the value
		   of the slider is called. Must be a usual callback function"""
		self.update_function_valid=True
		self.update_function=code
		return(True)
		
	def kill_update_function(self,code):
		"""Call if you ever want to cancel the slider update function"""
		self.update_function_valid=False
		self.update_function=null_routine
		return(True)

	def slider_mouse_ldown(self,handle,xpos,ypos):
		"""Called when user clicks down with the mouse over a slider knob
			 Captures all input until user releases mouse button"""
		# first of all we check to see wether it was over the
		# slider knob or not...
		if((xpos>self.knob_rect.x)and(xpos<(self.knob_rect.x+self.knob_rect.w))):
			# ok, enter a loop where we catch all events until the left
			# mouse button is depressed
			# we only handle mouse moves though, everything else is ignored
			while(True):
				event=pygame.event.wait()
				if((event.type==MOUSEBUTTONUP)and(event.button==1)):
					# time to exit
					return(True)
				elif((event.type==MOUSEMOTION)):
					# we only need to look at x movement:
					xdiff=event.rel[0]	
					# any movement?
					if(xdiff!=0):
						# extra bit of bling, as used by many wm's:
						# only move the slider in a given direction as long as the
						# mouse is past the middle of the slider knob in that
						# direction. I.e. to drag left, the mouse must be to the
						# left of the middle of the slider knob :-)
						move=True
						middle=self.parent.rect.x+self.rect.x+self.knob_rect.x
						middle+=(self.knob_rect.w/2)
						# work out what side we are moving and calculate:
						if(xdiff<0):
							# moving left?
							if(event.pos[0]>middle):
								# don't do it
								move=False
						else:
							# must be moving right...
							if(event.pos[0]<middle):
								move=False
						if(move==True):
							# yes, so move the bar:
							old=self.current_value
							self.current_value+=(xdiff*self.pixel_increment)
							# test for still in range:
							if(self.current_value<self.left_value):
								self.current_value=self.left_value
							elif(self.current_value>self.right_value):
								self.current_value=self.right_value
							# need to update?
							if(old!=self.current_value):
								# update the image
								self.draw_slider()
								x=self.parent.rect.x+self.rect.x
								y=self.parent.rect.y+self.rect.y						
								handle.parent.image.blit(self.image,(self.rect.x,self.rect.y))
								self.update()	
								# *finally*, we may have asked for an extra callback...
								if(self.update_function_valid==True):
									# do the callback
									self.update_function(lgui,handle,xpos,ypos)
		# nothing happened, but be graceful about it anyway
		return(True)

# some widgets are used in similar ways when we use them. Most
# labels, for example, are just simple text. For these instances
# we can use the following helper routines

def BuildLabel(text):
	"""Helper function to build a label given just the text.
	   Uses standard font, which is FONT_VERA. Returns the new label"""
	# get the size
	w,h=fonts[FONT_VERA].size(text)
	# and then create
	# note: annoyingly enough, despite asking what size the font is, if
	# I render to an image of that size, it doesn't work. So we have to add 1
	# any answers to this one, or have I missed something?
	return(Label(0,0,w,h+1,text))

def BuildImage(picture):
	"""Pass your own image. You'll probably need to set the
	   x/y rectangle attributes"""
	new=Image(0,0,0,0,0)
	# now amend that image
	new.rect.w=picture.get_width()
	new.rect.h=picture.get_height()
	new.image=picture
	return(new)

def BuildImageAlpha(lgui,picture):
	"""As BuildImage, but blits alpha image over gui color
	   This is for when you have an alpha image and you
	   want to make sure the background fits with the GUI"""
	w=picture.get_width()
	h=picture.get_height()
	# create our initial image and make it the right color
	piccy=pygame.Surface((w,h))
	piccy.fill(BGUI_COL)
	# now blit over the real image
	piccy.blit(picture,(0,0))
	# and thats almost it
	return(BuildImage(piccy))

# these are the standard callbacks, they should never be called
# they are here to prevent an exception should an unregistered
# event ever be called
# in truth, these are checked against and not called if they match
# if these ever get called, we have a serious error going on!
def mouse_over_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_over_std called"
	return(False)

def mouse_ldown_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_ldown_std called"
	return(False)

def mouse_rdown_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_rdown_std called"
	return(False)

def mouse_dclick_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_dclick_std called"
	return(False)

def mouse_lclk_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_lclk_std called"
	return(False)

def mouse_rclk_std(handle,x,y):
	if(DEBUG_MODE==True):
		print "[GUI]: Error: mouse_rclk_std called"
	return(False)
	
def null_callback(handle,xpos,ypos):
	"""Another filler routine to handle blank callbacks"""
	if(DEBUG_MODE==True):
		print "[GUI]: Null routine called"
	return(False)

# callbacks for the messegebox routines (if needed)
def msgbox_ok(gui,handle,xpos,ypos): 
	"""Callback for messagebox ok button"""
	gui.callback_temp=BUTTON_OK
	return(BUTTON_OK)

def msgbox_cancel(gui,handle,xpos,ypos):
	"""Callback for messagebox cancel button"""
	gui.callback_temp=BUTTON_CANCEL
	return(BUTTON_CANCEL)

def msgbox_yes(gui,handle,xpos,ypos):
	"""Callback for messagebox yes button"""
	gui.callback_temp=BUTTON_YES
	return(BUTTON_YES)

def msgbox_no(gui,handle,xpos,ypos):
	"""Callback for messagebox no button"""
	gui.callback_temp=BUTTON_NO
	return(BUTTON_NO)

def msgbox_quit(gui,handle,xpos,ypos):
	"""Callback for messagebox quit button"""
	gui.callback_temp=BUTTON_QUIT
	return(BUTTON_QUIT)

def msgbox_ignore(gui,handle,xpos,ypos):
	"""Callback for messagebox ignore button"""
	gui.callback_temp=BUTTON_IGNORE
	return(BUTTON_IGNORE)

