import pygame
from pygame.locals import *

import event

class App(object):
    def __init__(self, screen, event_handler):

        if screen:
            self.screen = screen
        if event_handler:
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


class Container(App):
    def __init__(self, parent, size, pos, background_image=None):
        self.parent = parent
        self.parent.add_widget(self)
        self.size = size
        self.pos = pos
        App.__init__(self, None, None)

        self.dispatch = event.Dispatcher()

        self.screen = pygame.Surface(size).convert_alpha()
        self.bg_color = (0,0,0,0)
        self.background_image = background_image

        self.clear_screen()

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

    def mouse_on_me(self):
        return pygame.Rect(self.pos, self.size).collidepoint(self.parent.get_mouse_pos)

    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        if not mouse_on_me():
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
        if not mouse_on_me():
            return False
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mouseup(button, name):
                    return True
        return False

    def render(self):
        screen = self.parent.get_screen()
        self.clear_screen()

        App.render(self)

        screen.blit(self.screen, self.pos)
