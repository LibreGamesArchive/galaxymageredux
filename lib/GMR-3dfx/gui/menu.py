import widget, container, dropdown, misc

class MenuEntry(widget.Widget):
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos)

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
        width, height = self.parent.font.get_size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        r = self.get_rect()
        if self.parent.entry_bg_color:
            self.draw_rect(r, self.parent.entry_bg_color)
        self.draw_text(self.text, r.topleft, self.text_color)

class Menu(container.Container):
    def __init__(self, parent, pos, options=[], padding=(0,0)):
        container.Container.__init__(self, parent, (1,1), pos)

        self.entry_text_reg_color = (0,0,0)
        self.entry_text_hover_color = (.25,.25,.25)
        self.entry_text_click_color = (.5,.5,.5)
        self.entry_bg_color = (1,1,1)

        self.options = options
        self.padding = padding

        self.build_options()

    def build_options(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.options:
            if self.widgets:
                pos = misc.RelativePos(pady=self.padding[1])
            else:
                pos = misc.AbsolutePos(self.padding)
            new = MenuEntry(self, pos, opt)
            new.dispatch.bind('click', lambda:self.dispatch.fire('select', self.widgets[0].text))

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))


class MenuDisableEntry(widget.Widget):
    def __init__(self, parent, pos, text, dis):
        widget.Widget.__init__(self, parent, pos)

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
        width, height = self.parent.font.get_size(self.text)
        return width, height

    def render(self):
        self.size = self.get_size()
        r = self.get_rect()
        if self.disabled:
            bg = self.parent.entry_dis_bg_color
        else:
            bg = self.parent.entry_bg_color
        if bg:
            self.draw_rect(r, bg)
        self.draw_text(self.text, r.topleft, self.text_color)

class DisableMenu(container.Container):
    def __init__(self, parent, pos, options=[], padding=(0,0)):
        container.Container.__init__(self, parent, (1,1), pos)

        self.entry_text_reg_color = (0,0,0)
        self.entry_text_hover_color = (.25,.25,.25)
        self.entry_text_click_color = (.5,.5,.5)
        self.entry_bg_color = (1,1,1)
        self.entry_dis_bg_color = (0,0,0)
        self.entry_dis_text_reg_color = (.3,.3,.3)
        self.entry_dis_text_hover_color = (.3,.3,.3)
        self.entry_dis_text_click_color = (.3,.3,.3)

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
                pos = misc.RelativePos(pady=self.padding[1])
            else:
                pos = misc.AbsolutePos(self.padding)
            new = MenuDisableEntry(self, pos, opt, dis)
            new.dispatch.bind('click', lambda:self.dispatch.fire('select', self.widgets[0].text, self.widgets[0].disabled))

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width+self.padding[0]*2, height+self.padding[1]))


class DropDownMenu(dropdown.DropDown):
    def __init__(self, parent, pos, text, options=[], padding=(0,0)):
        child = Menu(parent, misc.RelativePos(to=self), options, padding)

        dropdown.DropDown.__init__(self, parent, pos, text, child)

        self.child.dispatch.bind('select', self.fire_event)

    def fire_event(self, item):
        self.dispatch.fire('select', item)
        self.turn_off()
