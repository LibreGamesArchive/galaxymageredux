import pygame
from pygame.locals import *

import event
import time

printable_chars = "abcdefghijklmnopqrstuvwxyz`1234567890-=[]\\;',./ "+'ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?'

class App(object):
    def __init__(self, screen, event_handler, bg_image=None):

        self.screen = screen
        self.event_handler = event_handler
        self.event_handler.gui = self
        self.event_handler.all_guis.append(self)
        self.widgets = []

        self.bg_image = bg_image

        #self.dispatch = event.Dispatcher()

        self.font = pygame.font.Font(None, 32)
        self.visible = True

    def activate(self):
        self.event_handler.gui = self

    def get_root_app(self):
        return self

    def focus(self):
        pass

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
        if self.bg_image:
            self.screen.blit(self.bg_image, (0,0))
        self.widgets.reverse()
        for i in self.widgets:
            if i.visible: i.render()
        self.widgets.reverse()

class Widget(object):
    def __init__(self, parent, pos):
        self.parent = parent
        self.parent.add_widget(self)

        if type(pos) is type([]) or type(pos) is type((1,2)):
            self.pos = AbsolutePos(pos)
        else:
            self.pos = pos
        self.pos.parent = self.parent
        self.size = 0,0
        self.dispatch = event.Dispatcher()

        self.visible = True
        self.font = self.parent.get_font()

        self._mhold = False
        self._mhover = False
        self.key_active = False
        self.key_hold_lengths = {}
        self.khl = 150 #milliseconds to hold keys for repeat!

        self.no_events = False

        self.last_click = None
        self.double_click_dur = 0.1 #max seconds between clicks to register!
        self.dispatch.bind('click', self.test_double_click)

    def test_double_click(self):
        if self.last_click:
            if time.time() - self.last_click < self.double_click_dur:
                self.dispatch.fire('double-click')
                self.last_click = None
                return
        self.last_click = time.time()

    def destroy(self):
        if self in self.parent.widgets:
            self.parent.widgets.remove(self)

    def get_root_app(self):
        return self.parent.get_root_app()

    def get_real_pos(self):
        parents = []
        i = self.parent
        while not i == self.get_root_app():
            parents.append(i)
            i = i.parent

        x = 0
        y = 0
        for i in parents:
            ix, iy = i.pos.get_pos()
            x += ix
            y += iy
        sx, sy = self.pos.get_pos()
        return x+sx, y+sy

    def mouse_on_me(self):
        return pygame.Rect(self.pos.get_pos(), self.size).collidepoint(self.parent.get_mouse_pos())

    def focus(self):
        """Focus this widget so it is at the top of rendering and event calls."""
        self.parent.set_top_widget(self)
        self.key_active = True
        self.dispatch.fire("focus")
        self._mhover = self.mouse_on_me()
        self.parent.focus()

    def unfocus(self):
        """Remove the widget's focus."""
        self.key_active=False
        self.key_hold_lengths = {}
        self.dispatch.fire("unfocus")
        self._mhold=False
        self._mhover=False

    def handle_mousedown(self, button, name):
        """Handle a mouse down event from the App."""
        if self.no_events:
            return False
        self._mhover = self.mouse_on_me()
        if name == "left":
            if self._mhover:
                self._mhold = True
                self.focus()
                self.dispatch.fire("press")
                return True
            self.unfocus()
        return self._mhover

    def handle_mouseup(self, button, name):
        """Handle a mouse release event from the App."""
        if self.no_events:
            return False
        self._mhover = self.mouse_on_me()
        if name == "left":
            if self._mhold and self._mhover:
                self._mhold = False
                self.dispatch.fire("click")
                return True
        return self._mhover

    def handle_mousehold(self, button, name):
        """Handle a mouse hold event from the App."""
        if self.no_events:
            return False
        if name == "left":
            if self._mhold:
                return True
        return self._mhover

    def handle_mousemotion(self, change):
        """Handle a mouse motion event from the App."""
        if self.no_events:
            return False
        n = self._mhover
        self._mhover = self.mouse_on_me()
        if n == False and self._mhover == True:
            self.dispatch.fire("hover")
            for i in self.parent.widgets:
                if not i == self:
                    n = i._mhover
                    i._mhover = False
                    if n == True:
                        i.dispatch.fire("unhover")
            if self._mhold:
                self.dispatch.fire("press-return")
        if n == True and self._mhover == False:
            self.dispatch.fire("unhover")
        return self._mhover

    def can_handle_key(self, key, string):
        """Return whether key/string is used by this widget."""
        if self.no_events:
            return False
        return False

    def handle_keydown(self, key, string):
        """Handle a key down event from the App."""
        if self.no_events:
            return False
        if self.can_handle_key(key, string):
            if self.key_active:
                self.dispatch.fire("keypress", key, string)
                return True

    def handle_keyhold(self, key, string):
        """Handle a key hold event from the App."""
        if self.no_events:
            return False
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
        if self.no_events:
            return False
        if self.can_handle_key(key, string):
            if self.key_active:
                if key in self.key_hold_lengths:
                    del self.key_hold_lengths[key]
                return True

    def handle_uncaught_event(self, event):
        """Handle any non mouse or key event from the App."""
        if self.no_events:
            return False
        pass

    def render(self):
        pass

    def draw_rect(self, screen, rect, color):
        surf = pygame.Surface(rect.size).convert_alpha()
        surf.fill(color)
        screen.blit(surf, rect)


