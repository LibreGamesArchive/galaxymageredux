import core3d
from core3d import *


def main():
    core3d.init()

    camera = core3d.Camera(position=(-10, 0, 0),
                           angle=(-45, 0, 45),
                           distance=(0, 0, 15))
    l1 = core3d.Light()

    a = pygame.image.load("testc3d1.png")
    b = pygame.image.load("testc3d2.png")

    a = core3d.DynamicImage(a, camera)
    b = core3d.FlatImage(b, camera)

    ##b_pos = [0, 5, 0.5]#moved out to be "above" tiles
    b_pos = [0, 0, 0.5] #moved z-coord out to be "above" tiles

    while 1:
        #camera.update()
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return None

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    b_pos[0] -= 1
                if event.key == K_RIGHT:
                    b_pos[0] += 1

                if event.key == K_UP:
                    b_pos[1] += 1
                if event.key == K_DOWN:
                    b_pos[1] -= 1

        core3d.clear_screen()

        camera.update() ##

        for x in xrange(10):
            for y in xrange(10):
                a.render((x,y,0))

        b.render(b_pos)
        camera.position = (-b_pos[0] * 2, -b_pos[1] * 2, 0) ##

        pygame.display.flip()

main()
