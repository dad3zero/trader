#!/usr/bin/env python


def slope(x1: float, y1: float, x2: float, y2: float):
    """
    Calculate the slope (coéficient directeur in french)
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    :rtype: float
    """
    return (y2 - y1) / (x2 - x1)


def trajectory(x1: float, y1: float, x2: float, y2: float):
    """
    y = mx + k
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    m = slope(x1, y1, x2, y2)
    k = y1 - m * x1
