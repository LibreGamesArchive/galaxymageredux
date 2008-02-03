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

    def force_update(self):
        self.dirty = True

    def add_widget(self, widg):
        self.widgets.insert(0, widg)
        self.dirty = True
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
                    self.dirty = True
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
                 widget_pos="topleft", theme=None):
        self.name = name
        self.parent = parent
        self.parent.add_widget(self)

        self.theme = copy.copy(theme)
        if not self.theme:
            if self.parent:
                self.theme = copy.copy(self.parent.theme)

        x, y = pos
        if x == -1:
            x = int(self.parent.surface.get_width() / 2)
        if y == -1:
            y = int(self.parent.surface.get_height() / 2)
        self.pos = (x, y)

        self.widget_pos = widget_pos

        self.rect = pygame.Rect(0, 0, 1, 1)
        self.move()

    def render(self, surface, offset=(0, 0)):
        pass

    def force_update(self):
        self.parent.force_update()

    def event(self, event, offset=(0, 0)):
        return event

    def move(self, off=(0,0)):
        x, y = self.pos
        x += off[0]
        y += off[1]

        self.pos = (x, y)
        setattr(self.rect, self.widget_pos, self.pos)
        self.force_update()
        return None

    def combine_images(self, images):
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

    def not_active(self):
        pass


class Label(Widget):
    def __init__(self, parent, pos, name, text,
                 widget_pos="topleft", theme=None,
                 icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos, theme)

        self.text = text

        self.over_width = None

        self.icon = icon
        if self.icon:
            self.icon = pygame.image.load(os.path.join(self.theme.theme, self.icon)).convert_alpha()

        self.make_image()

    def make_image(self):
        if self.theme and self.theme.font["font"]:
            font = pygame.font.Font(self.theme.font["font"],
                                    self.theme.font["size"])
            tex = font.render(self.text, self.theme.font["aa"],
                              self.theme.label["text-color"])
            if self.icon:
                tex = self.combine_images([self.icon, tex])
            image = self.theme.label["image"]
            if image=="noimage":
                self.comp_image = tex
            elif image:
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
        self.move()
        return None

    def render(self, surface, offset=(0, 0)):
        pos = self.rect.left + offset[0], self.rect.top + offset[1]
        surface.blit(self.comp_image, pos)
        return None

