import numpy as np


def string_art(width=1, height=1, n_steps=20, base_x=0., base_y=0., rotation=0):
    dx = np.array([np.cos(rotation), np.sin(rotation)]) * width
    dy = np.array([-np.sin(rotation), np.cos(rotation)]) * height
    segments_x = []
    segments_y = []
    thetas = list(np.linspace(0, np.pi / 2, num=n_steps, endpoint=True))

    # Construct the base tree lines
    # The Tree
    even = True
    for theta in thetas:
        if even:
            segments_x.append([np.cos(theta), 0, -np.cos(theta)])
        else:
            segments_x.append([-np.cos(theta), 0, np.cos(theta)])
        even = not even
        segments_y.append([0, np.sin(theta), 0])
    # The Trunk
    trunk_depth = -0.1
    trunk_width = 0.1
    segments_x.append([-trunk_width, -trunk_width, trunk_width])
    segments_y.append([0, trunk_depth, trunk_depth])
    segments_x.append([trunk_width, trunk_width, -trunk_width])
    segments_y.append([trunk_depth, 0, 0])

    # Scale
    segments_x = np.array(segments_x, dtype=float) * (width / 2.0)
    segments_y = np.array(segments_y, dtype=float) * height

    # Rotate
    rotated_x = segments_x * np.cos(rotation) - segments_y * np.sin(rotation)
    rotated_y = segments_x * np.sin(rotation) + segments_y * np.cos(rotation)

    # Translate
    segments_x = rotated_x + base_x
    segments_y = rotated_y + base_y

    return segments_x, segments_y
