# LICENSE:
#
# Copyright (c) 2007-2008 A. Joseph Hager and Redux contributors.
#
# Redux is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License, as published by the
# Free Software Foundation.
# 
# Redux is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along
# with Redux; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


from pyglet import resource

from codecs import md2


def load(model, image):
    m = md2.MD2Model(model, image)
    f = []
    for frame in m.frames:
        f.append(Frame(frame.varray, m.animationSpeed))
    a = Animation(f, m.frames[0].tarray, image)
    return a


class Frame(object):
    def __init__(self, vertices, delay):
        self.vertices = vertices
        self.delay = delay


class Animation(object):
    def __init__(self, frames, tex_coords, image):
        self.frames = frames
        self.tex_coords = tex_coords
        self.texture = resource.texture(image)
