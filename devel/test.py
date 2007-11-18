
import ui_engine
from ui_engine import *

def main():
    init()
    set_3d()

    c = Camera()
    c.move((0, 0, -5))

    image = load_image("tile_example.png")

    tile = Tile(image, image, image, image, image,
                (0, 0, 0),
                (5, 8, 2, 4),
                (1, 1, 1, 1))

    while 1:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                return

        clear_screen()
        tile.render()
        pygame.display.flip()

main()
