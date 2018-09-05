#!/usr/bin/env python 

"""
Collection of space economic ressources
"""


# *** DATA FOR ECONOMETRIC MODEL FOLLOWS ***
# [k, b], y = k * x + b
# Table is for Frontier, underdeveloped, developed or above
ECONOMIC = [
    [[-0.1, 1], [-0.2, 1.5], [-0.1, 0.5]],
    [[0, 0.75], [-0.1, 0.75], [-0.1, 0.75]],
    [[0, -0.75], [0.1, -0.75], [0.1, -0.75]],
    [[-0.1, -0.5], [0.1, -1.5], [0, 0.5]],
    [[0.1, -1], [0.2, -1.5], [0.1, -0.5]],
    [[0.1, 0.5], [-0.1, 1.5], [0, -0.5]]
]


def transfer_credit(t_from, t_to, value):
    t_from.sum -= value
    t_to.sum += value


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
