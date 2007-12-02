
import ui_engine
from ui_engine import *
import map_loader

def main():
    init()
    set_3d()

    c = Camera()
    c.move((0, 0, 0))
    c.distance = 15
    c.rotate((45, 45, 0))

    l = Light((0,0,-15),
              (1,1,1,1),
              (1,1,1,1),
              (1,1,1,1))

    images, terrains, tiles = map_loader.load_map("test_map.py")

    s = ui_engine.Sprite(pygame.image.load("unit_example.png"), c)
    s_pos = tiles[0].get_top()

    click = False

    while 1:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return

            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    c.rotate((0, 90, 0))
                if event.key==K_RIGHT:
                    c.rotate((0, -90, 0))

            if event.type == MOUSEBUTTONDOWN:
                click = True

        c.update()
        pick = select_tiles(tiles, pygame.mouse.get_pos())
        if pick:
            pick.old_color = pick.color
            pick.set_color((1, 0, 1, 1))
            if click:
                click = False
                s_pos = pick.get_top()
                print s_pos
        
        c.update()
        for i in tiles:
            i.render()
        s.render(s_pos)
        pygame.display.flip()
        
        if pick:
            pick.set_color(pick.old_color)
            del pick.old_color

main()
