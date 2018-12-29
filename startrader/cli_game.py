#!/usr/bin/env python 

"""
Main module for a legacy-cli style game
"""

from startrader import db_sqlite as db


def start(*args):
    universe_data = db.UniverseDb()

    config = universe_data.load_config()
    print(config)
