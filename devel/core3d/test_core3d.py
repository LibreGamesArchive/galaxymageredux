import core3d
from core3d import *


def main():
    core3d.init()

    camera = core3d.Camera(position=(0, 0, 0),
                           angle=[-45, 0, 135],
                           distance=(0, 0, 15))
    l1 = core3d.Light()

    a = pygame.image.load("testc3d1.png")
    b = pygame.image.load("testc3d2.png")

    a = core3d.DynamicImage(a, camera)
    b = core3d.FlatImage(b, camera)

    b_pos = [0, 0, 0.5] #moved z-coord out to be "above" tiles

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return None

            if event.type == KEYDOWN:
                angle = camera.angle[2]
                if angle == 0:
                    angle = 1

                if event.key == K_LEFT:
                    b_pos[0] -= 1
                if event.key == K_RIGHT:
                    b_pos[0] += 1

                if event.key == K_UP:
                    b_pos[1] += 1
                if event.key == K_DOWN:
                    b_pos[1] -= 1

                # Rotate camera, ultimately orbiting unit
                if event.key == K_LEFTBRACKET:
                    camera.angle[2] -= 45
                if event.key == K_RIGHTBRACKET:
                    camera.angle[2] += 45

        core3d.clear_screen()

        camera.update()

        for x in xrange(10):
            for y in xrange(10):
                a.render((x,y,0))

        b.render(b_pos)
        camera.position = (-b_pos[0] * 2, -b_pos[1] * 2, 0)

        pygame.display.flip()

main()