class Container(Widget, App):
    def __init__(self, parent, size, pos):
        Widget.__init__(self, parent, pos)
        self.size = size
        self.widgets = []

        self.dispatch = event.Dispatcher()
        self.bg_image = None

        self.font = self.parent.get_font()

        self.screen = pygame.Surface(size).convert_alpha()
        self.bg_color = (0,0,0,0)

        self.clear_screen()
        self.dispatch.bind("unhover", self.unhover_all_widgets)

    def change_size(self, new):
        self.size = new
        self.screen = pygame.Surface(new).convert_alpha()

    def unhover_all_widgets(self):
        for i in self.widgets:
            n = i._mhover
            i._mhover = False
            if n == True:
                i.dispatch.fire("unhover")

    def clear_screen(self):
        self.screen.fill(self.bg_color)

    def get_mouse_pos(self):
        x,y = self.parent.get_mouse_pos()
        xx, yy = self.pos.get_pos()
        x = x - xx
        y = y - yy
        return x,y

    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        x = Widget.handle_mousedown(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mousedown(button, name):
                    return True
        return x

    def handle_mouseup(self, button, name):
        """Callback for mouse release events from the event_handler."""
        x = Widget.handle_mouseup(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.visible:
            return False
        for i in self.widgets:
            if i.visible:
                if i.handle_mouseup(button, name):
                    return True
        return x

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

        screen.blit(self.screen, self.pos.get_pos())

class Icon(Widget):
    def __init__(self, parent, pos, image):
        Widget.__init__(self, parent, pos)

        self.image = image

        self.size = self.image.get_size()

    def get_size(self):
        return self.image.get_size()

    def render(self):
        self.size = self.get_size()
        try:
            self.image.render(self.parent.screen, self.pos.get_pos())
        except:
            self.parent.screen.blit(self.image, self.pos.get_pos())

class Label(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent, pos)

        self.text = text

        self.bg_color = (255,255,255,255)

        self.size = self.get_size()

        self.text_color = (100,100,100)
        self.bg_color = None

    def get_size(self):
        width, height = self.font.size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        i = self.font.render(self.text, 1, self.text_color)
        r = i.get_rect()
        r.topleft = self.pos.get_pos()
        if self.bg_color:
            self.draw_rect(self.parent.screen, r, self.bg_color)
        self.parent.screen.blit(i, r)

class Button(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent, pos)

        self.text = text

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
        width, height = self.font.size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        i = self.font.render(self.text, 1, self.text_color)
        r = i.get_rect()
        r.topleft = self.pos.get_pos()
        if self.bg_color:
            self.draw_rect(self.parent.screen, r, self.bg_color)
        self.parent.screen.blit(i, r)

class MessageBoxLabel(Widget):
    def __init__(self, parent, text):
        Widget.__init__(self, parent, (0,0))

        self.text = text

        self.size = self.get_size()

    def get_size(self):
        return self.font.size(self.text)

    def render(self):
        self.size = self.get_size()
        if self.parent.entry_bg_color:
            self.draw_rect(self.parent.screen,
                           pygame.Rect(self.pos.get_pos(), self.size),
                           self.parent.entry_bg_color)
        self.parent.screen.blit(self.font.render(self.text, 1, self.parent.text_color), self.pos.get_pos())

class MessageBox(Container):
    def __init__(self, parent, size, pos, max_lines=10):
        Container.__init__(self, parent, size, pos)

        self.max_lines = max_lines
        self.text_color = (0,0,0)
        self.entry_bg_color = None

    def add_line(self, text):
        MessageBoxLabel(self, text)

        height = self.font.get_height()

        lasty = self.size[1] - height
        for i in self.widgets:
            i.pos.y = lasty
            lasty -= height

        self.widgets = self.widgets[0:self.max_lines]

class Input(Widget):
    def __init__(self, parent, width, pos, max_chars=50):
        Widget.__init__(self, parent, pos)

        self.text = ""
        self.cursor_pos = 0

        self.width = width
        self.max_chars = max_chars
        self.size = self.get_size()

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
        elif string and string in printable_chars:
            self.text = self.text[0:self.cursor_pos] + string + self.text[self.cursor_pos::]
            self.cursor_pos += 1

            if self.max_chars >= 0 and len(self.text) >= self.max_chars:
                self.text = self.text[0:self.max_chars]
                self.cursor_pos = self.max_chars
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

        self.draw_rect(self.parent.screen, pygame.Rect(self.pos.get_pos(), self.size), self.bg_color)

        self.parent.screen.subsurface(self.pos.get_pos(), self.size).blit(
            self.font.render(self.text, 1, self.text_color), (-shift, 0))

        if time.time() - self.flash_timer > self.flash_space:
            self.flash_timer = time.time()
            self.flashed = not self.flashed

        if self.key_active and self.flashed:
            surf = pygame.Surface((2,self.size[1]-2)).convert_alpha()
            surf.fill(self.text_color)
            self.parent.screen.subsurface(self.pos.get_pos(), self.size).blit(
                surf, (x-shift, 1))

class RelativePos(object):
    """makes a position relative to the parent"""
    def __init__(self, x="left", y="bottom", to=None, padx=0, pady=0):
        self.x = x
        self.y = y
        self.padx = padx
        self.pady = pady
        self.to = to

    def get_pos(self):
        rel = self.to
        relx, rely = rel.pos.get_pos()
        if self.x == "left":
            x = relx
        elif self.x == "center":
            x = relx + int(rel.size[0]*0.5)
        else:
            x = relx + rel.size[0]

        if self.y == "top":
            y = rely
        elif self.y == "center":
            y = rely + int(rel.size[1]*0.5)
        else:
            y = rely + rel.size[1]

        return x+self.padx, y+self.pady

    def get_real_pos(self):
        rel = self.to
        px, py = rel.get_real_pos()
        if self.x == "left":
            x = px
        elif self.x == "center":
            x = px + int(rel.size[0]*0.5)
        else:
            x = px + rel.size[0]

        if self.y == "top":
            y = py
        elif self.x == "center":
            y = py + int(rel.size[1]*0.5)
        else:
            y = py + rel.size[1]

        return x+self.padx, y+self.pady

class AbsolutePos(object):
    def __init__(self, pos):
        self.x, self.y = pos

    def get_pos(self):
        return self.x, self.y

class PopUp(Widget):
    """Shows up on hover over parent"""
    def __init__(self, parent, pos=RelativePos("left", "bottom"), text="", width=150):
        Widget.__init__(self, parent.get_root_app(), pos)
        self.no_events = True

        self.attached_to = parent
        self.pos.to = self.attached_to
        self.text = text
        self.text_color = (0,0,0)

        self.width = width
        self.size = self.get_size()

        self.bg_color = None
        self.visible = False

        self.attached_to.dispatch.bind("hover", self.turn_on)
        self.attached_to.dispatch.bind("unhover", self.turn_off)

    def turn_on(self):
        self.visible = True
        self.parent.add_widget(self)
    def turn_off(self):
        self.visible = False
        self.destroy()

    def unfocus(self):
        Widget.unfocus(self)
        if self.visible:
            a,b,c,d = (self.attached_to.key_active, self.attached_to.key_hold_lengths,
                       self.attached_to._mhold, self.attached_to._mhover)
            self.parent.set_top_widget(self)
            self.attached_to.key_active, self.attached_to.key_hold_lengths = a,b
            self.attached_to._mhold, self.attached_to._mhover = c,d

    def compile_text(self):
        lines = []
        words = self.text.split(" ")

        cur_line = words[0]
        words.pop(0)
        while words:
            if self.font.size(cur_line+" "+words[0])[0] > self.width:
                if cur_line: lines.append(cur_line)
                cur_line = words[0]
            else:
                cur_line += " " + words[0]

            words.pop(0)

        self.comp_text = lines

    def get_size(self):
        self.compile_text()
        x = self.width
        y = self.font.get_height() * len(self.comp_text)

        return x, y

    def render(self):
        self.size = self.get_size()
        pos = self.pos.get_real_pos()
        self.draw_rect(self.parent.screen, pygame.Rect(pos, self.size), self.bg_color)

        down = 0
        for line in self.comp_text:
            self.parent.screen.blit(self.font.render(line, 1, self.text_color), (pos[0], pos[1]+down))
            down += self.font.get_height()


class DropDown(Button):
    def __init__(self, parent, pos, text, child=None):
        Button.__init__(self, parent, pos, text)

        self.child = None
        if child:
            self.setChild(child)
        self.dispatch.bind('click', self.turn_on)

    def setChild(self, child):
        self.child = child
        child.pos = RelativePos(to=self)
        child.dispatch.bind('unfocus', self.turn_off)
        self.turn_off()

    def turn_off(self):
        self.child.visible = False
        self.child.destroy()
    def turn_on(self):
        self.child.visible = True
        self.parent.add_widget(self.child)


class ListEntry(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent, pos)

        self.text = text

        self.size = self.get_size()

    def get_size(self):
        width, height = self.parent.font.size(self.text)
        return width, height

    def render(self):
        i = self.parent.font.render(self.text, 1, self.parent.entry_text_color)
        r = pygame.rect.Rect(self.pos.get_pos(), self.size)
        if self.parent.entry_bg_color:
            self.draw_rect(self.parent.screen, r, self.parent.entry_bg_color)
        self.parent.screen.blit(i, r)

class List(Container):
    def __init__(self, parent, pos, entries=[], padding=(0,0)):
        Container.__init__(self, parent, (1,1), pos)

        self.entry_text_color = (0,0,0)
        self.entry_bg_color = (255,255,255)

        self.entries = entries
        self.padding = padding

        self.build_entries()

    def build_entries(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.entries:
            if self.widgets:
                pos = RelativePos(to=self.widgets[0], pady=self.padding[1])
            else:
                pos = AbsolutePos(self.padding)
            new = ListEntry(self, pos, opt)

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))


class MenuEntry(Widget):
    def __init__(self, parent, pos, text):
        Widget.__init__(self, parent, pos)

        self.text = text

        self.size = self.get_size()

        self.text_color = self.parent.entry_text_reg_color

        self.dispatch.bind('hover', lambda: self.swap_text_color(self.parent.entry_text_hover_color))
        self.dispatch.bind('click', lambda: self.swap_text_color(self.parent.entry_text_hover_color))
        self.dispatch.bind('press', lambda: self.swap_text_color(self.parent.entry_text_click_color))
        self.dispatch.bind('press-return', lambda: self.swap_text_color(self.parent.entry_text_click_color))
        self.dispatch.bind('unhover', lambda: self.swap_text_color(self.parent.entry_text_reg_color))
        self.dispatch.bind('unhover', self.keep_off_held_if_unhover)

    def swap_text_color(self, new):
        self.text_color = new
    def keep_off_held_if_unhover(self):
        self._mhold = False

    def get_size(self):
        width, height = self.parent.font.size(self.text)
        return width, height

    def render(self):
        i = self.parent.font.render(self.text, 1, self.text_color)
        r = pygame.rect.Rect(self.pos.get_pos(), self.size)
        if self.parent.entry_bg_color:
            self.draw_rect(self.parent.screen, r, self.parent.entry_bg_color)
        self.parent.screen.blit(i, r)

class Menu(Container):
    def __init__(self, parent, pos, options=[], padding=(0,0)):
        Container.__init__(self, parent, (1,1), pos)

        self.entry_text_reg_color = (0,0,0)
        self.entry_text_hover_color = (75,75,75)
        self.entry_text_click_color = (150,150,150)
        self.entry_bg_color = (255,255,255)

        self.options = options
        self.padding = padding

        self.build_options()

    def build_options(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.options:
            if self.widgets:
                pos = RelativePos(to=self.widgets[0], pady=self.padding[1])
            else:
                pos = AbsolutePos(self.padding)
            new = MenuEntry(self, pos, opt)
            new.dispatch.bind('click', lambda:self.dispatch.fire('select', self.widgets[0].text))

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))

