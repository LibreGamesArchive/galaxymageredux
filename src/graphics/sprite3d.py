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


import math

from pyglet.gl import *
from pyglet import clock
from pyglet import event
from pyglet import graphics

import model


class Sprite3dState(object):
    def __init__(self, texture, blend_src, blend_dest, parent=None):
        super(Sprite3dState, self).__init__(parent)
        self.texture = texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def set(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

        glPushMatrix()
        glTranslatef(self.position[0],self.position[1],self.position[2])
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(self.scale[0], self.scale[1], self.scale[2])

    def unset(self):
        glPopMatrix()
        glPopAttrib()
        glDisable(self.texture.target)

    def __eq__(self, other):
        # To make batches work I had to move position/scale/rotation
        # to Sprite3dState.  This worked well until I realized that
        # batching removes redundant states based on this equality
        # method.  The difference between a 2d sprite and a 3d sprite
        # is you can update the position/scale/rotation of a 2d sprite
        # efficiently and only when an attribute is modified.  With 3d
        # sprites (especially ones that animate) the vertices change
        # every time the animation updates, and there are thousands of
        # vertices instead of 4.
        return False
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))


class Sprite3d(event.EventDispatcher):
    _batch = None
    _animation = None
    _opacity = 255
    _vertex_list = None

    def __init__(self,
                 mdl, x=0, y=0, z=0,
                 blend_src=GL_SRC_ALPHA,
                 blend_dest=GL_ONE_MINUS_SRC_ALPHA,
                 batch=None,
                 parent_state=None):

        # Make sure parent_state is accompanied by a batch.
        if parent_state is not None and batch is None:
            raise ValueError('parent_state requires batch rendering')

        if batch is not None:
            self._batch = batch

        if isinstance(mdl, model.Animation):
           self._animation = mdl
           self._frame_index = 0
           self._next_dt = mdl.frames[0].delay
           clock.schedule_once(self._animate, self._next_dt)
        else:
            self._model = mdl

        self._tex_coords = mdl.tex_coords
        self._texture = mdl.texture
        self._state = Sprite3dState(self._texture,
                                    blend_src, blend_dest,
                                    parent_state)
        self.x = x
        self.y = y
        self.z = z

        self._create_vertex_list()

    def __del__(self):
        if self._vertex_list is not None:
            self._vertex_list.delete()

    def delete(self):
        '''Force immediate removal from video memory.

        This is often necessary when using batches, as the Python garbage
        collector will not necessarily call the finalizer as soon as the
        sprite is garbage.
        '''
        if self._animation:
            clock.unschedule(self._animate)
        self._vertex_list.delete()
        self._vertex_list = None

    def _animate(self, dt):
        self._frame_index +=1
        if self._frame_index >= len(self._animation.frames):
            self.dispatch_event('on_animation_end')
            self._frame_index = 0

        frame = self._animation.frames[self._frame_index]
        if frame.delay is not None:
            delay = frame.delay - (self._next_dt - dt)
            delay = min(max(0, delay), frame.delay)
            clock.schedule_once(self._animate, delay)
            self._next_dt = delay
        else:
            self.dispatch_event('on_animation_end')

        self._vertex_list.vertices[:] = frame.vertices

    # TODO set batch
    batch = property(lambda self: self._batch)

    def _set_parent_state(self, parent_state):
        if self._state.parent == parent_state:
            return

        if self._batch is not None:
            self._state = Sprite3dState(self._texture,
                                        self._state.blend_src,
                                        self._state.blend_dest,
                                        parent_state)
            self._vertex_list.delete()
            self._create_vertex_list()

    def _get_parent_state(self):
        return self._state.parent

    parent_state = property(_get_parent_state, _set_parent_state)

    def _get_model(self):
        if self._animation:
            return self._animation
        return self._model

    def _set_model(self, mdl):
        if self._animation is not None:
            clock.unschedule(self._animate)
            self._animation = None

        if isinstance(mdl, model.Animation):
            self._animation = mdl
            self._frame_index = 0
            self._next_dt = mdl.frames[0].delay
            clock.schedule_once(self._animate, self._next_dt)
        else:
            self._model = mdl

        self._tex_coords = mdl.tex_coords
        self._set_texture(mdl.texture)
        self._create_vertex_list()

    model = property(_get_model,
                     _set_model)

    def _set_texture(self, texture):
        if texture.id is not self._texture.id:
            self._texture = texture
            self._state = Sprite3dState(self._texture,
                                        self._state.blend_src,
                                        self._state.blend_dest,
                                        self._state.parent)

    def _set_image(self, img):
        pass

    image = property(_set_image)

    def _create_vertex_list(self):
        if self._batch is None:
            self._vertex_list = graphics.vertex_list(len(self._tex_coords)/2,
                    'v3f', 'c4B', ('t2f', self._tex_coords))
        else:
            self._vertex_list = self._batch.add(len(self._tex_coords)/2,
                GL_TRIANGLES, self._state, 'v3f', 'c4B',
                ('t2f', self._tex_coords))
        self._update_color()

    def _update_color(self):
        self._vertex_list.colors[:] = [255, 255, 255, self._opacity] * (len(self._tex_coords)/2)

    def set_position(self, x, y, z):
        self._state.position = [x, y, z]

    position = property(lambda self: (self._x, self._y, self._z),
                    lambda self, t: self.set_position(*t))

    def _set_x(self, x):
        self._state.position[0] = x

    x = property(lambda self: self._state.position[0],
                 _set_x)

    def _set_y(self, y):
        self._state.position[1] = y

    y = property(lambda self: self._state.position[1],
                 _set_y)

    def _set_z(self, z):
        self._state.position[2] = z

    z = property(lambda self: self._state.position[2],
                 _set_z)

    def _set_rotation(self, rotation):
        self._state.rotation = rotation

    rotation = property(lambda self: self._state.rotation,
                        _set_rotation)

    def _set_scale(self, scale):
        self._state.scale = scale

    scale = property(lambda self: self._state.scale,
                     _set_scale)

    def _set_opacity(self, opacity):
        self._opacity = opacity
        self._update_color()

    opacity = property(lambda self: self._opacity,
                       _set_opacity)

    def draw(self):
        self._state.set()
        self._vertex_list.draw(GL_TRIANGLES)
        self._state.unset()

    def update(self, dt):
        pass

Sprite3d.register_event_type('on_animation_end')
