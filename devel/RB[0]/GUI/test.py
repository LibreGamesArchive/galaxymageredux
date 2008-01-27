import os

import core
from core import *

import GUI

class GuiScreen(object):
    def __init__(self, size):
        self.size = size
        self.surf = pygame.Surface(size, SRCALPHA).convert_alpha()

        self.gl_texture = glGenTextures(1)

        self.gui = GUI.PYTHON_GUI(self.redraw_routine)
        self.make_scene()

    def check_events(self, events):
        a = self.gui.check_inputs(events)

    def render(self):
        image = self.surf

        x, y = image.get_size()
        nx, ny = 16, 16
        while nx < x:
            nx *= 2
        while ny < y:
            ny *= 2

        image = pygame.transform.scale(image, (nx, ny))
        data = pygame.image.tostring(image, "RGBA", 1)

        glBindTexture(GL_TEXTURE_2D, self.gl_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        core.set2d(self.size)

        core.clear_screen()

        glBindTexture(GL_TEXTURE_2D, self.gl_texture)

        glBegin(GL_QUADS)
        glColor4f(1, 1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0); glVertex3f(self.size[0], 0, 0)
        glTexCoord2f(1, 1); glVertex3f(self.size[0], self.size[1], 0)
        glTexCoord2f(0, 1); glVertex3f(0, self.size[1], 0)
        glEnd()

        core.set3d(self.size)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

    def make_scene(self):
        self.gui.lock_updates()

        window=GUI.Window(-1,-1,300,160,"Test",True)

        buttons=[]

        def button_clicked(widget, x, y):
            print widget.text
            return True

        buttons.append(GUI.button_details("OK",None,button_clicked))
        buttons.append(GUI.button_details("Cancel",None,button_clicked))

        window.build_button_area(buttons,False)

        self.gui.add_window(window)

        my_label=GUI.BuildLabel("This is a label")

        my_button=GUI.Button(0,0,"Xing")
        my_button.callbacks.mouse_lclk=button_clicked

        my_label.rect.x=8
        my_button.rect.x=my_label.rect.w+16
        my_button.rect.y=8

        width=my_label.rect.w+my_button.rect.w+24
        height=my_button.rect.h+16
        my_label.rect.y=(height-my_label.rect.h)/2
        window=GUI.Window(16,16,width,height,"Label",True)

        window.add_item(my_label)
        window.add_item(my_button)

        self.gui.add_window(window)

        img=GUI.BuildImage(pygame.image.load(
                os.path.normpath("./gfx/test.png")).convert())

        window=GUI.Window(120,120,img.rect.w,img.rect.h,"Image",True)
        window.add_item(img)
        self.gui.add_window(window)

        chk=GUI.CheckBox(self.gui.update_screen,40,12,True)
        window=GUI.Window(300,100,chk.rect.w+80,chk.rect.h+24,"CheckBox",True)
        window.add_item(chk)
        self.gui.add_window(window)

        slider=GUI.Slider(self.gui.update_screen,16,16,140,1,140,70)
        window=GUI.Window(400,75,172,slider.rect.y+32,"Slider",True)
        window.add_item(slider)
        self.gui.add_window(window)

        self.gui.unlock_updates()

    def redraw_routine(self, rects):
        self.surf.fill((0,0,0,0))
        for img in rects:
            self.surf.blit(img.image, img.rect)

        self.render()
        pygame.display.flip()

def main():
    screen_size = (640, 480)
    core.init(screen_size)
    core.set3d(screen_size)

    core.clear_screen()

    gui_screen = GuiScreen(screen_size)

    while 1:
        gui_screen.check_events(pygame.event.wait())

        glBegin(GL_QUADS)
        glColor4f(1, 0, 0, 1)
        glVertex3f(-1, 1, -10)
        glColor4f(0, 1, 0, 1)
        glVertex3f(1, 1, -10)
        glColor4f(0, 0, 1, 1)
        glVertex3f(1, -1, -10)
        glColor4f(1, 1, 1, 1)
        glVertex3f(-1, -1, -10)
        glEnd()
        pygame.display.flip()

##        core.clear_screen()
##        gui_screen.render()
##        pygame.display.flip()

main()
        
