#!/usr/bin/env python 

from startrader import model as m


def test_start_location_none():
    ship = m.Ship(None)
    assert ship.star is None


def test_can_set_location():
    ship = m.Ship(None)
    ship.location = "here"
    assert "here" == ship.star
    assert "here" == ship.location
