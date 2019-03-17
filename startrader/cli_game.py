#!/usr/bin/env python 

"""
Main module for a legacy-cli style game
"""

from startrader import db_sqlite as db
from startrader import assets
from startrader.creation import starsystem


def create_universe(dao: db.UniverseDb):
    print('Star system not created, creating standard one.')
    stars = starsystem.create_starsystem(starsystem.STAR_NAMES)
    dao.save_starsystem(stars)

    return dao.load_starsystem()


def draw_map(stars):
    """
    Draw a map on the console

    :param stars: collection of stars to be displayed on the map. The first one
    is ignored
    """
    print("                      STAR MAP")
    print("                    ************")
    for y in range(15, -16, -1):
        line = list("                         |                             ")
        if y == 0:
            line = list(
                "+----+----+----+----+----*SOL-+----+----+----+----+    ")
        elif y % 3 == 0:
            line[25] = "+"

        y_hi = y * 10 / 3
        y_lo = (y + 1) * 10 / 3

        for star in stars[1:]:
            if y_lo > star.y >= y_hi:
                x = round(25 + star.x / 2)
                name = star.name
                line[x:x + len(name) + 1] = "*" + name
                break

        print("%s" % "".join(line))

    print("\nThe map is 100 Light-Years by 100 Light-Years,")
    print("so the cross-lines mark 10 light-years distances.")


def start(*args):
    universe_data = db.UniverseDb()

    config = universe_data.load_config()
    try:
        starsystem = universe_data.load_starsystem()
    except db.NoSuchComponentError:
        starsystem = create_universe(universe_data)
        
    print(assets.INTRO)
    draw_map(starsystem)


start()
