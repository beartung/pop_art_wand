# -*- coding: UTF-8 -*-
import os
import math
import json
import urllib2
from time import sleep
from functools import partial
import traceback

#http://www.imagemagick.org/Usage/montage/

PALETTE_DIR = "palette/"

def fetch_color_palette(id=None):
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
        print palette['id'], ' '.join(palette['colors'])
        out = open("%s%s.palette" % (PALETTE_DIR, palette['id']), 'w')
        colors = ' '.join([' '.join('0x%s' % c[x:x+2] for x in xrange(0, 6, 2)) for c in palette['colors']])
        out.write(colors)
        out.close()

if __name__ == '__main__':
    if not os.path.exists(PALETTE_DIR):
        os.mkdir(PALETTE_DIR)
    fetch_color_palette(1886982)
#    for i in xrange(1024):
#        fetch_color_palette()
#        sleep(1)
