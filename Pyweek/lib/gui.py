import pygame
from pygame.locals import *

import event
import time

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
            if self._mhold:
                self.dispatch.fire("press-return")
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

    def draw_rect(self, screen, rect, color):
        surf = pygame.Surface(rect.size).convert_alpha()
        surf.fill(color)
        screen.blit(surf, rect)


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
            return True
        return False

    def handle_mousemotion(self, change):
        """Callback for mouse motion events from event_handler."""
        if Widget.handle_mousemotion(self, change):
            App.handle_mousemotion(self, change)
            return True
        return False

    def handle_uncaught_event(self, event):
        """Callback for uncaught_event events from event_handler."""
        if Widget.handle_uncaught_event(self, event):
            App.handle_uncaught_event(self, event)
            return True
        return False

    def can_handle_key(self, key, string):
        for i in self.widgets:
            if i.can_handle_key(key, string):
                return True
        return False

    def handle_keydown(self, key, string):
        """Callback for key press events from event_handler."""
        return App.handle_keydown(self, key, string)

    def handle_keyup(self, key, string):
        """Callback for key release events from event_handler."""
        return App.handle_keyup(self, key, string)

    def handle_keyhold(self, key, string):
        """Callback for key hold events from event_handler."""
        return App.handle_keyhold(self, key, string)

    def render(self):
        screen = self.parent.get_screen()
        self.clear_screen()

        App.render(self)

        screen.blit(self.screen, self.pos)

class Icon(Widget):
    def __init__(self, parent, pos, image):
        Widget.__init__(self, parent)

        self.pos = pos
        self.image = image

        self.size = self.image.get_size()

    def render(self):
        self.parent.screen.blit(self.image, self.pos)

class Label(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent)

        self.pos = pos
        self.text = text

        self.bg_image = None
        self.bg_color = (255,255,255,255)

        self.size = self.get_size()

        self.text_color = None

    def get_size(self):
        if self.bg_image:
            width, height = self.bg_image.get_size()
        else:
            width, height = self.font.size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        if self.bg_image:
            self.parent.screen.blit(self.bg_image, self.pos)
            i = self.font.render(self.text, 1, self.text_color)
            r = i.get_rect()
            w,h = self.size
            r.centerx = self.pos[0]+w/2
            r.centery = self.pos[1]+h/2
            self.parent.screen.blit(i, r)
        else:
            i = self.font.render(self.text, 1, self.text_color)
            r = i.get_rect()
            r.topleft = self.pos
            if self.bg_color:
                self.draw_rect(self.parent.screen, r, self.bg_color)
            self.parent.screen.blit(i, r)

class Button(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent)

        self.pos = pos
        self.text = text

        self.bg_image = None
        self.bg_color = (255,255,255,255)

        self.size = self.get_size()

        self.text_color = (0,0,0)
        self.text_reg_color = (0,0,0)
        self.text_hover_color = (255,0,0)
        self.text_click_color = (255,100,100)

        self.dispatch.bind('hover', lambda: self.swap_text_color(self.text_hover_color))
        self.dispatch.bind('click', lambda: self.swap_text_color(self.text_hover_color))
        self.dispatch.bind('press', lambda: self.swap_text_color(self.text_click_color))
        self.dispatch.bind('press-return', lambda: self.swap_text_color(self.text_click_color))
        self.dispatch.bind('unhover', lambda: self.swap_text_color(self.text_reg_color))

    def swap_text_color(self, new):
        self.text_color = new

    def get_size(self):
        if self.bg_image:
            width, height = self.bg_image.get_size()
        else:
            width, height = self.font.size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        if self.bg_image:
            self.parent.screen.blit(self.bg_image, self.pos)
            i = self.font.render(self.text, 1, self.text_color)
            r = i.get_rect()
            w,h = self.size
            r.centerx = self.pos[0]+w/2
            r.centery = self.pos[1]+h/2
            self.parent.screen.blit(i, r)
        else:
            i = self.font.render(self.text, 1, self.text_color)
            r = i.get_rect()
            r.topleft = self.pos
            if self.bg_color:
                self.draw_rect(self.parent.screen, r, self.bg_color)
            self.parent.screen.blit(i, r)

