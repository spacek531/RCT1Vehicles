import png
import sys
import shutil
from pathlib import Path
import itertools

palpath2 = Path("D:/Documents/OpenRCT2/Custom Rides/RCT1 Project/terrain/palette_gif.png")
palpath = Path("D:/Documents/OpenRCT2/Custom Rides/RCT1 Project/terrain/palette_green.png")

UseOldPalette = False
BorderIndexOffset = 1



class rgba:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return "#{0:02x}{1:02x}{2:02x}-{3:02x}".format(self.r, self.g, self.b, self.a)

    def __eq__(self,other):
        if isinstance(other, rgba):
            return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
        return False

    def tupleRGBA(self):
        return (self.r, self.g, self.b, self.a)

    def tupleRGB(self):
        return (self.r, self.g, self.b)

class palette:
    def __init__(self, path):
        tup = png.Reader(filename = path).asRGBA()
        rawdata = list(tup[2])
        self.palette = []
        self.length = tup[0]*tup[1]
        self.transparentIndex = 0
        for row in rawdata:
            for i in range(0,tup[0] * 4, 4):
                self.palette.append(rgba(row[i],row[i+1],row[i+2],row[i+3]))
        print("Loaded palette {0} with {1} indices".format(path, len(self.palette)))
    
    def getIndex(self, pix):
        for i in range(len(self.palette)):
            if (pix == self.palette[i]):
                return i
        return self.transparentIndex

    def renderRGBA(self, width, height, pixpal):
        image = []
        pointer = 0
        for i in range(height):
            pixlist = pixpal[i * width : (i + 1) * width]
            renderedrow = [self.palette[pix % 256].tupleRGBA() for pix in pixlist]
            row = itertools.chain(*renderedrow)
            image.append(list(row))
        return image

    def renderRGB(self, width, height, pixpal):
        image = []
        pointer = 0
        for i in range(height):
            pixlist = pixpal[i * width : (i + 1) * width]
            renderedrow = [self.palette[pix % 256].tupleRGB() for pix in pixlist]
            row = itertools.chain(*renderedrow)
            image.append(list(row))
        return image

    def renderPalette(self):
        return [p.tupleRGB() for p in self.palette]



outpalette = palette(palpath)
inpallete = UseOldPalette and palette(palpath2) or outpalette


workingdir = Path("D:/Documents/OpenRCT2/Custom Rides/RCT1 Project/object/terrain_surface")

g1dir = Path("D:/Documents/OpenRCT2/g1dump")

for i in range(19):
    src = Path(workingdir,"{0:02d}.png".format(i + 19))
    dst = Path(workingdir,"{0:02d}.png".format(i))
    maskin = Path(workingdir,"{0:02d}.png".format(i + 38))
    maskout = Path(workingdir,"{0:02d}.png".format(i + 57))
    print("loading image {0} and mask {1}".format(src, maskin))
    imgdata = png.Reader(filename = src).asRGBA()
    width = imgdata[0]
    height = imgdata[1]
    pixdata = list(imgdata[2])

    imgdata = png.Reader(filename = maskin).asRGBA()
    assert(imgdata[0] == width and imgdata[1] == height)
    maskdta = list(imgdata[2])

    pixpal = []
    pixpalmask = []

    ppall = 0

    print("image data: height: {0}, width: {1}".format(height, width))
    for y in range(len(pixdata)):
            row = pixdata[y]
            for i in range(0,width * 4, 4):
                x = i/4
                pix = rgba(row[i],row[i+1],row[i+2],row[i+3])
                pindex = inpallete.getIndex(pix)

                mrow = maskdta[y]
                maskin = inpallete.getIndex(rgba(mrow[i],mrow[i+1],mrow[i+2],mrow[i+3])) != 0

                borderPixel = False
                if ((y + 1 == height) and (ppall > 0)):
                    if pindex == 0 and pixpal[ppall-width] != 0: # the current pixel is void and the one above is not
                        if pixpal[ppall-width] < 256:
                            pixpal[ppall-width] += 256 + BorderIndexOffset
                    if pindex != 0:
                        borderPixel = True # lower edge is a void
                elif (y > 0):
                    if pixpal[ppall-width] == 0 and pindex > 0: # pixel above is void and I am not
                        borderPixel = True
                    if pindex == 0 and pixpal[ppall-width] != 0: # the current pixel is void and the one above is not
                        if pixpal[ppall-width] < 256:
                            pixpal[ppall-width] += 256 + BorderIndexOffset
                elif pindex > 0:
                    borderPixel = True # upper edge is a void

                if ((x + 1 == width) and (ppall > 0)):
                    if pindex == 0 and pixpal[ppall - 1] != 0: # the current pixel is is void and the one to the left is not
                        if pixpal[ppall-1] < 256:
                            pixpal[ppall-width] += 256 + BorderIndexOffset
                    if pindex != 0:
                        borderPixel = True # right edge is a void
                elif (x > 0):
                    if pixpal[ppall - 1] == 0 and pindex > 0: # pixel to the left is void and I am not
                        borderPixel = True
                    if pindex == 0 and pixpal[ppall - 1] != 0: # the current pixel is is void and the one to the left is not
                        if pixpal[ppall-1] < 256:
                            pixpal[ppall-width] += 256 + BorderIndexOffset
                elif pindex > 0:
                    borderPixel = True # left edge is a void

                if borderPixel:
                    pindex += 256 + BorderIndexOffset
                    if (x*y)%3 == 0:
                        pindex += 1

                pixpal.append(pindex)
                pixpalmask.append(maskin * pindex)
                ppall += 1

    palette = outpalette.renderPalette()
    #imager = [pixpal[i * width : (i + 1) * width] for i in range(height)]
    imager = outpalette.renderRGBA(width, height, pixpal)
    with open(dst, "wb") as f: 
        #w = png.Writer(width = width, height  = height, greyscale = False, palette = palette)
        w = png.Writer(width = width, height  = height, greyscale = False, alpha = True)
        w.write(f, imager)

    #imager = [pixpalmask[i * width : (i + 1) * width] for i in range(height)]
    imager = outpalette.renderRGBA(width, height, pixpalmask)
    with open(maskout, "wb") as f: 
        #w = png.Writer(width = width, height  = height, greyscale = False, palette = palette)
        w = png.Writer(width = width, height  = height, greyscale = False, alpha = True)
        w.write(f, imager)
