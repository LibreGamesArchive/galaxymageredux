import widget
import time

import event

class Input(widget.Widget):
    widget_type = "Input"
    def __init__(self, parent, pos, name=None):
        widget.Widget.__init__(self, parent, pos, name)

        self.text = ""
        self.cursor_pos = 0

        self.dispatch.bind('keypress', self.handle_key)

        self.key_active = True
        self.flash_timer = time.time()
        self.flash_space = 0.5
        self.flashed = False

    def can_handle_key(self, key, string):
        return True

    def unfocus(self):
        widget.Widget.unfocus(self)
        if self.get_theme_val('always-active', True):
            self.key_active = True

    def handle_key(self, key, string):
        max_chars = self.get_theme_val('max-chars', 50)
        pos = self.cursor_pos
        if key == event.K_LEFT:
            if self.cursor_pos > 0: self.cursor_pos -= 1
        elif key == event.K_RIGHT:
            if self.cursor_pos < len(self.text): self.cursor_pos += 1
        elif key == event.K_HOME:
            self.cursor_pos = 0
        elif key == event.K_END:
            self.cursor_pos = len(self.text)
        elif key == event.K_DELETE:
            self.text = self.text[0:self.cursor_pos]+self.text[self.cursor_pos+1::]
        elif key == event.K_BACKSPACE:
            if self.cursor_pos:
                self.text = self.text[0:self.cursor_pos-1]+self.text[self.cursor_pos::]
                self.cursor_pos -= 1
        elif key == event.K_RETURN:
            self.dispatch.fire("input-submit", self.text)
        elif string and string in event.printable_chars:
            self.text = self.text[0:self.cursor_pos] + string + self.text[self.cursor_pos::]
            self.cursor_pos += 1

            if max_chars >= 0 and len(self.text) >= max_chars:
                self.text = self.text[0:max_chars]
                self.cursor_pos = max_chars
        if pos != self.cursor_pos:
            self.flash_timer = time.time()
            self.flashed = True
        return True

    def get_size(self):
        f = self.get_font()
        return (self.get_theme_val('width', 100),
                f[0].get_height(f[1]))

    def get_cursor_real_x(self):
        x = self.get_text_size(self.text[0:self.cursor_pos])[0]
        w,h = self.get_size()
        shift = 0
        if x > w:
            shift = x - w + 3

        return x, shift

    def render(self):
        size = self.get_size()

        pad = self.get_padding()

        x, shift = self.get_cursor_real_x()
        sx, sy = self.get_pos()
        w,h = self.get_size()

        self.draw_canvas_border((sx,sy,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')

        self.screen.push_clip((sx+pad[0], sy+pad[1], w, h))
        self.draw_text(self.text, (sx-shift+pad[0], sy+pad[1]),)
        self.screen.pop_clip()


        if time.time() - self.flash_timer > self.flash_space:
            self.flash_timer = time.time()
            self.flashed = not self.flashed

        if self.key_active and self.flashed:
            self.draw_rect((sx+x-shift+1+pad[0], sy+1+pad[1], 2, h-2), self.get_font()[2])
