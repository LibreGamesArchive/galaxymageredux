import os
import copy

import pygame
from pygame.locals import *

from theme import make_theme, Theme

class App(object):
    def __init__(self, surface,
                 background_color=(0, 0, 0)):

        self.surface = surface

        self.widgets = []

        self.theme = None

        self.dirty = False
        self.background_color = background_color

    def move_to_top(self, other):
        i = self.widgets.index(other)
        self.widgets.insert(0, self.widgets.pop(i))
        self.dirty = True
        return None

    def add_widget(self, widg, name):
        self.widgets.insert(0, widg)

        return None

    def remove_widget(self, name):
        for i in self.widgets:
            if i.name == name:
                self.widgets.remove(i)
                break
        return None

    def get_events(self):
        return_events = []

        for event in pygame.event.get():
            for widg in self.widgets:
                ret = widg.event(event)
                if ret == event:
                    continue
                else:
                    if ret:
                        return_events.append(ret)
                    break

        return return_events

    def render(self):
        if self.dirty:
            self.surface.fill(self.background_color)
            self.widgets.reverse()
            for i in self.widgets:
                i.render(self.surface)
            self.widgets.reverse()
            self.dirty = False
        return self.surface

        
def resize_image(image, size):
    x, y = size
    if x < image.get_width(): x = image.get_width()
    if y < image.get_height(): y = image.get_height()
    bsize = (image.get_width() / 3,
             image.get_height() / 3)

    topleft = image.subsurface((0, 0), bsize)
    top = pygame.transform.scale(image.subsurface((bsize[0], 0), bsize),
                                 (size[0] - bsize[0] * 2, bsize[1]))
    topright = image.subsurface((bsize[0] * 2, 0), bsize)

    left = pygame.transform.scale(image.subsurface((0, bsize[1]), bsize),
                                  (bsize[0], size[1] - bsize[1] * 2))
    middle = pygame.transform.scale(image.subsurface((bsize[0], bsize[1]), bsize),
                                    (size[0] - bsize[0] * 2,
                                     size[1] - bsize[1] * 2))
    right = pygame.transform.scale(image.subsurface((bsize[0] * 2, bsize[1]), bsize),
                                   (bsize[0], size[1] - bsize[1] * 2))

    botleft = image.subsurface((0, bsize[1] * 2), bsize)
    bottom = pygame.transform.scale(image.subsurface((bsize[0], bsize[1] * 2), bsize),
                                    (size[0] - bsize[0] * 2, bsize[1]))
    botright = image.subsurface((bsize[0] * 2, bsize[1] * 2), bsize)

    new = pygame.Surface(size).convert()
    new.blit(topleft, (0, 0))
    new.blit(top, (bsize[0], 0))
    new.blit(topright, (size[0] - bsize[0], 0))

    new.blit(left, (0, bsize[1]))
    new.blit(middle, bsize)
    new.blit(right, (size[0] - bsize[0], bsize[1]))

    new.blit(botleft, (0, size[1] - bsize[1]))
    new.blit(bottom, (bsize[0], size[1] - bsize[1]))
    new.blit(botright, (size[0] - bsize[0], size[1] - bsize[1]))
    return new


class Widget(object):
    def __init__(self, parent, pos = (-1, -1), name="",
                 widget_pos="topleft"):
        self.parent = parent
        self.parent.add_widget(self, name)

        self.name = name

        self.theme = copy.copy(self.parent.theme)

        x, y = pos
        if x == -1:
            x = int(self.parent.surface.get_width() / 2)
        if y == -1:
            y = int(self.parent.surface.get_height() / 2)
        self.pos = (x, y)

        self.widget_pos = widget_pos

        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rect.center = self.pos

    def render(self, surface, offset=(0, 0)):
        pass

    def event(self, event, offset=(0, 0)):
        return event

    def move(self, off):
        x, y = self.pos
        x += off[0]
        y += off[1]

        self.pos = (x, y)
        setattr(self.rect, self.widget_pos, self.pos)
        return None


