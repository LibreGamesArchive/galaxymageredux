image("this_maps_grass1":"path_from_here/to_the_image.png")
#this will load an image named this_maps_grass1,
#and add it to the group of images from the main game assets

terrain_type(name="grass", images=("this_maps_grass1", "Grass1"),
             color=(0,1,0,1), color_deviation=(0, 0.1, 0, 0),
             hitpoints=50, armor={})
#this defines a new kind of terrain, which is added to a list of already defined terrains,
#or replaces said terrian with this one.

map_tile(x=0, y=0, bottom=0, height=5,
         terrain="grass",
         blockable=False,
         tl_add=0, tr_add=0, bl_add=0, br_add=0)
#this is a tile on the map.
#x and y are it's coordinates
#bottom is the bottom height it starts at
#height is how tall above bottom the tile starts at
#terrain is the name of the terrain type this tile is
#blockable determines whether units can move onto this tile or not
#tl/tr/bl/br_add define how much taller/shorter
#the corners of the tile are than there height
#you can modify this so all will follow a procedural approach, but then can be modified beyond this.

#The other idea is that the top of the tile is cut into 4 triangles.
#then the center vertex is always at the real height of the tile,
#but the corners can be any height and it will still look correct


#This approach means you could keep the logical data in here as well
#so you would define units, objects, etc. here.
