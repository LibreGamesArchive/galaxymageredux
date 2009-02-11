# Copyright (c) 2007, A. Joseph Hager
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#   * No personal names or organizational names may be used to endorse 
#   or promote products derived from this software without specific prior 
#   written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import struct

from pyglet.gl import *
from pyglet import image
from pyglet import graphics
from pyglet import resource

class Header:
    def __init__(self, headerData):
        self.ident = headerData[0]
        self.version = headerData[1]
        self.skinWidth = headerData[2]
        self.skinHeight = headerData[3]
        self.frameSize = headerData[4]
        self.numSkins = headerData[5]
        self.numVertices = headerData[6]
        self.numTexCoords = headerData[7]
        self.numTriangles = headerData[8]
        self.numGlCommands = headerData[9]
        self.numFrames = headerData[10]
        self.offsetSkins = headerData[11]
        self.offsetTexCoords = headerData[12]
        self.offsetTriangles = headerData[13]
        self.offsetFrames = headerData[14]
        self.offsetGlCommands = headerData[15]
        self.offsetEnd = headerData[16]

class TexCoord:
    def __init__(self, s, t):
        self.s = s
        self.t = t

class Triangle:
    def __init__(self, vertexIndices, textureIndices):
        self.vertexIndices = vertexIndices
        self.textureIndices = textureIndices

class Vertex:
    def __init__(self, vertex):
        self.x = vertex[0]
        self.y = vertex[1]
        self.z = vertex[2]

class Frame:
    def __init__(self, scale, translate, name, vertices):
        self.name = name
        self.vertices = vertices
        self.varray = []
        self.tarray = []
        for v in self.vertices:
            v.x = v.x * scale[0] + translate[0]
            v.y = v.y * scale[1] + translate[1]
            v.z = v.z * scale[2] + translate[2]

class MD2Model:
    def __init__(self, filename, texFilename, interpolate=False):
        self.skins = []
        self.texCoords = []
        self.triangles = []
        self.frames = []
        self.animations = {}
        self.texture = None
        self.currentFrame = None 
        self.nextFrame = None
        self.currentAnimation = None
        self.elapsedTime = 0
        self.animationSpeed = .1 
        self.interpolate = interpolate

        self.load(filename)
        self.setTexture(texFilename)
        self.setupAnimations()
        if self.animations:
            self.setAnimation(self.animations.keys()[0])
        self.currentFrame = self.animations[self.currentAnimation][0]
        self.createArrays()
        
    def load(self, filename):
        # Open file
        file = resource.file(filename, 'rb')
        
        # Read in the header information
        headerData = struct.unpack('<17i', file.read(17 * 4))
        header = Header(headerData)
        
        # Check magic number.  Must be equal to "IPD2"
        if header.ident != 844121161: # "IPD2"
            raise SystemExit("Invalid md2 file: %s" % filename)

        # Check md2 version.  Must be equal to 8.
        if header.version != 8:
            raise SystemExit("Invalid md2 file: %s" % filename)

        # Read skin names
        file.seek(header.offsetSkins)
        for i in xrange(header.numSkins):
            skinName = struct.unpack('<64s', file.read(64))[0].split('\x00')[0]
            self.skins.append(skinName)

        # Read texture coordinates
        file.seek(header.offsetTexCoords)
        for i in xrange(header.numTexCoords):
            tc = struct.unpack('<2h', file.read(4))
            tc = (tc[0] / float(header.skinWidth),
                        tc[1] / float(header.skinHeight))
            self.texCoords.append(TexCoord(tc[0], tc[1]))

        # Read triangle data
        file.seek(header.offsetTriangles)
        for i in xrange(header.numTriangles):
            vertexIndices = struct.unpack('<3h', file.read(6))
            textureIndices = struct.unpack('<3h', file.read(6))
            self.triangles.append(Triangle(vertexIndices, textureIndices))

        # Read frames
        file.seek(header.offsetFrames)
        for i in xrange(header.numFrames):
            scale = struct.unpack('<3f', file.read(12))
            translate = struct.unpack('<3f', file.read(12))
            name = struct.unpack('<16s', file.read(16))[0].split('\x00')[0]
            
            vertices = []
            for j in xrange(header.numVertices):
                vertex = struct.unpack('<3B', file.read(3))
                lightNormal = struct.unpack('<B', file.read(1))[0]
                
                vertices.append(Vertex(vertex))
            
            self.frames.append(Frame(scale, translate, name, vertices))
    
    def createArrays(self):
        # Create a vertex array for each frame
        for frame in self.frames:
            for triangle in self.triangles:
                for j in [0, 1, 2]:
                    index = triangle.vertexIndices[j]
                    v = frame.vertices[index]
                    frame.varray.append(v.y)
                    frame.varray.append(v.z)
                    frame.varray.append(v.x)

                    texIndex = triangle.textureIndices[j]
                    frame.tarray.append(self.texCoords[texIndex].s)
                    frame.tarray.append(1.0 - self.texCoords[texIndex].t)

    def setupAnimations(self):
        for i in xrange(len(self.frames)):
            str = self.frames[i].name
            frameNum = 0

            for j in xrange(len(str)):
                if str[j].isdigit() and j >= len(str) - 2:
                    str = str[:j]
                    break

            if not self.animations.has_key(str):
                self.animations[str] = (i, i)
            else:
                low, high = self.animations[str]
                self.animations[str] = (low, i)

    def setTexture(self, filename):
        self.texture = resource.image(filename).texture

    def setAnimation(self, name):
        if name in self.animations:
            self.currentAnimation = name
            self.currentFrame = self.animations[name][0]

    def update(self, dt):
        self.elapsedTime += dt
        if self.elapsedTime >= self.animationSpeed:
            self.elapsedTime = 0
            self.currentFrame += 1

        maxFrame = self.animations[self.currentAnimation][1]
        startFrame = self.animations[self.currentAnimation][0]

        if self.currentFrame > maxFrame:
            self.currentFrame = startFrame

        self.nextFrame = self.currentFrame + 1

        if self.nextFrame > maxFrame:
            self.nextFrame = startFrame

    def draw(self):
        if self.interpolate:
            t = self.elapsedTime / self.animationSpeed
            arrayA = self.frames[self.currentFrame].varray
            arrayB = self.frames[self.nextFrame].varray
            arrayV = map((lambda a, b: a + t * (b - a)), arrayA, arrayB)
        else:
            arrayV = self.frames[self.currentFrame].varray

        num = len(arrayV)/3
        arrayT = self.frames[self.currentFrame].tarray

        glBindTexture(self.texture.target, self.texture.id)
        graphics.draw(num, GL_TRIANGLES, ('t2f', arrayT), ('v3f', arrayV))
