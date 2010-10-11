import engine
from engine import *

test = engine.Display()
test.setup(screen_size=(800,600))
test.build()
test.clear()

running = True
while running:
    new = load_texture('unit-test-archer.gif')
    for event in pygame.event.get():
        if event.type == QUIT:
            test.destroy()
            running = False
