import pygame
from pygame.locals import *

import event

class App(object):
    def __init__(self, screen, event_handler):

        self.screen = screen
        self.event_handler = event_handler
        self.event_handler.gui = self
        self.event_handler.all_guis.append(self)
        self.widgets = []

        #self.dispatch = event.Dispatcher()

        self.font = pygame.font.Font(None, 32)
        self.visible = True

    def get_font(self):
        return self.font

    def get_screen(self):
        return self.screen

    def get_mouse_pos(self):
        #return pygame.mouse.get_pos()
        return self.event_handler.mouse.get_pos()

    def add_widget(self, widg):
        if not widg in self.widgets:
            self.widgets.insert(0, widg)


    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mousedown(button, name):
                    return True
        return False

    def handle_mouseup(self, button, name):
        """Callback for mouse release events from the event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mouseup(button, name):
                    return True
        return False

    def handle_mousehold(self, button, name):
        """Callback for mouse hold events from the event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mousehold(button, name):
                    return True
        return False

    def handle_mousemotion(self, change):
        """Callback for mouse motion events from event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mousemotion(change):
                    return True

    def handle_uncaught_event(self, event):
        """Callback for uncaught_event events from event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_uncaught_event(event):
                    return True
        return False

    def handle_keydown(self, key, string):
        """Callback for key press events from event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_keydown(key, string):
                    return True
        return False

    def handle_keyup(self, key, string):
        """Callback for key release events from event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_keyup(key, string):
                    return True
        return False

    def handle_keyhold(self, key, string):
        """Callback for key hold events from event_handler."""
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_keyhold(key, string):
                    return True
        return False

    def next_widget(self):
        """Cycle widgets so next widget is top one."""
        for i in self.widgets[1:]:
            if i.visible:
                self.set_top_widget(i)
                return

    def set_top_widget(self, widg):
        """Moves widget 'widg' to top position."""
        if widg in self.widgets:
            self.widgets.remove(widg)
        self.widgets.insert(0, widg)
        for i in self.widgets:
            if i.visible:
                if not i == widg:
                    i.unfocus()

    def render(self):
        self.widgets.reverse()
        for i in self.widgets:
            if i.visible: i.render()
        self.widgets.reverse()

class Widget(object):
    def __init__(self, parent):
        self.parent = parent
        self.parent.add_widget(self)

        self.pos = 0,0
        self.size = 0,0
        self.dispatch = event.Dispatcher()

        self.visible = True
        self.font = self.parent.get_font()

        self._mhold = False
        self._mhover = False
        self.key_active = False
        self.key_hold_lengths = {}
        self.khl = 200 #milliseconds to hold keys for repeat!

    def mouse_on_me(self):
        return pygame.Rect(self.pos, self.size).collidepoint(self.parent.get_mouse_pos())

    def focus(self):
        """Focus this widget so it is at the top of rendering and event calls."""
        self.parent.set_top_widget(self)
        self.key_active = True
        self.dispatch.fire("focus")
        self._mhover = self.mouse_on_me()

    def unfocus(self):
        """Remove the widget's focus."""
        self.key_active=False
        self.key_hold_lengths = {}
        self.dispatch.fire("unfocus")
        self._mhold=False
        self._mhover=False

    def handle_mousedown(self, button, name):
        """Handle a mouse down event from the App."""
        self._mhover = self.mouse_on_me()
        if name == "left":
            if self._mhover:
                self._mhold = True
                self.focus()
                self.dispatch.fire("press")
                return True
            self.unfocus()

    def handle_mouseup(self, button, name):
        """Handle a mouse release event from the App."""
        self._mhover = self.mouse_on_me()
        if name == "left":
            if self._mhold and self._mhover:
                self._mhold = False
                self.dispatch.fire("click")
                return True

    def handle_mousehold(self, button, name):
        """Handle a mouse hold event from the App."""
        if name == "left":
            if self._mhold:
                return True

    def handle_mousemotion(self, change):
        """Handle a mouse motion event from the App."""
        n = self._mhover
        self._mhover = self.mouse_on_me()
        if n == False and self._mhover == True:
            self.dispatch.fire("hover")
            for i in self.parent.widgets:
                if not i == self:
                    i._mhover = False
        elif n == True and self._mhover == False:
            self.dispatch.fire("unhover")
        return self._mhover

    def can_handle_key(self, key, string):
        """Return whether key/string is used by this widget."""
        return False

    def handle_keydown(self, key, string):
        """Handle a key down event from the App."""
        if self.can_handle_key(key, string):
            if self.key_active:
                self.dispatch.fire("keypress", key, string)
                return True

    def handle_keyhold(self, key, string):
        """Handle a key hold event from the App."""
        if self.can_handle_key(key, string):
            if self.key_active:
                if key in self.key_hold_lengths:
                    if time.time() - self.key_hold_lengths[key] >= self.khl*0.001:
                        self.handle_keydown(key, string)
                        self.key_hold_lengths[key] = time.time()
                else:
                    self.key_hold_lengths[key] = time.time()
                return True

    def handle_keyup(self, key, string):
        """Handle a key release event from the App."""
        if self.can_handle_key(key, string):
            if self.key_active:
                if key in self.key_hold_lengths:
                    del self.key_hold_lengths[key]
                return True

    def handle_uncaught_event(self, event):
        """Handle any non mouse or key event from the App."""
        pass

    def render(self):
        pass


