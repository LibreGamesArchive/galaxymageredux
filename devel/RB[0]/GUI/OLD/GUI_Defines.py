#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# we need a few pygame globals
from pygame.locals import *

# here is where we set all the variables as required by the Handy GUI library

# handy for testing
DEBUG_MODE		=	True
SCREEN_WIDTH	=	640
SCREEN_HEIGHT	=	480

# set this next one to true if you want a rh mouse click to exit
RMOUSE_END		=	True
# menu icons are always squares
ICON_SIZE		=	24
# checkbox size goes here (always a square)
CHKBOX_SIZE		=	13

# sizes of various gradiant bars used in ItemList widget
GRADBAR_SIZES	=	[64,96,128]
GRADBAR_WIDTH	=	128

# fonts used by the game
FONT_VERA		=	0

# and their sizes
FONT_SMALL		=	12
FONT_STD		=	14
FONT_LARGE		=	16
FONT_XLARGE		=	48
FONT_HUGE		=	64

# index numbers of windows that are always present
WIN_MENU		=	0
WIN_INFO		=	1

# images loaded by the gui system, used to draw the gui
# mmm... quite a few images here
# always start with the alpha images
GUI_SLIDER		=	0
GUI_CLICKER		=	1
ARROW_UP		=	2
ARROW_DOWN		=	3
# icons for menu start here
ICON_LOAD		=	4
# just in case it ever gets blitted:
ICON_NONE		=	ICON_LOAD
ICON_SAVE		=	5
ICON_PREFS		=	6
ICON_EXIT		=	7
ICON_SENATE		=	8
ICON_MILITARY	=	9
ICON_STATS		=	10
ICON_ABOUT		=	11
ICON_HELP		=	12
ICON_NEW		=	13
ICON_DEBUG		=	14
ICON_CONSOLE	=	15
ICON_CITY		=	16
IMG_MUSIC		=	17

IALPHA_END		=	17
WIN_TL			=	IALPHA_END+1
WIN_LFT			=	IALPHA_END+2
WIN_BL			=	IALPHA_END+3
WIN_BOT			=	IALPHA_END+4
WIN_BR			=	IALPHA_END+5
WIN_RGT			=	IALPHA_END+6
WIN_TR			=	IALPHA_END+7
WIN_TOP			=	IALPHA_END+8
WIN_LFT_LG		=	IALPHA_END+9
WIN_BOT_LG		=	IALPHA_END+10
WIN_RGT_LG		=	IALPHA_END+11
WIN_TOP_LG		=	IALPHA_END+12
BUTTON_STD		=	IALPHA_END+13
BUTTON_HIGH		=	IALPHA_END+14
CHECK_YES		=	IALPHA_END+15
CHECK_NO		=	IALPHA_END+16

# more GUI images
SCROLL_TOP		=	IALPHA_END+17
SCROLL_BOTTOM	=	IALPHA_END+18
SCHAN_MIDDLE	=	IALPHA_END+19
SCHAN_TOP		=	IALPHA_END+20
SCHAN_BOTTOM	=	IALPHA_END+21
SCHAN_FILL		=	IALPHA_END+22
GRADBAR			=	IALPHA_END+23
GRADBAR_MED		=	IALPHA_END+24
GRADBAR_LGE		=	IALPHA_END+25
OPTM_LHAND		=	IALPHA_END+26
OPTM_RHAND		=	IALPHA_END+27
# an image purely for experimentation with
IMG_TEST		=	IALPHA_END+28
# some wallapers
IMG_WALL1		=	IALPHA_END+29
# sometimes, there really is no image
IMG_NONE		=	0

# number of milliseconds between clicks in a double-click
# (400 is the Gnome standard)
DCLICK_SPEED	=	400

# mouse events as seen by the gui
MOUSE_NONE		=	0
MOUSE_OVER		=	1
MOUSE_LCLK		=	2
MOUSE_RCLK		=	3
MOUSE_DCLICK	=	4
MOUSE_LDOWN		=	5
MOUSE_RDOWN		=	6

# standard buttons that the messagebox function uses
BUTTON_FAIL		=	0
BUTTON_OK		=	1
BUTTON_CANCEL	=	2
BUTTON_YES		=	4
BUTTON_NO		=	8
BUTTON_QUIT		=	16
BUTTON_IGNORE	=	32

# standard widget types
WT_ROOT			=	0
WT_BUTTON		=	1
WT_LABEL		=	2
WT_IMAGE		=	3
WT_SEP			=	4
WT_CHECK		=	5
WT_MENU			=	6
WT_SLIDER		=	7
WT_SCROLLAREA	=	8
WT_ITEMLIST		=	9
WT_OPTMENU		=	10

# text layout types
LEFT_JUSTIFY	=	0
RIGHT_JUSTIFY	=	1
CENTRE_HORIZ	=	2

# offsets for when we draw a pop-up menu to screen
MENU_X_OFFSET	=	2
MENU_Y_OFFSET	=	23
# amount of pixels left empty on lhs of any menu
MNU_LSPACE		=	4
# amount of pixels padded out above and below a menu entry
# (distance between menu texts is twice this number)
MNU_HSPACE		=	4
# pixels on rhs left blank on menu
MNU_RSPACE		=	8
# minimum gap between menu text and key text in menu dropdown
MNU_KEY_GAP		=	12
# any other random spacing we need
SPACER			=	8
HALFSPCR		=	4
QTRSPCR			=	2
# minimum height of scroll area handle
SCAREA_MINH		=	32
# sizes of the window borders
WINSZ_SIDE		=	6
WINSZ_TOP		=	24
WINSZ_BOT		=	6

# alpha is from 0 to 255, where 0 is transparent
MENU_ALPHA		=	64
# colour of the highlight
MENU_HLCOL		= 	(170,83,83)
MENU_HBORDER	=	6

# define all the colours we use
BGUI_COL		=	(238,238,230)
BGUI_HIGH		=	(227,219,213)
MENU_COL		=	(246,246,246)
MENU_BDR_COL	=	(220,220,220)
MENU_CNR_COL	=	(194,194,194)
MENU_TXT_COL	=	(0,0,0)
COL_BLACK		=	(0,0,0)
COL_WHITE		=	(255,255,255)
COLG_BLUE		=	(81,93,151)
COLG_RED		=	(171,84,84)
COLG_GREEN		=	(112,154,104)
COLG_BHIGH		=	(116,133,216)
COLG_RHIGH		=	(254,120,120)
COLG_GHIGH		=	(160,220,149)
COL_BUTTON		=	(0,0,0)
COL_WINTITLE	=	(0,0,0)
SLIDER_LIGHT	=	(116,133,216)
SLIDER_MEDIUM	=	(98,113,183)
SLIDER_DARK		=	(81,93,151)
SLIDER_BDARK	=	(70,91,110)
SLIDER_BLIGHT	=	(170,156,143)
SLIDER_BMED1	=	(192,181,169)
SLIDER_BMED2	=	(209,200,191)
SCROLL_BORDER	=	(170,156,143)
SCROLL_MIDDLE	=	(209,200,191)
SEP_DARK		=	(154,154,154)
SEP_LIGHT		=	(248,252,248)
OPTM_BDARK		=	(190,190,180)
WALLPAPER		=	(160,160,185)

# stop looking for a double-click when we get this event
EVENT_DC_END	=	USEREVENT+1


