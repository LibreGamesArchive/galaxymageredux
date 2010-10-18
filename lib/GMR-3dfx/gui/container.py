from include import *

import app, widget

class Container(widget.Widget, app.App):
    widget_type = "Container"
    def __init__(self, parent, size, pos, name=None):
        self.widgets = []
        widget.Widget.__init__(self, parent, pos, name)
        self.size = size

        self.dispatch = event.Dispatcher()

        self.dispatch.bind("unhover", self.unhover_all_widgets)

    def change_size(self, new):
        self.size = new

    def update_theme(self):
        widget.Widget.update_theme(self)
        self.update_child_theme()

    def update_child_theme(self):
        for i in self.widgets:
            i.update_theme()

    def unhover_all_widgets(self):
        for i in self.widgets:
            n = i._mhover
            i._mhover = False
            if n == True:
                i.dispatch.fire("unhover")

    def get_mouse_pos(self):
        x,y = self.parent.get_mouse_pos()
        xx, yy = self.pos.get_pos()
        x = x - xx
        y = y - yy
        return x,y

    def handle_mousedown(self, button, name):
        """Callback for mouse click events from the event_handler."""
        x = widget.Widget.handle_mousedown(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.get_visible():
            return False
        for i in self.widgets:
            if i.get_visible():
                if i.handle_mousedown(button, name):
                    return True
        return x

    def handle_mouseup(self, button, name):
        """Callback for mouse release events from the event_handler."""
        x = widget.Widget.handle_mouseup(self, button, name)
        if not self.mouse_on_me():
            return False
        if not self.get_visible():
            return False
        for i in self.widgets:
            if i.get_visible():
                if i.handle_mouseup(button, name):
                    return True
        return x

    def handle_mousehold(self, button, name):
        """Callback for mouse hold events from the event_handler."""
        if widget.Widget.handle_mousehold(self, button, name):
            app.App.handle_mousehold(self, button, name)
            return True
        return False

    def handle_mousemotion(self, change):
        """Callback for mouse motion events from event_handler."""
        if widget.Widget.handle_mousemotion(self, change):
            app.App.handle_mousemotion(self, change)
            return True
        return False

    def handle_uncaught_event(self, event):
        """Callback for uncaught_event events from event_handler."""
        if widget.Widget.handle_uncaught_event(self, event):
            app.App.handle_uncaught_event(self, event)
            return True
        return False

    def can_handle_key(self, key, string):
        for i in self.widgets:
            if i.can_handle_key(key, string):
                return True
        return False

    def handle_keydown(self, key, string):
        """Callback for key press events from event_handler."""
        return app.App.handle_keydown(self, key, string)

    def handle_keyup(self, key, string):
        """Callback for key release events from event_handler."""
        return app.App.handle_keyup(self, key, string)

    def handle_keyhold(self, key, string):
        """Callback for key hold events from event_handler."""
        return app.App.handle_keyhold(self, key, string)

    def get_size(self):
        return self.size

    def render(self):
        r = self.get_rect()
        self.draw_canvas_border(r, 'background')

        self.screen.push_clip(r)
        glPushMatrix()
        glTranslatef(r.left,r.top,0)

        self.widgets.reverse()
        for i in self.widgets:
            if i.get_visible(): i.render()
        self.widgets.reverse()
        glPopMatrix()
        self.screen.pop_clip()
