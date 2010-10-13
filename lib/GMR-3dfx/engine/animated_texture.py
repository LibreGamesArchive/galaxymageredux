import include
from include import *

import display
import texture

class GIFImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.image = PIL.open(filename)
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pygame.image.fromstring(image.tostring(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0,0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

class Texture(object):
    def __init__(self):
        self.textures = []
        self.durations = []
        self.size = (0,0)
        self.size_mult = (1,1)
        self.area = (0,0,1,1)

        self.ptime = time.time()
        self.cur_frame = 0

    def _from_file(self, filename):
        self._from_image(GIFImage(filename))

    def _from_image(self, image):
        self._compile(image)

    def free_texture(self):
        for i in self.textures:
            i.free_texture()
        self.textures = []
        self.durations = []

    def _compile(self, image):
        self.textures = []
        self.durations = []
        for frame in image.frames:
            frame, dur = frame
            self.durations.append(dur)
            image = texture.Texture()
            image._from_image(frame)
            self.textures.append(image)
        self.size = self.textures[0].size
        self.size_mult = self.textures[0].size_mult
        self.area = self.textures[0].area

    def bind(self):
        if time.time() - self.ptime > self.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.textures):
                self.cur_frame = 0

            self.ptime = time.time()

        self.textures[self.cur_frame].bind()

    def bind_orepeat(self, repeat):
        self.textures[self.cur_frame].bind_orepeat(repeat)

    def bind_frame(self, frame):
        self.textures[frame].bind()

    def coord(self, x, y):
        return self.textures[0].coord(x,y)

    def get_region(self, area):
        return TextureRegion(self, clamp_area(self.area, area))

class TextureClone(texture.TextureClone):
    def __init__(self, tex):
        texture.TextureClone.__init__(self, tex)

        self.ptime = time.time()
        self.cur_frame = 0

    def bind(self):
        self.check_swap()
        self.tex.bind_frame(self.cur_frame)

    def check_swap(self):
        if time.time() - self.ptime > self.tex.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.tex.textures):
                self.cur_frame = 0

            self.ptime = time.time()

    def get_region(self, area):
        return self.tex.get_region(self, clamp_area(self.area, area))

class TextureRegion(object):
    def __init__(self, tex, area):
        self.tex = tex

        self.textures = tex.textures
        self.durations = tex.durations
        self.area = area
        self.repeat = False

        x = self.area[2] - self.area[0]
        y = self.area[3] - self.area[1]
        self.size = x, y

        self.ptime = time.time()
        self.cur_frame = 0

    def bind(self):
        if time.time() - self.ptime > self.tex.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.tex.textures):
                self.cur_frame = 0

            self.ptime = time.time()

        self.textures[self.cur_frame].bind_orepeat(False)

    def coord(self, x, y):
        x1,y1,x2,y2 = self.area

        x += x1
        y += y1

        x = clamp(x1,x2, x)
        y = clamp(y1,y2, y)
        return self.tex.coord(x,y)

    def get_region(self, area):
        return TextureRegion(self, clamp_area(self.area, area))