class Button(Widget):
    def __init__(self, parent, pos, name, text,
                 widget_pos="topleft",
                 theme=None, icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos, theme)

        self.text = text

        self.over_width = None

        self.icon = icon
        if self.icon:
            self.icon = pygame.image.load(os.path.join(self.theme.theme, self.icon)).convert_alpha()

        self.make_image()

        self.__mouse_hold_me = False

    def not_active(self):
        self.change_image(self.regular)

    def make_image(self):
        if self.theme and self.theme.font["font"]:
            font = pygame.font.Font(self.theme.font["font"],
                                    self.theme.font["size"])
            tex = font.render(self.text, self.theme.font["aa"],
                              self.theme.button["text-color"])
            if self.icon:
                tex = self.combine_images([self.icon, tex])

            #default button!
            image = self.theme.button["default"]
            if image=="noimage":
                self.regular = tex
            elif image:
                bsize = (image.get_width() / 3,
                         image.get_height() / 3)
                rect = tex.get_rect()
                rect.width += bsize[0] * 2
                rect.height += bsize[1] * 2
                if self.over_width:
                    rect.width = self.over_width
                new = resize_image(image, rect.size)
                new.blit(tex, bsize)
                self.regular = new
            else:
                self.regular = tex

            #hover button!
            image = self.theme.button["hover"]
            if image=="noimage":
                self.hover = tex
            elif image:
                bsize = (image.get_width() / 3,
                         image.get_height() / 3)
                rect = tex.get_rect()
                rect.width += bsize[0] * 2
                rect.height += bsize[1] * 2
                if self.over_width:
                    rect.width = self.over_width
                new = resize_image(image, rect.size)
                new.blit(tex, bsize)
                self.hover = new
            else:
                self.hover = tex

            #click button!
            image = self.theme.button["click"]
            if image=="noimage":
                self.click = tex
            elif image:
                bsize = (image.get_width() / 3,
                         image.get_height() / 3)
                rect = tex.get_rect()
                rect.width += bsize[0] * 2
                rect.height += bsize[1] * 2
                if self.over_width:
                    rect.width = self.over_width
                new = resize_image(image, rect.size)
                new.blit(tex, bsize)
                self.click = new
            else:
                self.click = tex
        else:
            if self.icon:
                self.regular = self.hover = self.click = self.icon
            else:
                self.regular = self.hover = self.click = pygame.Surface((1, 1))

        self.image = self.regular
        self.rect = self.image.get_rect()
        self.move()
        return None

    def render(self, surface, offset=(0,0)):
        pos = self.rect.left + offset[0], self.rect.top + offset[0]
        surface.blit(self.image, pos)
        return None

    def change_image(self, new):
        if not self.image == new:
            self.image = new
            self.force_update()
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
                 widget_pos="topleft",
                 theme=None,
                 icons={"None":None}):
        Widget.__init__(self, parent, pos, name, widget_pos, theme)

        self.button_list = buttons
        self.icons = icons

        self.surface = pygame.Surface((1, 1))
        self.draw_area = pygame.Surface((1, 1))

        self.make_image()

    def make_image(self):
        buttons = []
        self.theme.button["default"] = self.theme.menu["entry-default"]
        self.theme.button["hover"] = self.theme.menu["entry-hover"]
        self.theme.button["click"] = self.theme.menu["entry-click"]
        self.theme.button["text-color"] = self.theme.menu["entry-text-color"]
        height = 0
        width = 0
        for i in self.button_list:
            try:
                x = self.icons[i]
            except:
                x = None
            new = Button(self, (0, height), i, i, icon=x)
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
        self.move()
        self.buttons = buttons

    def add_widget(self, *other):
        pass

    def move_to_top(self, other):
        pass

    def not_active(self):
        for i in self.buttons:
            i.not_active()

    def render(self, surface, offset=(0, 0)):
        self.draw_area.blit(self.old_draw_area, (0, 0))
        for i in self.buttons:
            i.render(self.draw_area, offset)
        surface.blit(self.surface, self.rect)
        return None

    def event(self, event, offset=(0, 0)):
        offset = offset[0] + self.rect.left, offset[1] + self.rect.top
        for i in self.buttons:
            x = i.event(event, offset)
            if not x == event:
                self.force_update()
                if x:
                    x.widget = MenuList
                    x.entry = x.name
                    x.name = self.name
                event = x
                break
        return event           

