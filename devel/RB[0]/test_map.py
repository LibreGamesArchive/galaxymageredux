image("grass1","tile_example.png")


terrain_type(name="grass",
             image_top="grass1",
             image_sides=("grass1", "grass1",
                          "grass1", "grass1"),
             color=(0,1,0,1), color_deviation=(0, 0.1, 0, 0),
             hitpoints=50, armor={})


map_tile(x=0, y=0, bottom=0, height=5,
         terrain="grass",
         tl_add=0, tr_add=0, bl_add=0, br_add=0)
map_tile(x=1, y=0, bottom=0, height=4,
         terrain="grass",
         tl_add=0, tr_add=0, bl_add=0, br_add=0)

map_tile(x=0, y=1, bottom=0, height=4,
         terrain="grass",
         tl_add=0, tr_add=0, bl_add=0, br_add=0)
map_tile(x=1, y=1, bottom=0, height=3,
         terrain="grass",
         tl_add=0, tr_add=0, bl_add=0, br_add=0)