class MessageBoxLabel(Widget):
    def __init__(self, parent, text):
        Widget.__init__(self, parent)

        self.pos = (0,0)
        self.text = text

        self.size = self.get_size()

    def get_size(self):
        return self.font.size(self.text)

    def render(self):
        self.size = self.get_size()
        self.parent.screen.blit(self.font.render(self.text, 1, self.parent.text_color), self.pos)

class MessageBox(Container):
    def __init__(self, parent, size, pos, background_image=None, max_lines=10):
        Container.__init__(self, parent, size, pos, background_image)

        self.max_lines = max_lines
        self.text_color = (0,0,0)

    def add_line(self, text):
        MessageBoxLabel(self, text)

        height = self.font.get_height()

        lasty = self.size[1] - height
        for i in self.widgets:
            i.pos = (0,lasty)
            lasty -= height

        self.widgets = self.widgets[0:self.max_lines]

class Input(Widget):
    def __init__(self, parent, width, pos, background_image=None, max_chars=50):
        Widget.__init__(self, parent)

        self.pos = pos
        self.text = ""
        self.cursor_pos = 0

        self.width = width
        self.max_chars = max_chars
        self.size = self.get_size()

        self.bg_image = background_image
        self.bg_color = (100,100,100)
        self.text_color = (255,0,0)

        self.dispatch.bind('keypress', self.handle_key)
        self.always_active = True
        self.key_active = True

        self.flash_timer = time.time()
        self.flash_space = 0.5
        self.flashed = False

    def can_handle_key(self, key, string):
        return True

    def unfocus(self):
        Widget.unfocus(self)
        if self.always_active:
            self.key_active = True

    def handle_key(self, key, string):
        if key == K_LEFT:
            if self.cursor_pos > 0: self.cursor_pos -= 1
        elif key == K_RIGHT:
            if self.cursor_pos < len(self.text): self.cursor_pos += 1
        elif key == K_HOME:
            self.cursor_pos = 0
        elif key == K_END:
            self.cursor_pos = len(self.text)
        elif key == K_DELETE:
            self.text = self.text[0:self.cursor_pos]+self.text[self.cursor_pos+1::]
        elif key == K_BACKSPACE:
            if self.cursor_pos:
                self.text = self.text[0:self.cursor_pos-1]+self.text[self.cursor_pos::]
                self.cursor_pos -= 1
        elif key == K_RETURN:
            self.dispatch.fire("input-submit", self.text)
        else:
            self.text = self.text[0:self.cursor_pos] + string + self.text[self.cursor_pos::]
            self.cursor_pos += 1

            if len(self.text) >= self.max_chars:
                self.text = self.text[0:self.max_chars]
        self.flash_timer = time.time()
        self.flashed = True
        return True

    def get_size(self):
        return self.width, self.font.get_height()

    def get_cursor_real_x(self):
        x = self.font.size(self.text[0:self.cursor_pos])[0]
        shift = 0
        if x > self.width:
            shift = x - self.width + 3

        return x, shift

    def render(self):
        self.size = self.get_size()

        x, shift = self.get_cursor_real_x()

        self.parent.screen.subsurface(self.pos, self.size).blit(
            self.font.render(self.text, 1, self.text_color), (-shift, 0))

        if time.time() - self.flash_timer > self.flash_space:
            self.flash_timer = time.time()
            self.flashed = not self.flashed

        if self.key_active and self.flashed:
            surf = pygame.Surface((3,self.size[1])).convert_alpha()
            surf.fill((255,255,255))
            self.parent.screen.subsurface(self.pos, self.size).blit(
                surf, (x-shift, 0))
