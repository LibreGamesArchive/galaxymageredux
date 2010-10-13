import widget
import time

import event

class Input(widget.Widget):
    def __init__(self, parent, width, pos, max_chars=50):
        widget.Widget.__init__(self, parent, pos)

        self.text = ""
        self.cursor_pos = 0

        self.width = width
        self.max_chars = max_chars
        self.size = self.get_size()

        self.bg_color = (.3,.3,.3)
        self.text_color = (1,1,0)

        self.dispatch.bind('keypress', self.handle_key)
        self.always_active = True
        self.key_active = True

        self.flash_timer = time.time()
        self.flash_space = 0.5
        self.flashed = False

    def can_handle_key(self, key, string):
        return True

    def unfocus(self):
        widget.Widget.unfocus(self)
        if self.always_active:
            self.key_active = True

    def handle_key(self, key, string):
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

            if self.max_chars >= 0 and len(self.text) >= self.max_chars:
                self.text = self.text[0:self.max_chars]
                self.cursor_pos = self.max_chars
        self.flash_timer = time.time()
        self.flashed = True
        return True

    def get_size(self):
        return self.width, self.font.get_height()

    def get_cursor_real_x(self):
        x = self.font.get_size(self.text[0:self.cursor_pos])[0]
        shift = 0
        if x > self.width:
            shift = x - self.width + 3

        return x, shift

    def render(self):
        self.size = self.get_size()

        x, shift = self.get_cursor_real_x()

        self.draw_rect(self.get_rect(), self.bg_color)
        sx, sy = self.pos.get_pos()
        self.screen.push_clip((sx, sy, self.size[0], self.size[1]))
        self.draw_text(self.text, (sx-shift, sy), self.text_color)
        self.screen.pop_clip()


        if time.time() - self.flash_timer > self.flash_space:
            self.flash_timer = time.time()
            self.flashed = not self.flashed

        if self.key_active and self.flashed:
            self.draw_rect((sx+x-shift+1, sy+1, 2, self.size[1]-2), self.text_color)
