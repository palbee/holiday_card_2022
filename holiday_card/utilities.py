import numpy as np


def construct_bboxes(message, characters, center=False):
    x_strokes = []
    y_strokes = []
    x_start = 0
    prev_right = 0

    for c in message:
        char = characters[ord(c) - ord(' ')]
        x_start += prev_right + -char['left']
        x_stop = x_start + char['right']
        prev_right = char['right']
        x_strokes.append(np.array([x_start + char['left'], x_stop, x_stop, x_start + char['left']]))
        y_strokes.append(np.array([char['bottom'], char['bottom'], char['top'], char['top']]))
    if center:
        x_center = (x_start + prev_right) / 2.0
        x_strokes = [x - x_center for x in x_strokes]

    return x_strokes, y_strokes


def transform_strokes(x_strokes, y_strokes, width=1, height=1, base_x=0, base_y=0, rotation=0):
    transformed_x = []
    transformed_y = []
    for segments_x, segments_y in zip(x_strokes, y_strokes):
        # Scale
        segments_x = np.array(segments_x, dtype=float) * width
        segments_y = np.array(segments_y, dtype=float) * height

        # Rotate
        rotated_x = segments_x * np.cos(rotation) - segments_y * np.sin(rotation)
        rotated_y = segments_x * np.sin(rotation) + segments_y * np.cos(rotation)

        # Translate
        segments_x = rotated_x + base_x
        segments_y = rotated_y + base_y

        transformed_x.append(segments_x)
        transformed_y.append(segments_y)
    return transformed_x, transformed_y


def vert_squiggle(cycles=1.0):
    n_samples = np.ceil(30. * cycles).astype(int)
    y = np.linspace(0, 1, num=n_samples, endpoint=True)
    x_strokes = [(np.sin(y * np.pi * 2 * cycles) + 1) / 2.0]
    y_strokes = [np.array(y)]
    return x_strokes, y_strokes
