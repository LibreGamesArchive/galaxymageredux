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

        self.update_theme()

        self.dispatch = event.Dispatcher()

        self._mhold = False
        self._mhover = False
        self.key_active = False
        self.key_hold_lengths = {}

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

    def update_theme(self):
        self.theme = self.parent.theme.get_element_copy(self.widget_type,
                                                        self.widget_name)

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
            ix, iy = i.get_pos_with_padding()
            x += ix
            y += iy
        sx, sy = self.get_pos()
        return x+sx, y+sy

    def get_pos(self):
        return self.pos.get_pos()

    def get_pos_with_padding(self):
        x,y = self.get_pos()
        pad = self.get_padding()
        return (x+pad[0],y+pad[1])

    def get_size(self):
        return (0,0)

    def get_size_with_padding(self):
        w,h = self.get_size()
        pad = self.get_padding()
        return (w+pad[0]+pad[1], h+pad[2]+pad[3])

    def get_rect(self):
        return pygame.Rect(self.get_pos_with_padding(), self.get_size())

    def get_rect_with_padding(self):
        return pygame.Rect(self.get_pos(), self.get_size_with_padding())

    def mouse_on_me(self):
        if self.get_theme_val('mouse-ignore-border', False):
            return bool(self.get_rect().collidepoint(self.parent.get_mouse_pos()))
        else:
            return bool(self.get_rect_with_padding().collidepoint(self.parent.get_mouse_pos()))

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
                    if time.time() - self.key_hold_lengths[key] >= self.get_theme_val('key-repeat-delay', 150)*0.001:
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

    def draw_border(self, rect, border):
        rect = pygame.Rect(rect)
        left, right, top, bottom = border
        #each - texture, color, size

        #render borders
        i = left[0]
        if i != None:
            i = i.get_region((0,top[2],left[2],i.size[1]-bottom[2]))
        self.draw_rect((rect.left, rect.top+top[2], left[2], rect.height-top[2]-bottom[2]),
                       left[1], i)

        i = right[0]
        if i != None:
            i = i.get_region((i.size[0]-right[2],top[2],i.size[0],i.size[1]-bottom[2]))
        self.draw_rect((rect.right-right[2], rect.top+top[2], right[2], rect.height-top[2]-bottom[2]),
                       right[1], i)

        i = top[0]
        if i != None:
            n = i.get_region((0,0,i.size[0],top[2]))
        else:
            n = i
        self.draw_rect((rect.left, rect.top, rect.width, top[2]),
                       top[1], n)

        i = bottom[0]
        if i != None:
            n = i.get_region((0,i.size[1]-bottom[2],i.size[0],i.size[1]))
        else:
            n = i
        self.draw_rect((rect.left, rect.bottom-bottom[2], rect.width, bottom[2]),
                       bottom[1], n)

    def draw_canvas_border(self, rect, canvas):
        rect = pygame.Rect(rect)
        canvas = self.get_canvas(canvas)
        border = self.get_border()
        if border:
            left, right, top, bottom = border
            #each - texture, color, size

            l,t = rect.topleft
            w,h = rect.size
            l += left[2]
            t += top[2]
            w -= left[2] + right[2]
            h -= top[2] + bottom[2]
            self.draw_rect(pygame.Rect(l,t,w,h), canvas[1], canvas[0])

            #render borders
            self.draw_border(rect, border)
        else:
            self.draw_rect(rect, canvas[1], canvas[0])

    def draw_text(self, text, pos):
        font, size, color = self.get_font()
        down = font.get_height(size)
        x,y = pos
        for t in text.split('\n'):
            font.render(t, (x,y), color, size)
            y += down

    def get_text_size(self, text):
        font, size, color = self.get_font()
        width = 0
        height = 0
        down = font.get_height(size)
        for t in text.split('\n'):
            w,h = font.get_size(t, size)
            width = max((width, w))
            height += down

        return width, height

    def get_canvas(self, name):
        bg = self.get_theme_val(name, [])
        if bg == None:
            return None, Color((0,0,0,0))

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

    def get_background(self):
        return self.get_canvas('background')

    def get_border(self):
        bg = self.get_theme_val('border', None)
        if bg == None:
            return None
        Li = Ri = Ti = Bi = None
        Lc = Rc = Tc = Bc = Color((1,1,1,1))
        Ls = Rs = Ts = Bs = 0
        if bg:
            i = 0
            while i < len(bg):
                ii = bg[i]
                #all
                if ii == "block":
                    new, Ls, Rs, Ts, Bs = bg[i+1]
                    image = self.theme.get_texture(new)
                    Li = Ri = Ti = Bi = image
                    i += 1
                elif ii == "solid":
                    Li = Ri = Ti = Bi = None
                    Ls, Ts, Rs, Bs = bg[i+1]
                    i += 1
                elif ii == "color":
                    Lc = Rc = Tc = Bc = Color(bg[i+1])
                    i += 1

                #left
                elif ii == "block-left":
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
                elif ii == "block-right":
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
                elif ii == "block-top":
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
                elif ii == "block-bottom":
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
        return self.get_theme_val('visible', True)

    def get_font(self):
        name, size, color = self.get_theme_val('font', [None, 32, (0,0,0,1)])
        return (self.theme.get_font(name), size, Color(color))

    def get_padding(self):
        return self.get_theme_val('padding', (0,0,0,0))

    def am_active(self):
        if not self in self.parent.widgets:
            return False
        return (self.parent.am_active() and\
                self.parent.widgets.index(self) == 0) or\
                self.key_active

    def get_state(self):
        if self._mhold:
            return "click"
        if self._mhover:
            return "hover"
        if self.am_active() or self.key_active:
            return "active"

        return None

    def get_theme_val(self, name, default=None):
        state = self.get_state()

        reg = self.theme.get_val(name, default)

        if self.am_active() and name+"."+"active" in self.theme.vals:
            reg = self.theme.get_val(name+"."+"active", reg)

        if self._mhover:
            reg = self.theme.get_val(name+'.'+'hover', reg)

        if not state in ('click', 'hover', 'active', None):
            reg = self.theme.get_val(name+'.'+state, reg)

        return reg