class Menu(Widget):
    def __init__(self, parent, pos, name, text,
                 buttons=["None"], icons={"None":None},
                 widget_pos="topleft",
                 icon=None, theme=None):
        Widget.__init__(self, parent, pos, name, widget_pos, theme)

        self.text = text
        self.buttons = buttons
        self.icons = icons
        self.icon = icon

        self.make_image()

        self.widget_vis = False

    def move_to_top(self, other):
        self.parent.move_to_top(self)

    def not_active(self):
        self.window_vis = False
        self.other.not_active()
        self.button.not_active()

    def make_image(self):
        self.button = Button(self, self.pos, self.name, self.text,
                             self.widget_pos, icon=self.icon)

        self.other = MenuList(self, (self.pos[0], self.pos[1] + self.button.rect.height),
                              "", self.buttons, self.widget_pos, icons=self.icons)

        self.move()

    def add_widget(self, *other):
        pass

    def event(self, event, offset=(0, 0)):
        x = self.button.event(event, offset)
        if not x == event:
            self.force_update()
            if x:
                if x.type == GUI_EVENT:
                    if x.widget == Button:
                        if x.action == GUI_EVENT_CLICK:
                            self.widget_vis = not self.widget_vis
            return x
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
                                self.force_update()
                            else:
                                event = None

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
                 widget_pos="topleft", theme=None):
        Widget.__init__(self, parent, pos, name, widget_pos, theme)

        self.prompt = prompt
        self.text = starting_text

        self.size = size

        self.focused = False

        self.__mouse_hold_me = False
        self.__text_pos = len(self.text)

        self.make_image()

    def not_active(self):
        if self.focused:
            self.force_update()
        self.focused = False
        self.make_text()

    def make_image(self):

        if self.theme:
            font = self.theme.font
            f = pygame.font.Font(font["font"], font["size"])
            width = f.size(self.prompt + ": " + "0" * (self.size + 1))[0]
            height = f.get_linesize()

            tex_surface = f.render(self.prompt + ": " + self.text, font["aa"],
                                   self.theme.input["entry-text-color"])

            image = self.theme.input["border"]

            if image and not image == "noimage":
                self.__surf_size = image.get_width() / 3, image.get_height() / 3
                surface = resize_image(image, (width + self.__surf_size[0] * 2,
                                               height + self.__surf_size[1] * 2))
            else:
                surface = pygame.Surface((width, height)).convert_alpha()
                surface.fill((0,0,0,0))

        self.surface = surface
        self.tex_surface = tex_surface
        self.rect = self.surface.get_rect()
        self.move()

    def make_text(self):

        if self.theme:
            font = self.theme.font
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
            self.force_update()
            return None
        return None

    def render(self, surface, offset=(0, 0)):
        pos = self.rect.left - offset[0], self.rect.top - offset[1]
        surface.blit(self.surface, pos)
        surface.blit(self.tex_surface, (pos[0] + self.__surf_size[0],
                                        pos[1] + self.__surf_size[1]))
        return None

    def event(self, event, offset=(0, 0)):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] - offset[0], mpos[1] - offset[1]
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mpos):
                self.__mouse_hold_me = True
                self.parent.move_to_top(self)
                self.force_update()
                return None
            else:
                self.__mouse_hold_me = False
                if self.focused:
                    self.force_update()
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
                if self.focused:
                    self.force_update()
                self.focused = False
                self.__mouse_hold_me = False
                self.make_text()
                return event

        if event.type == KEYDOWN:
            if self.focused:
                self.force_update()
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


class WindowBar(object):
    def __init__(self, parent, pos, width=None,
                 caption="", icon=None):

        self.parent = parent
        self.theme = copy.copy(self.parent.theme)
        self.theme.button = self.theme.window_bar

        self.bar = Button(self, pos, "", caption, "midbottom", icon=icon)
        self.bar.over_width = width
        self.bar.make_image()

        self.__mouse_hold_me=False

        self.minimized = False

        self.min_button = Button(self, self.bar.rect.midright, "", "_",
                                 "midright")

    def add_widget(self, other):
        pass

    def move_to_top(self, other):
        self.moveup()

    def moveup(self):
        self.parent.force_update()

    def force_update(self):
        self.parent.force_update()

    def event(self, event, offset=(0, 0)):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] - offset[0], mpos[1] - offset[1]

        if self.bar.rect.collidepoint(mpos):
            if self.__mouse_hold_me:
                self.bar.change_image(self.bar.click)
            else:
                self.bar.change_image(self.bar.hover)
        else:
            self.bar.change_image(self.bar.regular)

        e = self.min_button.event(event, offset)
        if not e == event:
            self.force_update()
            if e:
                self.moveup()
                if e.type == GUI_EVENT:
                    self.minimized = not self.minimized
                    return None
            return e

        else:
            if event.type == MOUSEBUTTONDOWN:
                if self.bar.rect.collidepoint(mpos):
                    self.bar.change_image(self.bar.click)
                    self.__mouse_hold_me = True
                    self.moveup()
                    return None
                return event
            if event.type == MOUSEBUTTONUP:
                if self.__mouse_hold_me:
                    self.__mouse_hold_me = False
                    if self.bar.rect.collidepoint(mpos):
                        self.bar.change_image(self.bar.regular)
                        self.moveup()
                        return None
                    return None
                return event
            if event.type == MOUSEMOTION:
                if self.__mouse_hold_me:
                    self.bar.move(event.rel)
                    self.min_button.move(event.rel)
                    self.parent.move(event.rel)
        return event

    def render(self, surface, offset=(0, 0)):
        self.bar.render(surface, offset)
        self.min_button.render(surface, offset)
        return None

