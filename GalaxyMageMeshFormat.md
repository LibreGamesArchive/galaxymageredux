# Introduction #

The GalaxyMage Mesh Format is a model format that is similar to OBJ.
It removes many of the features of OBJ that were not deemed necessary, combines everything in one file, and adds skeletal animations.


# Details #
DataTypes:
  * (string) - a group of characters "this is a string", one word, no quotes necessary
  * (int) - an integer - 12
  * (float) - a decimal number - 12.12, can also be an int

Details:
  * "ver" - what version of the format are we using
  * "#" - a comment, ignored by parser

  * "o" - creates and sets as current a specific object in the mesh
  * "v" - creates a vertex
  * "n" - creates a normal
  * "f" - creates a face

  * "mtl" - creates a specific material
  * "mc" - binds a color to the chosen mtl
  * "mt" - loads and binds a texture to the chosen mtl
  * "tc" - specifies a texture coordinate

  * "usemtl" - sets the current material

  * "b" - creates a bone used in animation, a bone is a line segment with a starting point and ending point
  * "cb" - connects two bones

  * "ani" - specifies and sets as current a specific animation action (sequence)
  * "ar" - adds a rotate action that lasts for a duration of frames to the current animation
  * "at" - adds a translate (move) action to the current animation

  * "lani"? - loads the animations from another file into this one
  * "lf"? - loads another mesh and merges it with this one

USAGE:
  * "ver" - ver (string)
  * "#" - #anything can go here :D

  * "o" - o (string|object name)
  * "v" - v (float) (float) (float)
  * "n" - n (float) (float) (float)
  * "f" - f (int|vertex)/(int|normal) or (int|vertex)/(int|normal)/(int|texture coordinate) - if current material has a texture - for each vertex on the face

  * "mtl" - mtl (string|material name)
  * "mc" - mc (string|material name) (float|r value) (float|g value) (float|b value) (float|alpha value)
  * "mt" - mt (string|material name) (string|file name)
  * "tc" - tc (float| -1 < value < 1) (float| -1 < value < 1)

  * "usemtl" - usemtl (string|material name)

  * "b" - b (string|object name) (float|start x coord) (float|start y coord) (float|start z coord) (float|end x coord) (float|end y coord) (float|end z coord)
  * "cb" - cb (string|object name) (string|object name) (int|0 if connecting to start of first object, 1 if end) (int|start or end)

  * "ani" - ani (string|animation name)
  * "ar" - ar (string|object name) (int|start frame) (int|end frame) (float|x amount) (float|y) (float|z)
  * "at" - at (string|object name) (int|start frame) (int|end frame) (float|x offset) (float|y) (float|z)

  * "lani" - lani (string|file name)
  * "lf" - lf (string|file name)

EXAMPLE:
```
  ver 0.1
  #this is a comment :D
  #this creates a simple square that is red
  #and another square that is textured
  #it also creates a bone for square, that is not connected to another
  #and a bone for square2 that is connected to square
  #and provides rotate and move animations

  mtl square
  mc square 1.0 0.0 0.0 1.0

  mtl square2
  mt square2 some_texture.png

  usemtl square
  o square
  v -1 -1 0
  v -1 1 0
  v 1 1 0
  v 1 -1 0
  n -0.57735027 -0.57735027 0.57735027
  n -0.57735027 0.57735027 0.57735027
  n 0.57735027 0.57735027 0.57735027
  n 0.57735027 -0.57735027 0.57735027
  f 1/1 4/4 3/3 2/2

  usemtl square2
  o square2
  v 1 -1 0
  v 1 1 0
  v 2 1 0
  v 2 -1 0
  n -0.57735027 -0.57735027 0.57735027
  n -0.57735027 0.57735027 0.57735027
  n 0.57735027 0.57735027 0.57735027
  n 0.57735027 -0.57735027 0.57735027
  f 5/5 8/8 7/7 6/6

  b square -1 0 0 1 0 0
  b square2 1 0 0 2 0 0
  #the following will connect square2 to square 1 at the end of square with the start of sqaure 2
  cb square square2 1 0

  ani rotate
  #will rotate square2 around square
  ar square2 0 9 0 0 90

  ani move
  #will move square and square2
  at square 0 9 9 0 0

  lani other_ani.gmma
  lf other_mesh.gmm
```