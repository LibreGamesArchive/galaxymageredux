from gui.include import *
from engine.helpers import TextureHandler, FontHandler2D

class ThemeElement(object):
    def __init__(self, theme, parent, name, spec, vals):
        self.parent = parent
        self.theme_parent = theme
        self.name = name
        self.spec = spec
        self.vals = vals

        self.sub_vals = {}

    def update_vals(self, new):
        self.vals.update(new)

    def get_val(self, name, default=None):
        if name in self.vals:
            return self.vals[name]
        return default

    def get_element(self, name, spec=None):
        if not name in self.sub_vals:
            if self.parent == None:
                return ThemeElement(self.theme_parent,None,None,None,{})
            else:
                return self.parent.get_element(name, spec)
        if not spec in self.sub_vals[name]:
            spec = None
        return self.sub_vals[name][spec]

    def add_element(self, name, spec, vals):
        if not name in self.sub_vals:
            self.sub_vals[name] = {None:ThemeElement(self.theme_parent, self, name, None, {})}

        if not spec in self.sub_vals[name]:
            self.sub_vals[name][spec] = ThemeElement(self.theme_parent, self, name, spec, {})

        self.sub_vals[name][spec].update_vals(vals)
        return self.sub_vals[name][spec]

class Theme(object):
    def __init__(self, theme):
        if isinstance(theme, Theme):
            #copy vals
            self.theme_name = theme.theme_name
            self.textures = theme.textures
            self.fonts = theme.fonts
            self.root_element = theme.root_element
        else:
            self.theme_name = theme
            self._compile()

    def _compile(self):
        self.textures = TextureHandler()
        self.fonts = FontHandler2D()
        self.root_element = ThemeElement(self, None, None, None, {})

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

            last = self.root_element

            for name in name.split("#"):
                if "." in name:
                    widg, spec = name.split(".")
                else:
                    widg = name
                    spec = None

                if name in last.sub_vals:
                    last = last.get_element(widg, spec)
                else:
                    last = last.add_element(widg, spec, {})

            lines = values.split("\n")
            _vars = {}

            for line in lines:
                line = line.strip()
                if not ':' in line:
                    continue
                var, vals = line.split(":")
                var = var.strip()
                vals = vals.split()

                _vars[var] = vals
            last.update_vals(_vars)

    def get_root(self):
        return self.root_element

    def load_data(self):
        data_dir = self.root_element.get_element('*data_dir')
        if not data_dir.vals:
            dir = '.'
            font_tex = 1024
            font_size = 32
##            self.textures.load_dir(dir, False)
##            self.fonts.load_dir(dir, font_tex, font_size, False)
##            self.fonts.load_font(None, font_tex, font_size, False)

        for var in data_dir.vals:
            value = data_dir.vals[var]

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
##            self.textures.load_dir(dir, False)
##            self.fonts.load_dir(dir, font_tex, font_size, False)
##            self.fonts.load_font(None, font_tex, font_size, False)


def print_children(element, tab=""):
    print tab+str(element.name)+'.'+str(element.spec)
    for i in element.vals:
        print tab,i, "=", element.vals[i]
    for i in element.sub_vals:
        for x in element.sub_vals[i]:
            print_children(element.sub_vals[i][x], tab+":    ")

t = Theme('gui_theme.txt')
print_children(t.root_element)
t.load_data()
