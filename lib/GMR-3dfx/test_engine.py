import engine
from engine import *

test = engine.Display()
test.setup(screen_size=(800,600))
test.build()
test.clear()

t = engine.TextureHandler()
t.load_dir("")

i = engine.Image2D(t.get_texture('floor-dungeon-blue.png'))
i2 = i.copy((16,0,48,32))
i3 = engine.load_image2D('unit-test-archer.gif')
i4 = i3.copy((16, 14, 55, 64))

test.set_2d()
test.set_lighting(False)

test.screen.push_clip2d((60,60,160,100))
i.render((50,50))
i2.render((112,50))
i3.render((112,50))
i4.render((206, 50))
test.screen.pop_clip()

f = engine.Font2D()
i5 = Image2D(f.tex)
glScalef(2,2,2)
i5.render((0,0))

test.refresh()

##test.destroy()