class Label(Widget):
    def __init__(self, parent, pos, name, text,
                 font=None, image=None,
                 widget_pos="topleft",
                 icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.text = text

        self.over_image = image
        self.over_font = font

        self.over_width = None

        self.icon = icon
        if self.icon:
            self.icon = pygame.image.load(os.path.join(self.theme.theme, self.icon)).convert_alpha()

        self.make_image()

    def __combine_images(self, images):
        flags = images[-1].get_flags()
        width = 0
        height = 0
        for i in images:
            width += i.get_width()
            if i.get_height() > height:
                height = i.get_height()

        new = pygame.Surface((width, height), flags).convert_alpha()
        new.fill((0,0,0,0))
        lx = 0
        for i in images:
            new.blit(i, (lx, 0))
            lx += i.get_width()
        return new

    def make_image(self):
        if self.over_font:
            font = pygame.font.Font(self.over_font["font"],
                                    self.over_font["size"])
            tex = font.render(self.text, self.over_font["aa"],
                              self.over_font["text-color"])
            if self.icon:
                tex = self.__combine_images([self.icon, tex])
            if self.over_image == "noimage":
                self.comp_image = tex
            elif self.over_image:
                image = self.over_image
                bsize = (image.get_width() / 3,
                         image.get_height() / 3)
                rect = tex.get_rect()
                rect.width += bsize[0] * 2
                rect.height += bsize[1] * 2
                if self.over_width:
                    rect.width = self.over_width
                new = resize_image(image, rect.size)
                new.blit(tex, bsize)
                self.comp_image = new
            elif self.theme.label["image"]:
                image = self.theme.label["image"]
                bsize = (image.get_width() / 3,
                         image.get_height() / 3)
                rect = tex.get_rect()
                rect.width += bsize[0] * 2
                rect.height += bsize[1] * 2
                if self.over_width:
                    rect.width = self.over_width
                new = resize_image(image, rect.size)
                new.blit(tex, bsize)
                self.comp_image = new
            else:
                self.comp_image = tex
            self.rect = self.comp_image.get_rect()
            self.rect.center = self.pos
            return None
        else:
            if self.theme and self.theme.font["font"]:
                font = pygame.font.Font(self.theme.font["font"],
                                        self.theme.font["size"])
                tex = font.render(self.text, self.theme.font["aa"],
                                  self.theme.label["text-color"])
                if self.icon:
                    tex = self.__combine_images([self.icon, tex])
                if self.over_image == "noimage":
                    self.comp_image = tex
                elif self.over_image:
                    image = self.over_image
                    bsize = (image.get_width() / 3,
                             image.get_height() / 3)
                    rect = tex.get_rect()
                    rect.width += bsize[0] * 2
                    rect.height += bsize[1] * 2
                    if self.over_width:
                        rect.width = self.over_width
                    new = resize_image(image, rect.size)
                    new.blit(tex, bsize)
                    self.comp_image = new
                elif self.theme.label["image"]:
                    image = self.theme.label["image"]
                    bsize = (image.get_width() / 3,
                             image.get_height() / 3)
                    rect = tex.get_rect()
                    rect.width += bsize[0] * 2
                    rect.height += bsize[1] * 2
                    if self.over_width:
                        rect.width = self.over_width
                    new = resize_image(image, rect.size)
                    new.blit(tex, bsize)
                    self.comp_image = new
                else:
                    self.comp_image = tex
            else:
                if self.icon:
                    self.comp_image = self.icon
                else:
                    self.comp_image = pygame.Surface((1, 1))
            self.rect = self.comp_image.get_rect()
            setattr(self.rect, self.widget_pos, self.pos)
            return None
        return None

    def render(self, surface, offset=(0, 0)):
        pos = self.rect.left + offset[0], self.rect.top + offset[1]
        surface.blit(self.comp_image, pos)
        return None

class Button(Widget):
    def __init__(self, parent, pos, name, text,
                 font=None, images=None,
                 widget_pos="topleft",
                 icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.over_font = font
        self.over_images = images

        self.text = text

        self.over_width = None

        self.icon = icon

        self.make_image()

        self.__mouse_hold_me = False

    def add_widget(self, *other):
        pass

    def move_to_top(self, other):
        self.parent.move_to_top(self)

    def make_image(self):
        if self.over_font:
            font = self.over_font
        elif self.theme and self.theme.font:
            font = self.theme.font
            font["text-color"] = self.theme.button["text-color"]
        else:
            font = None

        if self.over_images:
            self.regular = Label(self, self.pos, self.name, self.text,
                                 font, self.over_images[0],
                                 icon=self.icon)
            self.regular.over_width = self.over_width
            self.regular.make_image()

            self.hover = Label(self, self.pos, self.name, self.text,
                               font, self.over_images[1],
                               icon=self.icon)
            self.hover.over_width = self.over_width
            self.hover.make_image()

            self.click = Label(self, self.pos, self.name, self.text,
                               font, self.over_images[2],
                                 icon=self.icon)
            self.click.over_width = self.over_width
            self.click.make_image()

        elif self.theme and self.theme.button:
            self.regular = Label(self, self.pos, self.name, self.text,
                                 font, self.theme.button["default"],
                                 icon=self.icon)
            self.regular.over_width = self.over_width
            self.regular.make_image()

            self.hover = Label(self, self.pos, self.name, self.text,
                               font, self.theme.button["hover"],
                                 icon=self.icon)
            self.hover.over_width = self.over_width
            self.hover.make_image()

            self.click = Label(self, self.pos, self.name, self.text,
                               font, self.theme.button["click"],
                                 icon=self.icon)
            self.click.over_width = self.over_width
            self.click.make_image()

        else:
            self.regular = Label(self, self.pos, self.name, self.text,
                                 font, icon=self.icon)

            self.hover = Label(self, self.pos, self.name, self.text,
                               font, icon=self.icon)

            self.click = Label(self, self.pos, self.name, self.text,
                               font, icon=self.icon)

        self.image = self.regular
        self.rect = self.image.comp_image.get_rect()
        setattr(self.rect, self.widget_pos, self.pos)
        self.parent.dirty = True

    def render(self, surface, offset=(0,0)):
        pos = self.rect.left + offset[0], self.rect.top + offset[0]
        surface.blit(self.image.comp_image, pos)
        return None

    def change_image(self, new):
        if not self.image == new:
            self.image = new
            self.parent.dirty = True
        return None

    def event(self, event, offset=(0, 0)):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] - offset[0], mpos[1] - offset[1]
        if self.rect.collidepoint(mpos):
            if self.__mouse_hold_me:
                self.change_image(self.click)
            else:
                self.change_image(self.hover)
        else:
            self.change_image(self.regular)

        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mpos):
                self.change_image(self.click)
                self.__mouse_hold_me = True
                self.parent.move_to_top(self)
                return None
            return event
        if event.type == MOUSEBUTTONUP:
            if self.__mouse_hold_me:
                self.__mouse_hold_me = False
                if self.rect.collidepoint(mpos):
                    self.change_image(self.regular)
                    self.parent.move_to_top(self)
                    return Event(Button, self.name, GUI_EVENT_CLICK)
                return None
            return event
        return event