class MenuDisableEntry(Widget):
    def __init__(self, parent, pos, text, dis):
        Widget.__init__(self, parent, pos)

        self.text = text

        self.size = self.get_size()

        self.disabled = dis
        if self.disabled:
            self.text_color = self.parent.entry_dis_text_reg_color
            self.dispatch.bind('hover', lambda: self.swap_text_color(self.parent.entry_dis_text_hover_color))
            self.dispatch.bind('click', lambda: self.swap_text_color(self.parent.entry_dis_text_hover_color))
            self.dispatch.bind('press', lambda: self.swap_text_color(self.parent.entry_dis_text_click_color))
            self.dispatch.bind('press-return', lambda: self.swap_text_color(self.parent.entry_dis_text_click_color))
            self.dispatch.bind('unhover', lambda: self.swap_text_color(self.parent.entry_dis_text_reg_color))
        else:
            self.text_color = self.parent.entry_text_reg_color
            self.dispatch.bind('hover', lambda: self.swap_text_color(self.parent.entry_text_hover_color))
            self.dispatch.bind('click', lambda: self.swap_text_color(self.parent.entry_text_hover_color))
            self.dispatch.bind('press', lambda: self.swap_text_color(self.parent.entry_text_click_color))
            self.dispatch.bind('press-return', lambda: self.swap_text_color(self.parent.entry_text_click_color))
            self.dispatch.bind('unhover', lambda: self.swap_text_color(self.parent.entry_text_reg_color))
        self.dispatch.bind('unhover', self.keep_off_held_if_unhover)

    def swap_text_color(self, new):
        self.text_color = new
    def keep_off_held_if_unhover(self):
        self._mhold = False

    def get_size(self):
        width, height = self.parent.font.size(self.text)
        return width, height

    def render(self):
        i = self.parent.font.render(self.text, 1, self.text_color)
        r = pygame.rect.Rect(self.pos.get_pos(), self.size)
        if self.disabled:
            bg = self.parent.entry_dis_bg_color
        else:
            bg = self.parent.entry_bg_color
        if bg:
            self.draw_rect(self.parent.screen, r, bg)
        self.parent.screen.blit(i, r)

