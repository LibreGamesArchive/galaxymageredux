
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
                (0.75, 1, 0.75, 1))

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

        clear_screen()
        c.update()
        glRotatef(rotation, 0, 1, 0)
        tile.render()
        pygame.display.flip()

main()
