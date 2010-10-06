import engine

test = engine.Display()
test.setup(screen_size=(800,600))
test.build()

print test
print test.screen

##t = engine.TextureHandler()
##t.load_dir("")
##
##i = engine.Image2D(t.get_texture('floor-dungeon-blue.png'))
t = engine.BaseTexture()
t._from_file('floor-dungeon-blue.png')
i = engine.Image2D(t)
test.set_2d()
test.set_lighting(False)
i.render((50,50))

test.refresh()

##test.destroy()