class DisableMenu(Container):
    def __init__(self, parent, pos, options=[], padding=(0,0)):
        Container.__init__(self, parent, (1,1), pos)

        self.entry_text_reg_color = (0,0,0)
        self.entry_text_hover_color = (75,75,75)
        self.entry_text_click_color = (150,150,150)
        self.entry_bg_color = (255,255,255)
        self.entry_dis_bg_color = (0,0,0)
        self.entry_dis_text_reg_color = (100,100,100)
        self.entry_dis_text_hover_color = (100,100,100)
        self.entry_dis_text_click_color = (100,100,100)

        self.options = options
        self.padding = padding

        self.build_options()

    def build_options(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.options:
            opt, dis = opt
            if self.widgets:
                pos = RelativePos(to=self.widgets[0], pady=self.padding[1])
            else:
                pos = AbsolutePos(self.padding)
            new = MenuDisableEntry(self, pos, opt, dis)
            new.dispatch.bind('click', lambda:self.dispatch.fire('select', self.widgets[0].text, self.widgets[0].disabled))

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width+self.padding[0]*2, height+self.padding[1]))

class DropDownMenu(DropDown):
    def __init__(self, parent, pos, text, options=[], padding=(0,0)):
        child = Menu(parent, RelativePos(to=self), options, padding)

        DropDown.__init__(self, parent, pos, text, child)

        self.child.dispatch.bind('select', self.fire_event)

    def fire_event(self, item):
        self.dispatch.fire('select', item)
        self.turn_off()


