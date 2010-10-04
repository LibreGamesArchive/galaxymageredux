import engine

test = engine.Display()
test.setup(screen_size=(800,600))
test.build()

print test
print test.screen

test.destroy()
