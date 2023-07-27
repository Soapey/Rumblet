import os
from math import floor


def root_directory():
    root_path = os.path.abspath(".")
    return root_path


def get_grid_index(pixel_value, pixels_per_cell):
    return floor(pixel_value / pixels_per_cell)
