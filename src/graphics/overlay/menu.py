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
        font = pyglet.font.load(font_name, 48)
        self.title_text = pyglet.font.Text(font, text=title, x=x, y=y,
                                           color=cnormalize(dark_orange),
                                           halign='center', valign='center')
        self.selected_index = 0

    def reset(self):
        self.selected_index = 0
        self.items[self.selected_index].selected = True

    def add_item(self, item):
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

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            item.draw(i == self.selected_index)


class MenuItem(object):
    def __init__(self, label, callback, font_name=None):
        self.callback = callback
        font = pyglet.font.load(font_name, 18)
        self.text = pyglet.font.Text(font, text=label, color=cnormalize(grey),
                                     halign='center', valign='center')

    def has_point(self, x, y):
        my_x = self.text.x
        my_y = self.text.y
        my_w = self.text.width
        my_h = self.text.height
        return x >= my_x - my_w/2 and x <= my_x + my_w/2 and \
                y >=my_y - my_h/2 and y <= my_y + my_h/2 

    def draw(self, selected):
        if selected:
            self.text.color = cnormalize(white)
        else:
            self.text.color = cnormalize(grey)
        self.text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.callback()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.callback()


class ToggleMenuItem(MenuItem):
    def __init__(self, label, value, callback, font_name=None):
        self.value = value
        self.label = label
        self.callback = callback
        super(ToggleMenuItem, self).__init__(self.get_label(),
                                             self.callback,
                                             font_name)

    def get_label(self):
        return self.label + (self.value and ': ON' or ': OFF')

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.value = not self.value
            self.text.text = self.get_label()
            self.callback(self.value)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.value = not self.value
            self.text.text = self.get_label()
            self.callback(self.value)


#class TextInputMenuItem(MenuItem):
#    def __init__(self, label, value, callback):
#        self.label = label
#        self.value = value
#        self.callback = callback
#        self.text_input = TextInput(
#        super(TextInputMenuItem, self).__init__(self.label, self.callback)
#
#    def on_key_press(self, symbol, modifiers):
#        pass
