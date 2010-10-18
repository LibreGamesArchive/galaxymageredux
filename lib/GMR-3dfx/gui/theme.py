from include import *
from engine.helpers import TextureHandler, FontHandler2D

class ThemeElement(object):
    def __init__(self, main_theme, parent, name, spec, vals):
        self.parent = parent
        self.main_theme = main_theme
        self.name = name
        self.spec = spec
        self.vals = vals

        if self.parent == None:
            self.parent_element = ThemeElement(self.main_theme,self,None,None,{})

        self.sub_vals = {}

    def get_texture(self, name):
        return self.main_theme.textures.get_texture(name)

    def get_font(self, name):
        return self.main_theme.fonts.get_font(name)

    def update_vals(self, new):
        self.vals.update(new)

    def set_val(self, name, value):
        self.vals[name] = value

    def get_val(self, name, default=None):
        if name in self.vals:
            return self.vals[name]
        return default

    def get_element(self, name, spec=None):
        if not name in self.sub_vals:
            if self.parent == None:
                return self.parent_element
            else:
                return self.parent.get_element(name, spec)
        if not spec in self.sub_vals[name]:
            spec = None
        return self.sub_vals[name][spec]

    def get_element_copy(self, name, spec=None):
        return ThemeElementCopy(self.get_element(name, spec))

    def add_element(self, name, spec, vals):
        if not name in self.sub_vals:
            self.sub_vals[name] = {None:ThemeElement(self.main_theme, self, name, None, {})}

        if not spec in self.sub_vals[name]:
            self.sub_vals[name][spec] = ThemeElement(self.main_theme, self, name, spec, {})

        self.sub_vals[name][spec].update_vals(vals)
        return self.sub_vals[name][spec]

    def get_root(self):
        if self.parent == None:
            return ThemeElementCopy(self)
        return self.parent.get_root()

class ThemeElementCopy(ThemeElement):
    def __init__(self, element):
        self.parent = element.parent
        self.main_theme = element.main_theme
        self.name = str(element.name)
        self.spec = str(element.spec)
        self.vals = dict(element.vals)

        if self.parent == None:
            self.parent_element = element.parent_element

        self.sub_vals = element.sub_vals

class Theme(object):
    def __init__(self, theme, texture_handler=None, font_handler=None):
        if isinstance(theme, Theme):
            #copy vals
            self.theme_name = theme.theme_name
            if texture_handler == None:
                self.textures = theme.textures
            else:
                self.textures = texture_handler
            if font_handler == None:
                self.fonts = theme.fonts
            else:
                self.fonts = font_handler
            self.root_element = theme.root_element
        else:
            self.theme_name = theme
            if texture_handler == None:
                self.textures = TextureHandler()
            else:
                self.textures = texture_handler
            if font_handler == None:
                self.fonts = FontHandler2D()
            else:
                self.fonts = font_handler
            self.root_element = ThemeElement(self, None, None, None, {})

            if not self.theme_name == None:
                self.update(self.theme_name)

    def build_array(self, val):
        vals = val.split(",")
        ret = []
        for i in vals:
            i = i.strip()
            ret.append(self.to_value(i))
        if len(ret) == 1:
            ret = ret[0]
        return ret

    def to_value(self, val):
        if val.lower() == "none": return None
        if val.lower() == "true": return True
        if val.lower() == "false": return False
        try: return int(val)
        except:pass
        try: return float(val)
        except: pass

        return val

    def update(self, filename):
        text = file(filename, 'rU').read()
        text = text.replace("(", " ( ")
        text = text.replace(")", " ) ")

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

            lasts = []

            for name in name.split(','):
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
                lasts.append(last)

            lines = values.split(";")
            _vars = {}

            for line in lines:
                line = line.strip()
                if not ':' in line:
                    continue
                var, vals = line.split(":")
                var = var.strip()
                vals = vals.split()

                new_vals = []
                cur_val = ""
                arr = False
                for i in vals:
                    if i == "(":
                        arr = True
                    elif i == ")":
                        arr = False
                        if cur_val:
                            new_vals.append(self.build_array(cur_val))
                        else:
                            new_vals.append("")
                        cur_val = ""
                    else:
                        if arr:
                            cur_val += " "+i
                        else:
                            new_vals.append(self.to_value(i))

                if len(new_vals) == 1:
                    new_vals = new_vals[0]
                _vars[var] = new_vals
            for last in lasts:
                last.update_vals(_vars)

    def get_root(self):
        return self.root_element

    def get_element(self, name, spec=None):
        return self.root_element.get_element(name, spec)

    def get_element_copy(self, name, spec=None):
        return ThemeElementCopy(self.get_element(name, spec))

    def load_data(self):
        data_dir = self.root_element.get_element('<data_dir>')
        if not data_dir.vals:
            dir = '.'
            font_tex = 1024
            font_size = 32

            self.textures.load_dir(dir)
            self.fonts.load_dir(dir, font_tex, font_size)

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

            self.textures.load_dir(dir)
            self.fonts.load_dir(dir, font_tex, font_size)
        self.fonts.load_font(None, font_tex, font_size)
