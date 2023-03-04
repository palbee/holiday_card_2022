"""String art tree generator."""
import numpy as np

from .utilities import transform_strokes


def string_art(width: float = 1, height: float = 1,
               n_steps: float = 20,
               base_x: float = 0., base_y: float = 0.,
               rotation=0) -> tuple[list[list[float]], list[list[float]]]:
    # pylint: disable=too-many-arguments
    """
    Construct a string art tree.

    The height of the tree is measured from the top of the trunk, with the
    trunk extending 0.1 * height below the tree.

    The output is a two-element tuple with the first element containing a
    list of lists of the x positions for the drawing segments. The second
    element is the positions.

    :param width: The width of the tree in millimeters
    :param height: The height of the tree in millimeters above the trunk.
    :param n_steps: The number of lines making up the tree.
    :param base_x: The x location of the tree's origin.
    :param base_y: The y location of the tree's origin.
    :param rotation: The rotation of the tree in radians.
    :return: The line segments representing the tree.

    """
    segments_x = []
    segments_y = []
    thetas = list(np.linspace(0, np.pi / 2, num=n_steps, endpoint=True))

    # Construct the base tree lines
    # The drawing alternates direction. This reduces motion in the final drawing.
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

    return transform_strokes(segments_x, segments_y,
                             width=width / 2.0, height=height,
                             base_x=base_x, base_y=base_y,
                             rotation=rotation)
