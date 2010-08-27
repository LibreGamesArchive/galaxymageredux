
mapd = gfx_engine.mapd

mapd.tiles = {1:'floor-dungeon-blue.png'}

mapd.map_grid = [[1,1,1,1,1],
                 [1,1,1,1,1],
                 [1,1,1,1,1]]

mapd.engine.camera.set_pos(2.5, 1.5)

#no name is needed, but Bob is there so I can identify entity later!
mapd.make_entity('test-ent1.gif', (2.5,1.5), 'Bob')

for i in mapd.get_entities_on_tile(2,1):
    print [i.name]
