import core
from load_gmm import *

print """usage:
press "a" to switch from rotation to movement animations.
hit QUIT to quit"""

def main():
    core.init()
    core.set3d()

    c = core.Camera()
    c.distance = 100

    l = core.Light((0,0,-15),
              (1,1,1,1),
              (1,1,1,1),
              (1,1,1,1))

    a = Mesh(*parse_file("test.gmm"))
    a.animation_action = "rotate"

    clock = pygame.time.Clock()

    while 1:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_a:
                    a.reset_animation()
                    if a.animation_action == "rotate":
                        a.animation_action = "move"
                    else:
                        a.animation_action = "rotate"
        core.clear_screen()
        c.update()

        a.render((0, 0, 25))
        a.update()
        pygame.display.flip()
main()
