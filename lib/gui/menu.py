import list, dropdown, misc

class MenuEntry(list.ListEntry):
    widget_type = "Entry"
    def __init__(self, parent, pos, text, disabled=False):
        self.disabled = disabled
        list.ListEntry.__init__(self, parent, pos, text)

        self.dispatch.bind('unhover', self.keep_off_held_if_unhover)

    def keep_off_held_if_unhover(self):
        self._mhold = False

    def get_state(self):
        if self.disabled:
            return 'disabled'
        return list.ListEntry.get_state(self)

class Menu(list.List):
    widget_type = "Menu"

    def build_entries(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.entries:
            if type(opt) is type(""):
                dis = False
            else:
                opt, dis = opt
            if self.widgets:
                pos = misc.RelativePos()
            else:
                pos = misc.AbsolutePos((0,0))
            new = MenuEntry(self, pos, opt, dis)
            new.dispatch.bind('click',
                              lambda new=new:self.dispatch.fire('select', new))

        self.check_size()

    def try_fire_select(self, widg):
        if not widg.disabled:
            self.dispatch.fire('select', widg)

class DDMMenu(Menu):
    widget_type = 'Menu'
    def __init__(self, parent, pos, entries=[]):
        self.drop_down = parent

        Menu.__init__(self, parent.parent, pos, [])

        self.update_theme()

        self.entries = entries
        self.build_entries()

    def update_theme(self):
        self.theme = self.drop_down.theme.get_element_copy('Menu', None)
        self.update_child_theme()

class DropDownMenu(dropdown.DropDown):
    widget_type = "DropDownMenu"
    def __init__(self, parent, pos, text, options=[], name=None):
        self.child = None
        dropdown.DropDown.__init__(self, parent, pos, text, None, name)

        self.setChild(DDMMenu(self, misc.RelativePos(to=self), options))

        self.child.dispatch.bind('select', self.fire_event)

    def fire_event(self, item):
        self.dispatch.fire('select', item)
        if item.disabled:
            return
        self.turn_off()

    def update_child_theme(self):
        if self.child:
            self.child.update_theme()

    def update_theme(self):
        dropdown.DropDown.update_theme(self)
        self.update_child_theme()
