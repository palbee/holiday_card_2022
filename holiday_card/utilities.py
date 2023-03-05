"""Utility functions"""
import numpy as np


def normalize(x_strokes, y_strokes):
    """Rescales the strokes so the larger bounding box side length is 1.
    :param x_strokes: The x components got the segments comprising the message
    :param y_strokes: The y components got the segments comprising the message
    :return: The scaled strokes."""
    x_min = np.min([np.min(x) for x in x_strokes])
    x_max = np.max([np.max(x) for x in x_strokes])
    y_min = np.min([np.min(y) for y in y_strokes])
    y_max = np.max([np.max(y) for y in y_strokes])

    x_range = x_max - x_min
    y_range = y_max - y_min

    scale_factor = max(x_range, y_range)
    x_strokes = [(x - x_min) / scale_factor for x in x_strokes]
    y_strokes = [(y - y_min) / scale_factor for y in y_strokes]

    return x_strokes, y_strokes


def transform_strokes(x_strokes, y_strokes, width=1, height=1, base_x=0,
                      base_y=0, rotation=0):
    # pylint: disable=too-many-arguments
    """" Transform the strokes.
    :param x_strokes: The x components of the strokes
    :param y_strokes: The y components of the strokes
    :param width: The desired width of the strokes
    :param height: The desired height of the strokes
    :param base_x: The new x base position
    :param base_y: The new y base position
    :param rotation: The CCW rotation of the message in radians
    :return: The transformed coordinates.

    """
    transformed_x = []
    transformed_y = []
    for segments_x, segments_y in zip(x_strokes, y_strokes):
        # Scale
        segments_x = np.array(segments_x, dtype=float) * width
        segments_y = np.array(segments_y, dtype=float) * height

        # Rotate
        rotated_x = segments_x * np.cos(rotation) - segments_y * np.sin(
            rotation)
        rotated_y = segments_x * np.sin(rotation) + segments_y * np.cos(
            rotation)

        # Translate
        segments_x = rotated_x + base_x
        segments_y = rotated_y + base_y

        transformed_x.append(segments_x)
        transformed_y.append(segments_y)
    return transformed_x, transformed_y


def vert_squiggle(cycles=1.0):
    """
    Create cycles sine waves inside a 1x1 boc

    :param cycles: The number of cycles for the sine wave
    :return: The segments making up the squiggle
    """
    n_samples = np.ceil(30. * cycles).astype(int)
    y = np.linspace(0, 1, num=n_samples, endpoint=True)
    x_strokes = [(np.sin(y * np.pi * 2 * cycles) + 1) / 2.0]
    y_strokes = [np.array(y)]
    return x_strokes, y_strokes
