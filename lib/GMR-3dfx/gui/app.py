from include import *
import theme

class App(object):
    def __init__(self, event_handler):

        self.screen = engine.display.get_display().screen
        self.event_handler = event_handler
        self.event_handler.gui = self
        self.event_handler.all_guis.append(self)
        self.widgets = []

        self.theme = theme.ThemeElement(None, None, None, None, {})

    def load_theme(self, name, texture_handler=None, font_handler=None):
        th = theme.Theme(name, texture_handler, font_handler)
        th.load_data()

        self.theme = th.get_element("App")

    def activate(self):
        self.event_handler.gui = self

    def get_root_app(self):
        return self

    def focus(self):
        pass

    def get_mouse_pos(self):
        #return pygame.mouse.get_pos()
        return self.event_handler.mouse.get_pos()

    def add_widget(self, widg):
        if not widg in self.widgets:
            self.widgets.insert(0, widg)

    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_mousedown(button, name):
                        return True
        return False

    def handle_mouseup(self, button, name):
        """Callback for mouse release events from the event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_mouseup(button, name):
                        return True
        return False

    def handle_mousehold(self, button, name):
        """Callback for mouse hold events from the event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_mousehold(button, name):
                        return True
        return False

    def handle_mousemotion(self, change):
        """Callback for mouse motion events from event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_mousemotion(change):
                        return True

    def handle_uncaught_event(self, event):
        """Callback for uncaught_event events from event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_uncaught_event(event):
                        return True
        return False

    def handle_keydown(self, key, string):
        """Callback for key press events from event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_keydown(key, string):
                        return True
        return False

    def handle_keyup(self, key, string):
        """Callback for key release events from event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_keyup(key, string):
                        return True
        return False

    def handle_keyhold(self, key, string):
        """Callback for key hold events from event_handler."""
        if self.get_visible():
            for i in self.widgets:
                if i.get_visible():
                    if i.handle_keyhold(key, string):
                        return True
        return False

    def next_widget(self):
        """Cycle widgets so next widget is top one."""
        for i in self.widgets[1:]:
            if i.get_visible():
                self.set_top_widget(i)
                return

    def set_top_widget(self, widg):
        """Moves widget 'widg' to top position."""
        if widg in self.widgets:
            self.widgets.remove(widg)
        self.widgets.insert(0, widg)
        for i in self.widgets:
            if i.get_visible():
                if not i == widg:
                    i.unfocus()

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
            elif ii == "solid":
                image = None
            elif ii == "color":
                color = Color(bg[i+1])
                i += 1
            i += 1

        return image, color

    def get_visible(self):
        return self.theme.get_val('visible', True)

    def render(self):
        if self.get_visible():
            image, color = self.get_canvas('background')
            engine.draw.rect2d(pygame.Rect((0,0),  self.screen.screen_size_2d),
                               color, image)

            self.widgets.reverse()
            for i in self.widgets:
                if i.get_visible(): i.render()
            self.widgets.reverse()

    def am_active(self):
        return self.event_handler.gui == self
