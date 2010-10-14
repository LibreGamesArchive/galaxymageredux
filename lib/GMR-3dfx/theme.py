from gui.include import *
from engine.helpers import TextureHandler, FontHandler2D
from engine.misc import Color

class Theme(object):
    def __init__(self, theme):
        if isinstance(theme, Theme):
            #copy vals
            self.theme_name = theme.theme_name
            self.val_dict = theme.val_dict
            self.textures = theme.textures
            self.fonts = theme.fonts
        else:
            self.theme_name = theme
            self.val_dict = {}
            self.textures = TextureHandler()
            self.fonts = FontHandler2D()
            self._compile()

    def _compile(self):
        text = file(self.theme_name, 'rU').read()
        text.replace("\r", "\n")
        text.replace("\r\n", "\n")

        #remove comments
        while text.find('/*') != -1:
            start = text.find('/*')
            end = text.find('*/')+2
            text = text[0:start] + text[end::]

        blocks = text.split('}')

        for block in blocks:
            if not "{" in block:
                continue #woah
            name, values = block.split('{')
            name = name.strip()

            if "." in name:
                widg, spec = name.split(".")
            else:
                widg = name
                spec = None

            if not widg in self.val_dict:
                self.val_dict[widg] = {}
            self.val_dict[widg][spec] = {}

            lines = values.split("\n")

            for line in lines:
                line = line.strip()
                if not ':' in line:
                    continue
                var, vals = line.split(":")
                var = var.strip()
                vals = vals.split()

                self.val_dict[widg][spec][var] = vals

    def get_value(self, widget, name, var, default=None):
        if widget in self.val_dict and\
           name in self.val_dict[widget] and\
           var in self.val_dict[widget][name]:
            return self.val_dict[widget][name][var]
        return default

    def load_data(self):
        if '*data_dir' in self.val_dict:
            for var in self.val_dict['*data_dir'][None]:
                value = self.val_dict['*data_dir'][None][var]

                dir = value[0]
                value.pop(0)
                font_tex = 1024
                font_size = 32
                while value:
                    new = value.pop(0)
                    if new == 'font_tex':
                        font_tex = value.pop(0)
                    elif new == 'font_size':
                        font_size = value.pop(0)
                self.textures.load_dir(dir, False)
                self.fonts.load_dir(dir, font_tex, font_size, False)
                self.fonts.load_font(None, font_tex, font_size, False)


t = Theme('gui_theme.txt')
print t.val_dict

print t.val_dict['Button'][None]
print t.fonts.fonts
