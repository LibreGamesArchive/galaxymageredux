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

from graphics.colors import *
import overlay
import config


class Menu(overlay.Overlay):
    def __init__(self, title, x, y, font_name=None):
        self.items = []
        self.font_name = font_name
        font = pyglet.font.load(font_name, 48)
        self.title_text = pyglet.font.Text(font, text=title, x=x, y=y,
                                           color=cnormalize(dark_orange),
                                           halign='center', valign='center')
        self.selected_index = 0

    def reset(self):
        self.selected_index = 0

    def add_items(self, items):
        for item in items:
            item.doc.set_style(0, 0, {'font_name': self.font_name})
            item.text.x = self.title_text.x
            item.text.y = self.title_text.y - (len(self.items) + 2) * 40
            self.items.append(item)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.DOWN:
            self.selected_index += 1
        elif symbol == pyglet.window.key.UP:
            self.selected_index -= 1
        else:
            self.items[self.selected_index].on_key_press(symbol, modifiers)
        self.selected_index = min(max(self.selected_index, 0),
                                  len(self.items) - 1)

    def on_mouse_press(self, x, y, dx, dy):
        for index in range(len(self.items)):
            if self.items[index].has_point(x, y):
                self.items[index].on_mouse_press(x, y, dx, dy)

    def on_mouse_motion(self, x, y, button, modifiers):
        for index in range(len(self.items)):
            if self.items[index].has_point(x, y):
                self.selected_index = index

    def on_text(self, text):
        self.items[self.selected_index].on_text(text)

    def on_text_motion(self, motion):
        self.items[self.selected_index].on_text_motion(motion)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            item.draw(i == self.selected_index)


class MenuItem(object):
    def __init__(self, label, callback):
        self.doc = pyglet.text.document.UnformattedDocument(label)
        self.doc.set_style(0, 0, {'color': grey})
        self.doc.set_style(0, 0, {'font_size': 18})
        self.text = pyglet.text.layout.IncrementalTextLayout(self.doc, 400, 40)
        self.text.valign = 'center'
        self.text.halign = 'center'
        self.callback = callback
        self.selected = False

    def has_point(self, x, y):
        my_x = self.text.x
        my_y = self.text.y
        my_w = self.text.content_width
        my_h = self.text.content_height
        return x >= my_x - my_w/2 and x <= my_x + my_w/2 and \
                y >= my_y - my_h/2 and y <= my_y + my_h/2 

    def draw(self, selected):
        if selected:
            self.doc.set_style(0, 0, {'color': white})
        else:
            self.doc.set_style(0, 0, {'color': grey})
        self.text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.callback()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.callback()

    def on_text(self, text):
        pass

    def on_text_motion(self, motion):
        pass
            

class InputMenuItem(MenuItem):
    def __init__(self, label, value, callback):
        self.label = label + ': '
        MenuItem.__init__(self, self.label + str(value), callback)
        self.caret_position = len(self.label)
        self.caret = pyglet.text.caret.Caret(self.text)
        self.caret.color = grey[:-1]
        self.caret.position = len(self.doc.text)

    def on_text(self, text):
        if ord(text) != 13:
            self.caret.on_text(text)
            self.callback(self.doc.text[self.caret_position:])

    def on_text_motion(self, motion):
        if (motion == pyglet.window.key.MOTION_BACKSPACE or \
                motion == pyglet.window.key.MOTION_LEFT) and \
                self.caret.position != self.caret_position:
            self.caret.on_text_motion(motion)
            self.callback(self.doc.text[self.caret_position:])

        if motion == pyglet.window.key.MOTION_DELETE or \
                motion == pyglet.window.key.MOTION_RIGHT:
            self.caret.on_text_motion(motion)
            self.callback(self.doc.text[self.caret_position:])

    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass


class ToggleMenuItem(MenuItem):
    def __init__(self, label, value, callback):
        self.value = value
        self.label = label
        MenuItem.__init__(self, self.get_label(), callback)

    def get_label(self):
        return self.label + (self.value and ': ON' or ': OFF')

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.value = not self.value
            self.doc.text = self.get_label()
            self.callback(self.value)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.value = not self.value
            self.doc.text = self.get_label()
            self.callback(self.value)
