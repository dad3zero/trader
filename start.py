#!/usr/bin/env python 

"""
Star Trader starter module

This should be the launched module.
"""

import argparse
from startrader import cli_game

parser = argparse.ArgumentParser()

parser.add_argument("--console", help="Launch the console version of the game",
                    action="store_true")
parser.parse_args()

cli_game.start()