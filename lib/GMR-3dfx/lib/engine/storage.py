import include
from include import *

import display

class DisplayList(object):
    """An object to compile and store an OpenGL display list"""
    def __init__(self):
        """Creat the list"""
        self.gl_list = glGenLists(1)

    def begin(self):
        """Begin recording to the list - anything rendered after this will be compiled into the list and not actually rendered"""
        glNewList(self.gl_list, GL_COMPILE)

    def end(self):
        """End recording"""
        glEndList()

    def render(self):
        """Render the display list"""
        glCallList(self.gl_list)

    def __del__(self):
        """Clear the display list data"""
        try:
            glDeleteLists(self.gl_list, 1)
        except:
            pass #already cleared!

class VertexArray(object):
    """An object to store and render an OpenGL vertex array of vertices, colors and texture coords"""
    def __init__(self, render_type=None, max_size=100):
        """Create the array
           render_type is the OpenGL constant used in rendering, ie GL_POLYGON, GL_TRINAGLES, etc.
           max_size is the size of the array"""
        if render_type is None:
            render_type = GL_QUADS
        self.render_type = render_type
        self.texture = display.get_display().blank_texture

        self.max_size = max_size

        self.verts = numpy.zeros((max_size, 3), "f")
        self.colors = numpy.zeros((max_size, 4), "f")
        self.texcs = numpy.zeros((max_size, 2), "f")
        self.norms = numpy.array([[0,1,0]]*max_size, "f")

    def render(self):
        """Render the array"""
        self.texture.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        glVertexPointerf(self.verts)
        glColorPointerf(self.colors)
        glTexCoordPointerf(self.texcs)
        glNormalPointerf(self.norms)

        glDrawArrays(self.render_type, 0, self.max_size)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    def reset_verts(self, data):
        self.verts = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_colors(self, data):
        self.colors = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_texcs(self, data):
        self.texcs = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_norms(self, data):
        self.norms = numpy.array(data, "f")
        self.max_size = len(data)

    def update_verts(self, index, new):
        self.verts[index] = new

    def update_colors(self, index, new):
        self.colors[index] = new

    def update_texcs(self, index, new):
        self.texcs[index] = new

    def update_norms(self, index, new):
        self.norms[index] = new

    def resize(self, max_size):
        self.verts = numpy.resize(self.verts, (max_size, 3))
        self.colors = numpy.resize(self.colors, (max_size, 4))
        self.norms = numpy.resize(self.norms, (max_size, 3))
        self.texcs = numpy.resize(self.texcs, (max_size, 2))
        self.max_size = max_size

class VBOArray(object):
    def __init__(self, render_type=None, max_size=100, usage="static", cache_changes=False):
        """Create the array
           render_type is the OpenGL constant used in rendering, ie GL_POLYGON, GL_TRINAGLES, etc.
           max_size is the size of the array
           usage can be static, dynamic or stream (affecting render vs. modify speeds)
           cache_changes makes any changes between renderings be stored,
               and then only one modification is performed.
               NOTE: doing this actually modifies the entire buffer data, just efficiently
                     so this is only recommended if you are modifying a tremendous amount of points each frame!"""

        if not VBO_AVAILABLE:
            raise AttributeError("Vertex buffer objects not available!")

        self.usage = ("GL_"+usage+"_DRAW").upper()
        uses = {"GL_STATIC_DRAW":GL_STATIC_DRAW,
                "GL_DYNAMIC_DRAW":GL_DYNAMIC_DRAW,
                "GL_STREAM_DRAW":GL_STREAM_DRAW}
        self.usage_gl = uses[self.usage]

        self.cache_changes = cache_changes
        self._cached_cv = []
        self._cached_cc = []
        self._cached_ct = []
        self._cached_cn = []

        if render_type is None:
            render_type = GL_QUADS
        self.render_type = render_type

        self.texture = display.get_display().blank_texture

        self.max_size = max_size

        self.verts = vbo.VBO(numpy.zeros((max_size, 3), "f"), self.usage)
        self.colors = vbo.VBO(numpy.zeros((max_size, 4), "f"), self.usage)
        self.texcs = vbo.VBO(numpy.zeros((max_size, 2), "f"), self.usage)
        self.norms = vbo.VBO(numpy.array([[0,1,0]]*max_size, "f"), self.usage)

    def render(self):
        """Render the array"""
        if self.cache_changes:
            if self._cached_cv or self._cached_cc or self._cached_ct:
                for i in self._cached_cv:
                    self.verts.data[i[0]] = i[1]
                self.verts.bind()
                glBufferData(GL_ARRAY_BUFFER, self.verts.data, self.usage_gl)
                self._cached_cv = []

                for i in self._cached_cc:
                    self.colors.data[i[0]] = i[1]
                self.colors.bind()
                glBufferData(GL_ARRAY_BUFFER, self.colors.data, self.usage_gl)
                self._cached_cc = []

                for i in self._cached_ct:
                    self.texcs.data[i[0]] = i[1]
                self.texcs.bind()
                glBufferData(GL_ARRAY_BUFFER, self.texcs.data, self.usage_gl)
                self._cached_ct = []

                for i in self._cached_cn:
                    self.norms.data[i[0]] = i[1]
                self.norms.bind()
                glBufferData(GL_ARRAY_BUFFER, self.norms.data, self.usage_gl)
                self._cached_cn = []
        self.texture.bind()

        self.verts.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.verts)

        self.colors.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(self.colors)

        self.texcs.bind()
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointerf(self.texcs)

        self.norms.bind()
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointerf(self.norms)

        glDrawArrays(self.render_type, 0, self.max_size)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    def reset_verts(self, data):
        self.verts.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_colors(self, data):
        self.colors.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_texcs(self, data):
        self.texcs.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_norms(self, data):
        self.norms.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def update_verts(self, index, new):
        if self.cache_changes:
            self._cached_cv.append([index, new])
        else:
            self.verts.bind()
            #index multiplier is
            #4*len(new) - so since verts have 3 points, we get 12
            glBufferSubData(GL_ARRAY_BUFFER, 12*index, numpy.array(new, "f"))
            self.verts.data[index] = new

    def update_colors(self, index, new):
        if self.cache_changes:
            self._cached_cc.append([index, new])
        else:
            self.colors.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 16*index, numpy.array(new, "f"))
            self.colors.data[index] = new

    def update_texcs(self, index, new):
        if self.cache_changes:
            self._cached_ct.append([index, new])
        else:
            self.texcs.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 8*index, numpy.array(new, "f"))
            self.texcs.data[index] = new

    def update_norms(self, index, new):
        if self.cache_changes:
            self._cached_cn.append([index, new])
        else:
            self.norms.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 12*index, numpy.array(new, "f"))
            self.norms.data[index] = new

    def __del__(self):
        bufs = []
        for i in (self.verts, self.colors, self.texcs, self.norms):
            try:
                i.delete()
            except:
                pass #display closed - they should already be dead!

    def resize(self, max_size):
        self.max_size = max_size
        d = numpy.resize(self.verts.data, (max_size, 3))
        self.verts.set_array(d)

        d = numpy.resize(self.colors.data, (max_size, 4))
        self.colors.set_array(d)

        d = numpy.resize(self.texcs.data, (max_size, 2))
        self.texcs.set_array(d)

        d = numpy.resize(self.norms.data, (max_size, 3))
        self.norms.set_array(d)
