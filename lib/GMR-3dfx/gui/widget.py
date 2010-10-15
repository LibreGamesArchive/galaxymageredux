from include import *

import misc, theme

class Widget(object):
    widget_type = "Widget"
    def __init__(self, parent, pos, name=None):
        self.widget_name = name

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

        self.theme = self.parent.theme.get_element(self.widget_type,
                                                   self.widget_name)
##        theme.print_children(self.theme)

        self.size = 0,0
        self.dispatch = event.Dispatcher()

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

    def draw_rect(self, rect, color, texture=None):
        engine.draw.rect2d(rect, color, texture)

    def draw_canvas_border(self, rect, canvas, border):
        rect = pygame.Rect(rect)
        canvas = self.get_canvas(canvas)
        border = self.get_border(border)
        if border:
            left, right, top, bottom = border
            #each - texture, color, size

            #render borders
            i = left[0]
            if i != None:
                i = i.get_region(0,top[2],left[2],i.size[1]-top[2]-bottom[2])
            self.draw_rect((rect.left, rect.top+top[2], left[2], rect.height-top[2]-bottom[2]),
                           left[1], i)

            i = right[0]
            if i != None:
                i = i.get_region(i.size[0]-right[2],top[2],right[2],i.size[1]-top[2]-bottom[2])
            self.draw_rect((rect.right-right[2], rect.top+top[2], right[2], rect.height-top[2]-bottom[2]),
                           right[1], i)

            i = top[0]
            if i != None:
                i = i.get_region(0,0,i.size[0],top[2])
            self.draw_rect((rect.left, rect.top, rect.width, top[2]),
                           top[1], i)

            i = bottom[0]
            if i != None:
                i = i.get_region(0,i.size[1]-bottom[2],i.size[0],bottom[2])
            self.draw_rect((rect.left, rect.bottom-bottom[2], rect.width, bottom[2]),
                           bottom[1], i)

            l,t,w,h = rect
            l += left[2]
            t += top[2]
            w -= left[2] + right[2]
            h -= top[2] + bottom[2]
            self.draw_rect(pygame.Rect(l,t,w,h), canvas[1], canvas[0])
        else:
            self.draw_rect(rect, canvas[1], canvas[0])

    def draw_text(self, text, pos):
        font = self.get_font()
        down = font.get_height()
        pad = self.get_padding()
        color = self.theme.get_val('text-color', (0,0,0,1))
        x,y = pos
        for t in text.split('\n'):
            font.render(t, (x+pad[0],y+pad[1]), color)
            y += down

    def get_text_size(self, text):
        font = self.get_font()
        pad = self.get_padding()
        width = 0
        height = 0
        down = font.get_height()
        for t in text.split('\n'):
            w,h = font.get_size(t)
            width = max((width, w))
            height += down

        return width+pad[0]+pad[2], height+pad[1]+pad[3]

    def get_canvas(self, name):
        bg = self.theme.get_val(name, [])
        image = None
        color = Color((1,1,1,1))
        i = 0
        while i < len(bg):
            ii = bg[i]
            if ii == "image":
                image = self.theme.get_texture(bg[i+1])
                i += 1
            elif ii == "block":
                new, left, top, width, height = bg[i+1]
                timage = self.theme.get_texture(new)
                image = timage.get_region((left, top,
                                           width+left,
                                           height+top))
                i += 1
            elif ii == "solid":
                image = None
            elif ii == "color":
                color = Color(bg[i+1])
                i += 1
            i += 1

        return image, color

    def get_border(self, name):
        bg = self.theme.get_val(name, None)
        if bg == None:
            return None
        Li = Ri = Ti = Bi = None
        Lc = Rc = Tc = Bc = Color((1,1,1,1))
        Ls = Rs = Ts = Bs = 1
        i = 0
        while i < len(bg):
            ii = bg[i]
            if ii == "block":
                new, size = bg[i+1]
                image = self.theme.get_texture(new)
                Li = Ri = Ti = Bi = image
                Ls = Rs = Ts = Bs = size
                i += 1
            elif ii == "solid":
                Li = Ri = Ti = Bi = None
                Ls = Rs = Ts = Bs = bg[i+1]
                i += 1
            elif ii == "color":
                Lc = Rc = Tc = Bc = Color(bg[i+1])
                i += 1

            #left
            if ii == "block-left":
                new, size = bg[i+1]
                image = self.theme.get_texture(new)
                Li = image
                Ls = size
                i += 1
            elif ii == "solid-left":
                Li = None
                Ls = bg[i+1]
                i += 1
            elif ii == "color-left":
                Lc = Color(bg[i+1])
                i += 1

            #right
            if ii == "block-right":
                new, size = bg[i+1]
                image = self.theme.get_texture(new)
                Ri = image
                Rs = size
                i += 1
            elif ii == "solid-right":
                Ri = None
                Rs = bg[i+1]
                i += 1
            elif ii == "color-right":
                Rc = Color(bg[i+1])
                i += 1

            #top
            if ii == "block-top":
                new, size = bg[i+1]
                image = self.theme.get_texture(new)
                Ti = image
                Ts = size
                i += 1
            elif ii == "solid-top":
                Ti = None
                Ts = bg[i+1]
                i += 1
            elif ii == "color-top":
                Tc = Color(bg[i+1])
                i += 1

            #bottom
            if ii == "block-bottom":
                new, size = bg[i+1]
                image = self.theme.get_texture(new)
                Bi = image
                Bs = size
                i += 1
            elif ii == "solid-bottom":
                Bi = None
                Bs = bg[i+1]
                i += 1
            elif ii == "color-bottom":
                Bc = Color(bg[i+1])
                i += 1
            i += 1

        return ((Li, Lc, Ls), (Ri, Rc, Rs),
                (Ti, Tc, Ts), (Bi, Bc, Bs))

    def get_visible(self):
        return self.theme.get_val('visible', True)

    def get_font(self, name='font'):
        name, size = self.theme.get_val(name, [None, 32])
        return self.theme.get_font(name).make_size(size)

    def get_padding(self, name='padding'):
        return self.theme.get_val(name, (0,0,0,0))
