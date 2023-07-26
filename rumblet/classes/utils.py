import os
from math import ceil


def root_directory():
    root_path = os.path.abspath(".")
    return root_path


def is_colliding(left1, top1, width1, height1, left2, top2, width2, height2):
    right1, bottom1 = left1 + width1, top1 + height1
    right2, bottom2 = left2 + width2, top2 + height2

    if (
        (right1 >= left2 and bottom1 >= top2 and top1 < top2 and left1 < left2) or
        (left1 <= right2 and bottom1 >= top2 and top1 < top2 and right1 > right2) or
        (right1 >= left2 and top1 <= bottom2 and bottom1 > bottom2 and left1 < left2) or
        (left1 <= right2 and top1 <= bottom2 and bottom1 > bottom2 and right1 > right2) or
        (left1 == left2 and right1 == right2 and top1 == top2 and bottom1 == bottom2)
    ):
        return True
    else:
        return False

def get_grid_index(pixel_value, pixels_per_cell):
    return ceil(pixel_value / pixels_per_cell)


def grid_indexes_are_colliding(x1, y1, x2, y2, pixels_per_cell_x, pixels_per_cell_y):
    x1_grid_index = get_grid_index(x1, pixels_per_cell_x)
    y1_grid_index = get_grid_index(y1, pixels_per_cell_y)

    x2_grid_index = get_grid_index(x2, pixels_per_cell_x)
    y2_grid_index = get_grid_index(y2, pixels_per_cell_y)

    return x1_grid_index == x2_grid_index and y1_grid_index == y2_grid_index