class GameRoomLobbyPlayers(Container):
    def __init__(self, parent, size, pos):
        Container.__init__(self, parent, size, pos)

    def set_players(self, game, players, free_teams):
        self.widgets = []
        last = None
        for player in players:
            name, team = player

            if last:
                pos = RelativePos(to=last, pady=5)
            else:
                pos = (5,5)
            #new = Container(self, (self.size[0]-10, 24), pos)
            x = Label(self, pos, name)
            x.bg_color = (0,0,0)
            x.text_color = (100,100,100)
            last = x
            x = Label(self, RelativePos(to=x, padx=20, x='right',y='top'), 'Team:')
            x.bg_color = (0,0,0)
            x.text_color = (100,100,100)
            if game.player_name == name:
                self.pt = x = DropDownMenu(self, RelativePos(to=x, padx=5, x='right',y='top'),
                                     team, [team]+free_teams)
                self.pt.dispatch.bind('select', self.swap_team_widg)
            else:
                x = Label(self, RelativePos(to=x, padx=5, x='right',y='top'), team)
                x.bg_color = (0,0,0)
                x.text_color = (100,100,100)
            
            if game.am_master and not game.player_name==name:
                x = Button(self, RelativePos(to=x, padx=20, x='right',y='top'), 'Kick')
                x.dispatch.bind('click', lambda name=name: self.dispatch.fire('kick', name))

    def swap_team_widg(self, value):
##        self.pt.text = value
        self.dispatch.fire('change-team', value)
