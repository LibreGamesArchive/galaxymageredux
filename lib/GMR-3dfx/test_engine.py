import engine, event
from engine import *

def main():
    test = engine.Display()
    test.setup(screen_size=(800,600))
    test.build()

    t = engine.TextureHandler()
    t.load_dir("")

    i = engine.Image2D(t.get_texture('floor-dungeon-blue.png'))
    i2 = i.copy((16,0,48,32))
    i3 = engine.load_image2D('unit-test-archer.gif')
    i4 = i3.copy((16, 14, 55, 64))

    test.set_2d()
    test.set_lighting(False)

    event_handler = event.Handler()

    f = engine.Font2D()

    while 1:
        event_handler.update()
        if event_handler.quit:
            test.destroy()
            return None

        test.clear()

        test.screen.push_clip((60,60,160,100))
        i.render((50,50))
        i2.render((112,50))
        i3.render((112,50))
        i4.render((206, 50))
        test.screen.pop_clip()

        f.render("Hello World", (10,10), (1,1,0,1), 32)

        engine.draw_rect2d((50,200,100,100))

        engine.draw_lines2d([((0,0), (500,500)),
                             ((500,0), (0,500))],
                            (1,0,0,.5))

        test.refresh()

main()