class MenuList(Widget):
    def __init__(self, parent, pos, name="",
                 buttons=["None"],
                 font=None, images=None,
                 widget_pos="topleft",
                 icons={"None":None}):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.button_list = buttons
        self.icons = icons

        self.over_font = font
        self.over_images = images

        self.dirty = False
        self.surface = pygame.Surface((1, 1))
        self.draw_area = pygame.Surface((1, 1))

        self.make_image()

    def make_image(self):
        buttons = []

        if self.over_font:
            font = self.over_font
        elif self.theme and self.theme.font:
            font = self.theme.font
            font["text-color"] = self.theme.menu["entry-text-color"]

        if self.over_images:
            height = 0
            width = 0
            for i in self.button_list:
                try:
                    x = self.icons[i]
                except:
                    x = None
                new = Button(self, (0, height), i, i,
                             font, self.over_images,
                             icon=x)
                height += new.rect.height
                if new.rect.width > width:
                    width = new.rect.width
                buttons.append(new)

        else:
            oimages = [self.theme.menu["entry-default"],
                       self.theme.menu["entry-hover"],
                       self.theme.menu["entry-click"]]
            height = 0
            width = 0
            for i in self.button_list:
                try:
                    x = self.icons[i]
                except:
                    x = None
                new = Button(self, (0, height), i, i,
                             font, oimages,
                             icon=x)
                height += new.rect.height
                if new.rect.width > width:
                    width = new.rect.width
                buttons.append(new)

        for i in buttons:
            i.over_width = width
            i.make_image()

        if self.theme and self.theme.menu["border"]:
            image = self.theme.menu["border"]
            bsize = (image.get_width() / 3,
                     image.get_height() / 3)
            image = resize_image(image, (width + bsize[0] * 2,
                                         height + bsize[1] * 2))
            self.surface = image
            self.draw_area = self.surface.subsurface(bsize,
                                        (image.get_width() - bsize[0],
                                         image.get_height() - bsize[1]))
            self.old_draw_area = self.draw_area.copy()
        else:
            self.surface = pygame.Surface((0, 0))
            self.draw_area = self.surface
            self.old_draw_area = self.surface
        self.rect = self.surface.get_rect()
        setattr(self.rect, self.widget_pos, self.pos)
        self.parent.dirty = True
        self.dirty = True

        self.buttons = buttons

    def add_widget(self, *other):
        pass

    def move_to_top(self, other):
        self.parent.move_to_top(self)

    def render(self, surface, offset=(0, 0)):
        pos = self.pos[0] + offset[0], self.pos[1] + offset[1]
        if self.dirty:
            self.draw_area.blit(self.old_draw_area, (0, 0))
            for i in self.buttons:
                i.render(self.draw_area, offset)
            self.dirty = False
        surface.blit(self.surface, self.rect)
        return None

    def event(self, event, offset=(0, 0)):
        offset = offset[0] + self.rect.left, offset[1] + self.rect.top
        for i in self.buttons:
            x = i.event(event, offset)
            if not x == event:
                if x:
                    x.widget = MenuList
                    x.entry = x.name
                    x.name = self.name
                event = x
                break
        if self.dirty:
            self.parent.dirty = True
        return event           

