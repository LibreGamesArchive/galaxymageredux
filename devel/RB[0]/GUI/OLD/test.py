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

        self.surf_data = pygame.image.tostring(self.surf, "RGBA", 1)
        self.dirty = False

    def check_events(self, events):
        return self.gui.check_inputs(events)

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
        self.dirty = True
        self.surf.fill((0,0,0,0))
        for img in rects:
            self.surf.blit(img.image, img.rect)

    def render(self):
        image = self.surf
        if self.dirty:
            data = self.surf_data = pygame.image.tostring(image, "RGBA", 1)
        else:
            data = self.surf_data
        glDrawPixels(self.size[0], self.size[1], GL_RGBA, GL_UNSIGNED_BYTE, data)

cc = pygame.time.Clock()
def main():
    screen_size = (640, 480)
    core.init(screen_size)
    core.set3d(screen_size)

    glClearColor(1, 1, 1, 1)

    core.clear_screen()

    gui_screen = GuiScreen(screen_size)

    while 1:
        cc.tick(9999)
        for event in gui_screen.check_events(pygame.event.get()):
            if event.type == QUIT:
                print cc.get_fps()
                pygame.quit()
                return

        core.clear_screen()

        gui_screen.render()

        pygame.display.flip()


main()
        
