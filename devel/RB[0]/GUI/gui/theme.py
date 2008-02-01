import os
import pygame

import safe_python

global __cur, __theme
__theme = ""
__cur = {"button":None,
       "label":None,
       "window":None,
       "container":None,
       "window_bar":None,
       "scroll_bar":None,
       "menu":None,

       "font":None}

def make_image(d):
    if not d == "noimage":
        return pygame.image.load(os.path.join(__theme, d)).convert_alpha()
    return d

def Button(default, hover, click, text_color):
    __cur["button"] = {"default": make_image(default),
                     "hover": make_image(hover),
                     "click": make_image(click),
                     "text-color": text_color}

def Label(image, text_color):
    __cur["label"] = {"image": make_image(image),
                      "text-color": text_color}

def Container(default, hover, click):
    __cur["container"] = {"default": make_image(default),
                        "hover": make_image(hover),
                        "click": make_image(click)}

def WindowBar(default, hover, click, text_color):
    __cur["window_bar"] = {"default": make_image(default),
                         "hover": make_image(hover),
                         "click": make_image(click),
                         "text-color": text_color}

def Window(default, hover, click):
    __cur["window"] = {"default": make_image(default),
                     "hover": make_image(hover),
                     "click": make_image(click)}

def ScrollBar(default, hover, click):
    __cur["scroll_bar"] = {"default": make_image(default),
                         "hover": make_image(hover),
                         "click": make_image(click)}

def Menu(border, entry_default, entry_hover, entry_click, entry_text_color):
    __cur["menu"] = {"border": make_image(border),
                  "entry-default": make_image(entry_default),
                  "entry-hover": make_image(entry_hover),
                  "entry-click": make_image(entry_click),
                  "entry-text-color": entry_text_color}

def Input(border, entry_text_color):
    __cur["input"] = {"border": make_image(border),
                      "entry-text-color": entry_text_color}

def Font(font, size, aa):
    __cur["font"] = {"font": os.path.join(__theme, font),
                     "size": size,
                     "aa": aa}

def make_theme(theme):
    if not safe_python.test_safe(os.path.join(theme, "theme.txt"),
                                 ["Button", "Label",
                                  "Container",
                                  "WindowBar",
                                  "Window", "Menu",
                                  "ScrollBar",
                                  "Font", "Input"]):
        BadThemeError = "this theme is corrupted"
        raise BadThemeError

    global __cur
    __cur = {"button":None,
           "label":None,
           "window":None,
           "container":None,
           "window_bar":None,
           "scroll_bar":None,
           "menu":None,

           "font":None,
             "input":None}
    global __theme
    __theme = theme

    data = open(os.path.join(__theme, "theme.txt"), "rU").read()

    exec data

    a = Theme(theme)
    a.compile_theme(__cur)
    return a

class Theme(object):
    def __init__(self, theme):
        self.theme = theme

        self.font = {"font": "Vera.ttf",
                     "size": 20,
                     "aa": 1}

        self.button = {"default":"noimage",
                       "hover":"noimage",
                       "click":"noimage",
                       "text-color":(0, 0, 0)}

        self.container = {"default":"noimage",
                          "hover":"noimage",
                          "click":"noimage"}
        self.window_bar = {"default":"noimage",
                           "hover":"noimage",
                           "click":"noimage",
                           "text-color":(0, 0, 0)}

        self.window = {"default":"noimage",
                       "hover":"noimage",
                       "click":"noimage"}

        self.label = {"image":"noimage",
                      "text-color":(0, 0, 0)}

        self.scroll_bar = {"default":"noimage",
                           "hover":"noimage",
                           "click":"noimage"}

        self.menu = {"border":"noimage",
                     "entry-default":"noimage",
                     "entry-hover":"noimage",
                     "entry-click":"noimage",
                     "entry-text-color":(0,0,0)}

        self.input = {"border":"noimage",
                      "entry-text-color":(0, 0, 0)}

    def compile_theme(self, cur):
        if cur["button"]:
            self.button = cur["button"]

        if cur["label"]:
            self.label = cur["label"]

        if cur["container"]:
            self.container = cur["container"]

        if cur["window_bar"]:
            self.window_bar = cur["window_bar"]

        if cur["window"]:
            self.window = cur["window"]

        if cur["scroll_bar"]:
            self.scroll_bar = cur["scroll_bar"]

        if cur["menu"]:
            self.menu = cur["menu"]

        if cur["font"]:
            self.font = cur["font"]

        if cur["input"]:
            self.input = cur["input"]
