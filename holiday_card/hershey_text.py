import numpy as np

from holiday_card.utilities import transform_strokes, vert_squiggle


def construct_message(message, characters, center=False):
    x_strokes = []
    y_strokes = []
    x_start = 0
    prev_right = 0

    for c in message:
        char = characters[ord(c) - ord(' ')]
        x_start += prev_right + -char['left']
        prev_right = char['right']
        for x, y in zip(char['x_strokes'], char['y_strokes']):
            x_strokes.append(x + x_start)
            y_strokes.append(y)

    if center:
        x_center = (x_start + prev_right) / 2.0
        x_strokes = [x - x_center for x in x_strokes]

    return x_strokes, y_strokes


def load_font(file_name):
    """Load a font file.
The format of the files is described as follows:

 The structure is basically as follows: each character consists of a number 1->4000 (not all
 used) in column 0:4, the number of vertices in columns 5:7, the left hand position in column 8,
 the right hand position in column 9, and finally the vertices in single character pairs. All
 coordinates are given relative to the ascii value of 'R'. If the coordinate value is " R" that
 indicates a pen up operation.
As an example consider the 8th symbol

8 9MWOMOV RUMUV ROQUQ
It has 9 coordinate pairs (this includes the left and right position).
The left position is 'M' - 'R' = -5
The right position is 'W' - 'R' = 5
The first coordinate is "OM" = (-3,-5)
The second coordinate is "OV" = (-3,4)
Raise the pen " R"
Move to "UM" = (3,-5)
Draw to "UV" = (3,4)
Raise the pen " R"
Move to "OQ" = (-3,-1)
Draw to "UQ" = (3,-1)
Drawing this out on a piece of paper will reveal it represents an 'H'.

The encoding and description assume a left-handed coordinate system, while this function
generates strokes for
a right-handed coordinate system.
This is accomplished by changing the second (y) elemement of each vertex to be computed as
'R'-'<character>'
"""
    R = ord('R')
    characters = []
    index = 0
    with open(file_name) as font:
        font.seek(0, 2)
        file_size = font.tell()
        font.seek(0)
        while font.tell() != file_size:
            number = font.read(5)
            number = int(number.strip())
            if number == 12345:
                number = index

            pairs = int(font.read(3))
            coding = ""
            while len(coding) / 2 < pairs:
                coding = coding + font.readline().rstrip("\n")
            left = ord(coding[0]) - R
            right = ord(coding[1]) - R
            coords = []
            top = 0
            bottom = 0
            x_vertices = []
            y_vertices = []
            x_strokes = []
            y_strokes = []
            for i in range(2, len(coding) - 1, 2):
                if coding[i:i + 2] == ' R':
                    if x_vertices:
                        x_strokes.append(np.array(x_vertices, dtype=float))
                        y_strokes.append(np.array(y_vertices, dtype=float))
                        x_vertices = []
                        y_vertices = []

                else:
                    x = ord(coding[i]) - R
                    y = R - ord(coding[i + 1])
                    top = max(top, y)
                    bottom = min(bottom, y)
                    x_vertices.append(x)
                    y_vertices.append(y)
            if x_vertices:
                x_strokes.append(np.array(x_vertices, dtype=float))
                y_strokes.append(np.array(y_vertices, dtype=float))

            characters.append({'char': chr(ord(' ') + index),
                               'number': number,
                               'left': left,
                               'right': right,
                               'top': top,
                               'bottom': bottom,
                               'x_strokes': x_strokes,
                               'y_strokes': y_strokes})
            index += 1
        top = max((x['top'] for x in characters))
        bottom = min((x['bottom'] for x in characters))
        scale = 1.0 / (top - bottom)
        for character in characters:
            character['top'] *= scale
            character['bottom'] *= scale
            character['left'] *= scale
            character['right'] *= scale
            character['x_strokes'] = [x * scale for x in character['x_strokes']]
            character['y_strokes'] = [y * scale for y in character['y_strokes']]

    return characters


def transform_message(x_strokes, y_strokes, height=1, base_x=0, base_y=0, rotation=0):
    return transform_strokes(x_strokes, y_strokes, width=height, height=height, base_x=base_x,
                             base_y=base_y, rotation=rotation)


def cross_out_bbox(x_bbox, y_bbox, cycles=1):
    x_squig, y_squig = vert_squiggle(cycles)

    base_x = x_bbox[0]
    base_y = y_bbox[0]
    width = x_bbox[1] - x_bbox[0]
    height = y_bbox[2] - y_bbox[1]
    x_squig, y_squig = transform_strokes(x_squig, y_squig, base_x=base_x, base_y=base_y,
                                         width=width, height=height)
    return x_squig, y_squig
