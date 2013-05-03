# -*- coding: UTF-8 -*-
"""
Pop Art with ImageMagick using wand
based on http://codeboje.de/fun-colors-or-making-art-python/
with wand fork: https://github.com/beartung/wand
"""
import os
import json
import urllib2
from functools import partial

inputdir = 'in'
tmpdir = '/tmp/pop_art'
outputdir= 'out'

from wand.image import Image
from wand.color import Color
from wand.api import library

def get_color(colors, index):
    return '#' + colors[index]

def pop_art_color(x, y, color, colors):
    r = color.red * 255
    if r < 50:
        color = get_color(colors, 0)
    elif r < 100:
        color = get_color(colors, 1)
    elif r < 150:
        color = get_color(colors, 2)
    elif r < 200:
        color = get_color(colors, 3)
    else:
        color = get_color(colors, 4)
    return Color(color)

#http://www.colourlovers.com/api/palette/1886982/?format=json
def get_color_palette(id=None):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    url = 'http://www.colourlovers.com/api/palettes/random?format=json'
    if id:
        url = 'http://www.colourlovers.com/api/palette/%s/?format=json' % id
    req = urllib2.Request(url, '', headers)
    response = urllib2.urlopen(req)
    palettes = json.load(response)
    palette = palettes[0]
    if len(palette['colors']) == 5:
        return palette


def center_crop(img, size=256):
    cw = size
    ch = size
    iw = img.width
    ih = img.height
    if iw > cw and ih > ch:
        #iw/ih <= cw/ch
        if iw*ch <= cw*ih:
            th = int(ih*cw / float(iw))
            #print "to h", th
            #print "resize to", cw, th
            img.resize(cw, th, "catrom")
            ot = (th - ch) % 2
            dy = (th - ch) / 2
            #print "dy", dy
            #print "crop", 0, dy, cw, th - dy
            img.crop(0, dy, cw, th - dy - ot)
        else:
            tw = int(iw*ch / float(ih))
            #print "to w", tw
            #print "resize to", tw, ch
            img.resize(tw, ch, "catrom")
            ot = (tw - cw) % 2
            dx = (tw - cw) / 2
            #print "dx", dx, "ot", ot
            #print "crop", dx, 0, tw - dx - ot, ch
            img.crop(dx, 0, tw - dx - ot, ch)
    elif iw > cw and ih <= ch:
        ot = (iw - cw) % 2
        dx = (iw - cw) / 2
        #rint "crop", dx, 0, iw - dx - 1, ch
        img.crop(dx, 0, iw - dx - ot, ch)
    elif iw <= cw and ih > ch:
        ot = (ih - ch) % 2
        dx = (ih - ch) / 2
        #print "crop", 0, dx, cw, ih - dx
        img.crop(0, dx, cw, ih - dx - ot)
    elif iw < cw and ih < ch:
        img.size(cw, ch, "catrom")

def main():
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    palette = get_color_palette(1886982)
    print 'using palette %s ( %s )' % (palette['title'], palette['url'])
    for img_file in os.listdir(inputdir):
        (file_basename, file_extension)=os.path.splitext(img_file)
        print 'processing %s' % file_basename
        input_name = '%s/%s' % (inputdir, img_file)
        tempfile = file_basename + '_tmp' + file_extension
        temp_name = '%s/%s' % (tmpdir, tempfile)
        with Image(filename=input_name) as img:
            center_crop(img)
            img.save(filename=temp_name)
        print 'save resized image to %s' % temp_name
        output_name = file_basename + '_' + str(palette['id']) + '_' + palette['title']  + file_extension
        output_name = '%s/%s' % (outputdir, output_name)
        colors = palette['colors']
        pop_art = partial(pop_art_color, colors=colors)
        with Image(filename=temp_name) as img:
            img.recolor(color_func=pop_art)
            img.save(filename=output_name)
        print 'done to %s' % output_name
        print 'processing %s with reverse color' % file_basename
        colors.reverse()
        pop_art_reverse = partial(pop_art_color, colors=colors)
        output_name = file_basename + '_' + str(palette['id']) + '_' + palette['title']  + "_dec" + file_extension
        output_name = '%s/%s' % (outputdir, output_name)
        with Image(filename=temp_name) as img:
            img.recolor(color_func=pop_art_reverse)
            img.save(filename=output_name)
        print 'done to %s' % output_name

def test_64():
    palette = get_color_palette(1886982)
    colors = palette['colors']
    pop_art = partial(pop_art_color, colors=colors)
    with Image(filename="in/test.jpg") as img:
        center_crop(img, 64)
        img.save(filename="in/t.jpg")
    with Image(filename="in/t.jpg") as img:
        img.recolor(color_func=pop_art)
        img.save(filename="test_out.jpg")

if __name__ == '__main__':
    #main()
