import widget, misc

class PopUp(widget.Widget):
    """Shows up on hover over parent"""
    def __init__(self, parent, pos=misc.RelativePos("left", "bottom"), text="", width=150):
        widget.Widget.__init__(self, parent.get_root_app(), pos)
        self.no_events = True

        self.attached_to = parent
        self.pos.to = self.attached_to
        self.text = text
        self.text_color = (0,0,0,1)

        self.width = width
        self.compile_text()
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
        widget.Widget.unfocus(self)
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
            if self.font.get_size(cur_line+" "+words[0])[0] > self.width:
                if cur_line: lines.append(cur_line)
                cur_line = words[0]
            else:
                cur_line += " " + words[0]

            words.pop(0)

        self.comp_text = lines

    def get_size(self):
        x = self.width
        y = self.font.get_height() * len(self.comp_text)

        return x, y

    def render(self):
        self.size = self.get_size()
        pos = self.pos.get_real_pos()
        if self.bg_color:
            self.draw_rect((pos, self.size), self.bg_color)

        x,y = pos
        down = self.font.get_height()
        for line in self.comp_text:
            self.font.render(line, (x,y), self.text_color)
            y += down