class Window(Widget):
    def __init__(self, parent, pos, name, widget_pos="topleft",
                 size=(50, 50), caption="",
                 icon=None):
        Widget.__init__(self, parent, pos, name, widget_pos)

        self.size = size

        self.icon = icon

        self.caption = caption

        self.widgets = []

        self.make_image()

    def not_active(self):
        for i in self.widgets:
            i.not_active()
        return None

    def make_image(self):
        if self.theme:
            image = self.theme.window["border"]

            if image and not image == "noimage":
                w, h = image.get_size()
                new = resize_image(image, (self.size[0] + w * 2,
                                           self.size[1] + h * 2))

                self.border = new
                self.surface = self.border.subsurface((w, h), self.size)
                self.border_offset = (w, h + 1)
                self.__old_draw_area = self.surface.copy()
                self.rect = self.border.get_rect()
                setattr(self.rect, self.widget_pos, self.pos)
            else:
                self.border_offset = (0, 0)
                self.border = None
                self.surface = pygame.Surface(self.size).convert()
                self.__old_draw_area = self.surface.copy()
                self.rect = self.surface.get_rect()
                setattr(self.rect, self.widget_pos, self.pos)
        else:
            self.border_offset = (0, 0)
            self.border = None
            self.surface = pygame.Surface(self.size).convert()
            self.__old_draw_area = self.surface.copy()
            self.rect = self.surface.get_rect()
            setattr(self.rect, self.widget_pos, self.pos)

        self.drag_bar = WindowBar(self, self.rect.midtop,
                                  self.rect.width, self.caption,
                                  self.icon)
        self.force_update()

    def event(self, event, offset=(0, 0)):
        e = self.drag_bar.event(event, offset)
        if not e == event:
            return e
        else:
            o = (self.rect.left - offset[0] + self.border_offset[0],
                 self.rect.top - offset[1] + self.border_offset[1])
            mpos = pygame.mouse.get_pos()
            mpos = mpos[0] - o[0], mpos[1] - o[1]
            if self.drag_bar.minimized:
                self.not_active()
                return event
            for i in self.widgets:
                if not i == self.drag_bar:
                    e = i.event(event, o)
                    if not e == event:
                        for x in self.widgets:
                            if not x == i:
                                x.not_active()
                        self.parent.move_to_top(self)
                        if e and e.type == GUI_EVENT:
                            e.subwidget = e.widget
                            e.widget = Window
                        return e
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                m = pygame.mouse.get_pos()
                m = m[0] - offset[0], m[1] - offset[1]
                if self.rect.collidepoint(m):
                    self.parent.move_to_top(self)
                    return None
                self.not_active()
            return event
        return event

    def move_to_top(self, other):
        i = self.widgets.index(other)
        self.widgets.insert(0, self.widgets.pop(i))
        self.force_update()
        return None

    def add_widget(self, widg):
        self.widgets.insert(0, widg)
        return None

    def remove_widget(self, name):
        for i in self.widgets:
            if i.name == name:
                self.widgets.remove(i)
                break
        return None

    def render(self, surface, offset=(0, 0)):
        self.surface.blit(self.__old_draw_area, (0, 0))
        self.widgets.reverse()
        for i in self.widgets:
            i.render(self.surface)
        self.widgets.reverse()

        self.drag_bar.render(surface, offset)
        if not self.drag_bar.minimized:
            pos = offset[0] + self.rect.left, offset[1] + self.rect.top
            surface.blit(self.border, pos)
        return None
            


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
