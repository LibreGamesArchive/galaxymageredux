import widget, container, dropdown, misc

class MenuEntry(widget.Widget):
    widget_type = "Entry"
    def __init__(self, parent, pos, text, disabled=False):
        widget.Widget.__init__(self, parent, pos, None)

        self.text = text
        self.disabled = disabled

        self.size = self.get_text_size(text)
        self.dispatch.bind('unhover', self.keep_off_held_if_unhover)

    def keep_off_held_if_unhover(self):
        self._mhold = False

    def get_size(self):
        return self.size

    def get_state(self):
        if self.disabled:
            return 'disabled'
        return widget.Widget.get_state(self)

    def render(self):
        pad = self.get_padding()
        down = 0
        x,y = self.get_pos()
        w,h = self.get_size()
        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')
        self.draw_text(self.text, (x+pad[0], y+pad[1]))

class Menu(container.Container):
    widget_type = "Menu"
    def __init__(self, parent, pos, options=[], name=None):
        container.Container.__init__(self, parent, (1,1), pos, name)

        self.options = options

        self.build_options()

    def build_options(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.options:
            if type(opt) is type(""):
                dis = False
            else:
                opt, dis = opt
            if self.widgets:
                pos = misc.RelativePos()
            else:
                pos = misc.AbsolutePos((0,0))
            new = MenuEntry(self, pos, opt, dis)
            new.dispatch.bind('click', lambda new=new:self.dispatch.fire('select', new))

            s = new.get_size_with_padding()
            width = max(width, s[0])
            height = new.get_pos()[1]+s[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))

    def try_fire_select(self, widg):
        if not widg.disabled:
            self.dispatch.fire('select', widg)

class DDMMenu(Menu):
    def __init__(self, parent, pos, options=[]):
        Menu.__init__(self, parent.parent, pos, [])

        self.theme = parent.theme.get_element('Menu', None)

        self.options = options
        self.build_options()

class DropDownMenu(dropdown.DropDown):
    widget_type = "DropDownMenu"
    def __init__(self, parent, pos, text, options=[], name=None):
        dropdown.DropDown.__init__(self, parent, pos, text, None, name)

        self.setChild(DDMMenu(self, misc.RelativePos(to=self), options))

        self.child.dispatch.bind('select', self.fire_event)

    def fire_event(self, item):
        self.dispatch.fire('select', item)
        self.turn_off()
