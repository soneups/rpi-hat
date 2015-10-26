# Copyright 2013-2015 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.
# this file enos.in/hatpe

import sys
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from EPD import EPD

WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf',              # B.B
    '/usr/share/fonts/TTF/FreeMonoBold.ttf',                          # Arch
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'                        # Arch
]


FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'

TEXT_FONT_SIZE = 15
HEADING_FONT_SIZE  = 20


def main(argv):
    """main program - draw and display a test image"""

    epd = EPD()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))

    epd.clear()

    demo(epd)


def demo(epd):
    """simple drawing demo - black drawing on white background"""

    text_font = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE)
    heading_font = ImageFont.truetype(FONT_FILE, HEADING_FONT_SIZE)

    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    # text
    draw.text((1, 1), 'RPI: Boot information', fill=BLACK, font=heading_font) #col/row from top left
    draw.text((40, 20+20), 'IP Address: 192.x.x.x', fill=BLACK, font=text_font) #col/row from top left
    draw.text((40, 40+20), 'Hostname  : <>', fill=BLACK, font=text_font) #col/row from top left

    # display image on the panel
    epd.display(image)
    epd.update()


# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))
    main(sys.argv[1:])


