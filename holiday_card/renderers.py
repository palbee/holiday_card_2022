"""Renderers for generating gcode"""
import numpy as np

from .hershey_text import (construct_letter_bboxes, construct_message, cross_out_bbox,
                           transform_message)
from .trees import string_art


def render_gcode(x_strokes, y_strokes, draw_depth, safe_depth, destination):
    """
    Renders gcode from a collection of strokes.

    This renderer assumes that the plotter has already been configured with the (0,0) in the
    lower left of the machine's working envelope. The generated code also assumes that
    the machine has a working envelope of at least 230x180mm and the 0 on the z axis is above
    the working surface.

    :param x_strokes: The x positions of the stroke segments
    :param y_strokes: The y positions of the stroke segments
    :param draw_depth: The z position for drawing (in millimeters)
    :param safe_depth: The z position for non-drawing moves (in millimeters)
    :param destination: The file to write the gcode to.
    """
    for x_stroke, y_stroke in zip(x_strokes, y_strokes):
        destination.write(f"G0 X{x_stroke[0]} Y{y_stroke[0]} Z{safe_depth}\n")
        destination.write(f"G0 Z{draw_depth}\n")
        for x, y in zip(x_stroke[1:], y_stroke[1:]):
            destination.write(f"G1 X{x} Y{y} F1000\n")
        destination.write(f"G0 Z{safe_depth}\n")
    destination.write("G0 X230 Y180 Z0\n")


def make_outside_of_card(script_font, block_font):
    # pylint: disable=too-many-locals
    """
    Generate the outside of the card.
    :param script_font: The font definition for the script font
    :param block_font: The font definition for the block font.
    :return: The segments that define the card
    """
    x_segments = []
    y_segments = []

    # Front
    trees = ((100, 90, 45, 171, 46),  # width, height,n_lines, base_x, base_y
             (20, 18, 9, 140, 114),
             (10, 12, 5, 210, 95),
             (10, 25, 13, 130, 58),
             )

    for tree in trees:
        tree_x, tree_y = string_art(*tree)
        x_segments.extend(tree_x)
        y_segments.extend(tree_y)

    x_message, y_message = construct_message("Happy Holidays", script_font, center=True)
    x_message, y_message = transform_message(x_message, y_message, height=15, base_x=171, base_y=30)
    x_segments.extend(x_message)
    y_segments.extend(y_message)

    x_message, y_message = construct_message("202012", script_font, center=True)
    x_bbox, y_bbox = construct_letter_bboxes("202012", script_font, center=True)
    for cross_out in (3, 4):
        x_squiggle, y_squiggle = cross_out_bbox(x_bbox[cross_out], y_bbox[cross_out], cycles=3)
        x_message.extend(x_squiggle)
        y_message.extend(y_squiggle)
    x_message, y_message = transform_message(x_message, y_message, height=15, base_x=171, base_y=15)
    x_segments.extend(x_message)
    y_segments.extend(y_message)

    # Back
    x_url, y_url = construct_message("github.com/palbee/holiday_card_2022", block_font, center=True)
    x_url, y_url = transform_message(x_url, y_url, height=6, base_x=105, base_y=76,
                                     rotation=np.deg2rad(90))
    x_segments.extend(x_url)
    y_segments.extend(y_url)

    return x_segments, y_segments


def make_inside_of_card(script_font, block_font, closing):
    # pylint: disable=too-many-locals
    """
    Generate the inside of the card.

    :param script_font: The font definition for the script font
    :param block_font: The font definition for the block font.
    :param closing: The closing message
    :return: The segments that define the card
    """
    x_segments = []
    y_segments = []

    # Left
    message_lines = ["Best wishes for a", "wonderful holiday", "season and a", "happy New Year!"]
    for index, message in enumerate(message_lines):
        x_message, y_message = construct_message(message, block_font, center=False)
        x_message, y_message = transform_message(x_message, y_message, height=10, base_x=124,
                                                 base_y=120 - (index * 10))
        x_segments.extend(x_message)
        y_segments.extend(y_message)

    message_lines = [closing]
    for index, message in enumerate(message_lines):
        x_message, y_message = construct_message(message, script_font, center=False)
        x_message, y_message = transform_message(x_message, y_message, height=10, base_x=124,
                                                 base_y=40)
        x_segments.extend(x_message)
        y_segments.extend(y_message)

    # Right
    for x in range(12, 110, 10):
        tree_x, tree_y = string_art(8, 8, 8, x, 6)  # width, height,n_lines, base_x, base_y
        x_segments.extend(tree_x)
        y_segments.extend(tree_y)

    return x_segments, y_segments


def render_envelope(sender, recipient, block_font):
    # pylint: disable=too-many-locals
    """
    Generate the outside of the card.
    :param sender: The address in an array of strings of the sender
    :param recipient: The address in an array of strings of the sender
    :param block_font: The font definition for the address font
    :return: The segments that define the card
    """
    x_segments = []
    y_segments = []
    who = recipient[0].replace(' ', '_')

    text_height = 4
    message_lines = sender
    for index, message in enumerate(message_lines):
        x_message, y_message = construct_message(message, block_font, center=False)
        x_message, y_message = transform_message(x_message, y_message, height=text_height, base_x=5,
                                                 base_y=109 - text_height - (index * text_height))
        x_segments.extend(x_message)
        y_segments.extend(y_message)

    text_height = 5
    message_lines = recipient
    address_x = []
    address_y = []
    for index, message in enumerate(message_lines):
        x_message, y_message = construct_message(message, block_font, center=False)
        x_message, y_message = transform_message(x_message, y_message, height=text_height,
                                                 base_x=60, base_y=50 - (index * text_height))
        address_x.extend(x_message)
        address_y.extend(y_message)

    # Adjust for long names
    x_max = np.max([np.max(x) for x in address_x])
    if x_max > 146:
        x_delta = 145 - x_max
        address_x = [x + x_delta for x in address_x]

    x_segments.extend(address_x)
    y_segments.extend(address_y)

    return x_segments, y_segments, who