class Menu(Widget):
    def __init__(self, parent, pos, name, text,
                 buttons=["None"], icons={"None":None},
                 font=None, images=None,
                 widget_pos="topleft",
                 icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.text = text
        self.buttons = buttons
        self.icons = icons
        self.icon = icon

        self.over_font = font
        self.over_images = images

        self.make_image()

        self.widget_vis = False

    def move_to_top(self, other):
        self.parent.move_to_top(self)

    def make_image(self):
        images = []
        if self.over_font:
            font = self.over_font
        elif self.theme and self.theme.font:
            font = self.theme.font
            font["text-color"] = self.theme.menu["entry-text-color"]

        if self.over_images:
            images = self.over_images
        elif self.theme:
            images = [self.theme.menu["entry-default"],
                      self.theme.menu["entry-hover"],
                      self.theme.menu["entry-click"]]

        self.button = Button(self, self.pos, self.name, self.text,
                             font, images, self.widget_pos, self.icon)

        self.other = MenuList(self, (self.pos[0], self.pos[1] + self.button.rect.height),
                              "", self.buttons, font, images, self.widget_pos, self.icons)

    def add_widget(self, *other):
        pass

    def event(self, event, offset=(0, 0)):
        x = self.button.event(event, offset)
        if not x == event:
            if x:
                if x.type == GUI_EVENT:
                    if x.widget == Button:
                        if x.action == GUI_EVENT_CLICK:
                            self.widget_vis = not self.widget_vis
        else:
            if self.widget_vis:
                x = self.other.event(event)
                if not x == event:
                    if x:
                        x.widget = Menu
                        x.name = self.name
                    event = x
                else:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mpos = pygame.mouse.get_pos()
                            mpos = mpos[0] - offset[0], mpos[1] - offset[1]
                            if not self.other.rect.collidepoint(mpos):
                                self.widget_vis = False
                            else:
                                event = None
        if self.dirty:
            self.parent.dirty = True

        return event

    def render(self, surface, offset=(0, 0)):
        self.button.render(surface, offset)
        if self.widget_vis:
            self.other.render(surface, offset)
        return None

class TextInputBox(Widget):
    def __init__(self, parent, pos, name,
                 prompt, starting_text,
                 size = 25,
                 font=None, image=None,
                 widget_pos="topleft"):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.prompt = prompt
        self.text = starting_text

        self.over_font = font
        self.over_image = image

        self.size = size

        self.focused = False

        self.__mouse_hold_me = False
        self.__text_pos = len(self.text)

        self.make_image()

    def make_image(self):
        font = None
        if self.over_font:
            font = self.over_font
        elif self.theme:
            font = self.theme.font
            font["entry-text-color"] = self.theme.input["entry-text-color"]

        image = None
        if self.over_image:
            image = self.over_image
        elif self.theme:
            image = self.theme.input["border"]

        if font:
            f = pygame.font.Font(font["font"], font["size"])
            width = f.size(self.prompt + ": " + "0" * (self.size + 1))[0]
            height = f.get_linesize()

            tex_surface = f.render(self.prompt + ": " + self.text, font["aa"],
                                   self.theme.input["entry-text-color"])

            if image and not image == "noimage":
                self.__surf_size = image.get_width() / 3, image.get_height() / 3
                surface = resize_image(image, (width + self.__surf_size[0] * 2,
                                               height + self.__surf_size[1] * 2))
            else:
                surface = pygame.Surface((width, height)).convert_alpha()
                surface.fill((0,0,0,0))
        else:
            NoFontError = "No font loaded for TextInputBox widget"
            raise NoFontError

        self.surface = surface
        self.tex_surface = tex_surface
        self.rect = self.surface.get_rect()
        setattr(self.rect, self.widget_pos, self.pos)
        self.parent.dirty = True

    def make_text(self):
        font = None
        if self.over_font:
            font = self.over_font
        elif self.theme:
            font = self.theme.font
            font["entry-text-color"] = self.theme.input["entry-text-color"]

        f = pygame.font.Font(font["font"], font["size"])

        if self.focused:
            t = f.size(self.prompt + ": ")[0]
            miw, height = f.size(self.text[0:self.__text_pos])
            maw = f.size(self.text[0:self.__text_pos+1])[0]

            self.tex_surface = f.render(self.prompt + ": " + self.text + " ",
                                        font["aa"],
                                   self.theme.input["entry-text-color"])
            r, g, b = self.theme.input["entry-text-color"]
            r = 255 - r
            g = 255 - g
            b = 255 - b
            rc = pygame.Rect((t + miw, 0), (maw - miw, height))
            pygame.draw.rect(self.tex_surface, (r, g, b), rc, 1)
            
        else:
            self.tex_surface = f.render(self.prompt + ": " + self.text, font["aa"],
                                   self.theme.input["entry-text-color"])
        self.parent.dirty = True
        return None

    def render(self, surface, offset=(0, 0)):
        pos = self.rect.left + offset[0], self.rect.top + offset[1]
        surface.blit(self.surface, pos)
        surface.blit(self.tex_surface, (pos[0] + self.__surf_size[0],
                                        pos[1] + self.__surf_size[1]))

    def event(self, event, offset=(0, 0)):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] + offset[0], mpos[1] + offset[1]
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mpos):
                self.__mouse_hold_me = True
                self.parent.move_to_top(self)
                return None
            else:
                self.__mouse_hold_me = False
                self.focused = False
                return event
        if event.type == MOUSEBUTTONUP:
            if self.rect.collidepoint(mpos):
                self.parent.move_to_top(self)
                if self.__mouse_hold_me:
                    self.focused = True
                self.__mouse_hold_me = False
                self.make_text()
                return None
            else:
                self.focused = False
                self.__mouse_hold_me = False
                self.make_text()
                return event

        if event.type == KEYDOWN:
            if self.focused:
                if event.key == K_BACKSPACE:
                    if not self.__text_pos == 0:
                        self.text = self.text[0:self.__text_pos-1] + self.text[self.__text_pos::]
                        self.__text_pos -= 1
                        self.make_text()
                elif event.key == K_DELETE:
                    if not self.__text_pos == len(self.text):
                        self.text = self.text[0:self.__text_pos] + self.text[self.__text_pos+1::]
                        self.make_text()
                elif event.key == K_HOME:
                    if not self.__text_pos == 0:
                        self.__text_pos = 0
                        self.make_text()
                elif event.key == K_END:
                    if not self.__text_pos == len(self.text):
                        self.__text_pos = len(self.text)
                        self.make_text
                elif event.key == K_LEFT:
                    if self.__text_pos > 0:
                        self.__text_pos -= 1
                        self.make_text()
                elif event.key == K_RIGHT:
                    if self.__text_pos < len(self.text):
                        self.__text_pos += 1
                        self.make_text()
                elif event.key == K_RETURN:
                    a = Event(TextInputBox, self.name, GUI_EVENT_INPUT)
                    a.string = self.text
                    self.text = ""
                    self.__text_pos = 0
                    self.make_text()
                    return a
                else:
                    if len(self.text) <= self.size:
                        char = event.unicode.encode('latin-1')
                        self.text = self.text[0:self.__text_pos] + char +\
                                    self.text[self.__text_pos::]
                        self.__text_pos += 1
                        self.make_text()
                    return None
                return None
            return event
        return event