class Container(Widget, App):
    def __init__(self, parent, size, pos, background_image=None):
        Widget.__init__(self, parent)
        self.size = size
        self.pos = pos
        self.widgets = []

        self.dispatch = event.Dispatcher()

        self.font = self.parent.get_font()

        self.screen = pygame.Surface(size).convert_alpha()
        self.bg_color = (0,0,0,0)
        self.background_image = background_image

        self.clear_screen()

        self.dispatch.bind('hover', self.swap_red)
        self.dispatch.bind('unhover', self.swap_blue)

    def swap_red(self, *rgs):
        self.bg_color = (255,0,0,150)
    def swap_blue(self, *args):
        self.bg_color = (0,0,255,150)

    def clear_screen(self):
        if self.background_image:
            self.screen = self.background_image.copy()
        else:
            self.screen.fill(self.bg_color)

    def get_mouse_pos(self):
        x,y = self.parent.get_mouse_pos()
        x = x - self.pos[0]
        y = y - self.pos[1]
        return x,y

    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        Widget.handle_mousedown(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mousedown(button, name):
                    return True
        return False

    def handle_mouseup(self, button, name):
        """Callback for mouse release events from the event_handler."""
        Widget.handle_mouseup(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mouseup(button, name):
                    return True
        return False

    def handle_mousehold(self, button, name):
        """Callback for mouse hold events from the event_handler."""
        if Widget.handle_mousehold(self, button, name):
            App.handle_mousehold(self, button, name)

    def handle_mousemotion(self, change):
        """Callback for mouse motion events from event_handler."""
        if Widget.handle_mousemotion(self, change):
            App.handle_mousemotion(self, change)

    def handle_uncaught_event(self, event):
        """Callback for uncaught_event events from event_handler."""
        if Widget.handle_uncaught_event(self, event):
            App.handle_uncaught_event(self, event)

    def handle_keydown(self, key, string):
        """Callback for key press events from event_handler."""
        if Widget.handle_keydown(self, key, string):
            App.handle_keydown(self, key, string)

    def handle_keyup(self, key, string):
        """Callback for key release events from event_handler."""
        if Widget.handle_keyup(self, key, string):
            App.handle_keyup(self, key, string)

    def handle_keyhold(self, key, string):
        """Callback for key hold events from event_handler."""
        if Widget.handle_keyhold(self, key, string):
            App.handle_keyhold(self, key, string)

    def render(self):
        screen = self.parent.get_screen()
        self.clear_screen()

        App.render(self)

        screen.blit(self.screen, self.pos)
