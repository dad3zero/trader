#!/usr/bin/env python 

"""
Collection of space economic ressources
"""


def price_window(good_units, units, current_round):
    w = 0.5

    if units < abs(good_units):
        w = units / (2 * abs(good_units))
    return w / (current_round + 1)


def sold(ship, index, units, price):
    ship.goods[index] += units
    if index < 4:
        ship.weight += units
    ship.star.goods[index] -= units
    ship.sum -= price
