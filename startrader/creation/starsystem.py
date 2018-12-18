"""
Star system creation tools
"""

import random

STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]


def create_starsystem(number_of_stars=4):
    """
    Prototype fonction for star system creation.

    :param number_of_stars: number of stars to create
    :return: a list of stars.
    """
    stars = []
    stars.append([STAR_NAMES[0], *get_sol_coordinates()])
    stars.append([STAR_NAMES[1], *get_frontier_class_coordinates()])
    stars.append([STAR_NAMES[2], *get_frontier_class_coordinates()])
    stars.append([STAR_NAMES[3], *get_underdeveloped_class_coordinates()])

    return stars


def get_sol_coordinates():
    """
    Create coordinates for SOL which should be the central star.
    :return: a tuple of coordinates
    """
    return 0, 0


def get_developed_class_coordinates():
    """
    Creates a new class II star coordinates. A class II star appears in the
    central 50 ly box.
    :return: a tuple of coordinates with values from -25 to 25
    """
    x = round(random.random() * 50) - 25
    y = round(random.random() * 50) - 25

    return x, y


def get_underdeveloped_class_coordinates():
    """
    Creates a new class III star coordinates. A class III star appears anywhere.
    :return: a tuple of coordinates with values from -50 to 50
    """
    x = round(random.random() * 100) - 50
    y = round(random.random() * 100) - 50

    return x, y


def get_frontier_class_coordinates():
    """
    Creates a new class IV star coordinates. A class IV star appears outside of
    the central 50 ly box.
    :return: a tuple of coordinates with values from -50 to -25 or 25 to 50.
    """
    x = random.random()
    x = round((x if x > 0.5 else x - 1) * 50)

    y = random.random()
    y = round(( y if y > 0.5 else y - 1) * 50)

    return x, y
