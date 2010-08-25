tiles = {1:'test-terrain1.png',
         2:'test-terrain2.png'}
map_grid = [[1,1,1,1,1],
            [1,2,2,2,1],
            [1,1,1,1,1]]
engine.set_camera_pos(2.5, 1.5)

#no name is needed, but Bob is there so I can identify entity later!
engine.make_entity('test-ent1.gif', (2.5,1.5), 'Bob')

for i in engine.get_entities_on_tile(2,1):
    print [i.name]
