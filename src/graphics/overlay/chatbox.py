# LICENSE:
#
# Copyright (c) 2007-2008 A. Joseph Hager and Redux contributors.
#
# Redux is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License, as published by the
# Free Software Foundation.
# 
# Redux is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along
# with Redux; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


import pyglet

from graphics import colors
import overlay
import config


class ChatBox(overlay.Overlay):
    def __init__(self, x, y, width, height, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

        # Scrollable text display for chat messages.
        self.text_display = pyglet.text.document.UnformattedDocument()
        self.text_display.set_style(0, 0, {"color": (114, 159, 207, 255)})
        self.td_layout = pyglet.text.layout.IncrementalTextLayout(self.text_display,
                                                                  width, height,
                                                                  multiline=True)
        self.td_layout.x = x
        self.td_layout.y = y

        # Text input with a caret for nice editing.
        self.text_input = pyglet.text.document.UnformattedDocument()
        self.text_input.set_style(0, 0, {"color": (163, 163, 163, 255)})
        self.ti_layout = pyglet.text.layout.IncrementalTextLayout(self.text_input,
                                                                  width,
                                                                  20)
        self.ti_layout.x = x
        self.ti_layout.y = y+25
        self.ti_layout.selection_color = (46, 52, 54, 255)
        self.ti_layout.selection_background_color = (163, 163, 163, 255)
        self.ti_caret = pyglet.text.caret.Caret(self.ti_layout)
        self.ti_caret.color = (163, 163, 163)

    def add_text(self, text):
        self.text_display.insert_text(0, text + "\n")

    def on_text(self, text):
        if ord(text) != 13: # Hack. Do not want hard returns showing up.
            self.ti_caret.on_text(text)

    def on_text_motion(self, motion):
        self.ti_caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        self.ti_caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.callback(self.text_input.text)
            self.text_input.text = ""
            self.ti_caret.position = 0

    def on_mouse_press(self, x, y, button, modifiers):
        self.ti_caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.ti_caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.td_layout.view_y += scroll_y * 2

    def on_activate(self):
        self.ti_caret.on_activate()

    def on_deactivate(self):
        self.ti_caret.on_deactivate()

    def draw(self):
        self.td_layout.draw()
        self.ti_layout.draw()