class WindowBar(Button):
    def __init__(self, parent, pos, name,
                 widget_pos="topleft",
                 width=None, caption="",
                 font=None, images=None):

        if not images:
            images = [parent.theme.window_bar["default"],
                      parent.theme.window_bar["hover"],
                      parent.theme.window_bar["click"]]
        if not font:
            font = copy.copy(parent.theme.font)
            font["text-color"] = parent.theme.window_bar["text-color"]
        
        Button.__init__(self, parent, pos, name, caption,
                        font, images, widget_pos)

        self.__mouse_hold_me=False

        self.child = None

        self.over_width = width
        self.make_image()

    def moveup(self):
        if self.child:
            self.child.parent.move_to_top(self.child)
        self.parent.move_to_top(self)

    def event(self, event, offset=(0, 0)):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] - offset[0], mpos[1] - offset[1]
        if self.rect.collidepoint(mpos):
            if self.__mouse_hold_me:
                self.change_image(self.click)
            else:
                self.change_image(self.hover)
        else:
            self.change_image(self.regular)

        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mpos):
                self.change_image(self.click)
                self.__mouse_hold_me = True
                self.moveup()
                return None
            return event
        if event.type == MOUSEBUTTONUP:
            if self.__mouse_hold_me:
                self.__mouse_hold_me = False
                if self.rect.collidepoint(mpos):
                    self.change_image(self.regular)
                    self.moveup()
                    return None
                return None
            return event
        if event.type == MOUSEMOTION:
            if self.__mouse_hold_me:
                self.move(event.rel)
                if self.child:
                    self.child.move(event.rel)
        return event

    def attach(self, other):
        self.child = other


#Defines
GUI_EVENT = "This is a string so we don't confuse Pygame ;)"
GUI_EVENT_CLICK = 0
GUI_EVENT_INPUT = 1

class Event(object):
    def __init__(self, widg=Widget, name="Name",
                 action=GUI_EVENT_CLICK):
        self.type = GUI_EVENT

        self.widget = widg
        self.name = name

        self.action = action
