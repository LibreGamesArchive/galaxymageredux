
import ui_engine
from ui_engine import *

def main():
    init()
    set_3d()

    c = Camera()
    c.move((0, 0, -5))

    image = load_image("tile_example.png")

    tile = Tile((image, image, image, image, image),
                (0, 0, 0),
                (5, 8, 2, 4),
                (1, 1, 0, 1))
    t2 = Tile((image, image, image, image, image),
                (0, 0, -2),
                (4, 2, 3, 4),
                (1, 1, 0, 1))

    rotation=0

    while 1:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return

            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    rotation+=25
                if event.key==K_RIGHT:
                    rotation-=25

        pick = select_tiles([tile, t2], pygame.mouse.get_pos())
        if pick:
            pick.color = (1, 0, 1, 1)
        
        clear_screen()
        c.update()
        glRotatef(rotation, 0, 1, 0)
        tile.render()
        t2.render()
        pygame.display.flip()
        
        if pick:
            pick.color = (1, 1, 0, 1)

main()
