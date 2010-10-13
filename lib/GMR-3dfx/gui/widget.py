from include import *

import misc

class Widget(object):
    def __init__(self, parent, pos):
        self.parent = parent
        self.parent.add_widget(self)

        self.screen = self.parent.screen

        if type(pos) is type([]) or type(pos) is type((1,2)):
            self.pos = misc.AbsolutePos(pos)
        else:
            self.pos = pos

        if isinstance(pos, misc.RelativePos):
            if pos.to == None:
                if len(self.parent.widgets) > 1:
                    pos.to = self.parent.widgets[1]

        self.size = 0,0
        self.dispatch = event.Dispatcher()

        self.visible = True
        self.font = self.parent.font

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

    def get_rect(self):
        return pygame.Rect(self.pos.get_pos(), self.size)

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

    def draw_rect(self, rect, color):
        engine.draw.rect2d(rect, color)

    def draw_text(self, text, pos, color):
        down = self.font.get_height()
        x,y = pos
        for t in text.split('\n'):
            self.font.render(t, (x,y), color)
            y += down

    def get_text_size(self, text):
        width = 0
        height = 0
        down = self.font.get_height()
        for t in text.split('\n'):
            w,h = self.font.get_size(t)
            width = max((width, w))
            height += down

        return width, height
