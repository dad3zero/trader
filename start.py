#!/usr/bin/env python 

"""
Star Trader starter module

This should be the launched module.
"""

import argparse
from startrader import cli_game

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--console", help="Launch the console version of the game",
                    action="store_true")
args = parser.parse_args()

if args.console:
    cli_game.start()

print("Bye")
