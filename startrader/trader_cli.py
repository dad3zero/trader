#!/usr/bin/env python 

import sys


def say(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()


def get_text():
    while True:
        s = sys.stdin.readline().upper().strip()
        if s != "":
            return s


def get_int():
    try:
        return int(get_text())
    except ValueError:
        return None


def in_range(lo, hi):
    return lambda n: lo <= n <= hi


def ask(text, checked):
    while True:
        say(text)
        n = get_int()
        if n is not None and checked(n):
            return n


def display_ga():
    say("\n                    *** GENERAL ANNOUNCEMENT ***\n\n")


def ask_for_expert_mode():
    say("HAVE ALL PLAYERS PLAYED BEFORE ")
    if get_text() == "Y":
        say("DO YOU WANT TO SET UP YOUR OWN GAME ")
        if get_text() == "Y":
            return own_game()

    return tuple()


def own_game():
    """
    Defines own game parameters

    :return: tuple  ships_per_player, number_of_stars, game_duration,
    max_weight, min_distance, number_of_rounds, profit_margin
    :rtype tuple:
    """
    ships_per_player = ask("HOW MANY SHIPS PER PLAYER (MAX 12) ",
                           lambda n: 0 < n <= 12)

    number_of_stars = ask("HOW MANY STAR SYSTEMS (FROM 4 TO 13 STARS) ",
                          in_range(4, 13))

    game_duration = ask("ENTER THE LENGTH OF GAME IN YEARS ", lambda n: n > 0)

    max_weight = ask("WHAT'S THE MAX CARGOE TONNAGE(USUALLY 30) ",
                     lambda n: n >= 25)

    say("WHAT'S THE MINIMUM DISTANCE BETWEEN STARS")
    min_distance = ask("(MIN SPACING 10, MAX 25, USUALLY 15) ",
                       in_range(10, 25))

    number_of_rounds = ask("HOW MANY BIDS OR OFFERS(USUALLY 3) ",
                           lambda n: n > 0)

    say("SET THE PROFIT MARGIN(1,2,3,4 OR 5)...THE HIGHER\n")
    say("THE NUMBER, THE LOWER THE PROFIT % ... USUALLY SET TO 2\n")
    profit_margin = ask("...YOUR NUMBER ", in_range(1, 5)) * 18

    return ships_per_player, number_of_stars, game_duration, max_weight, \
           min_distance, number_of_rounds, profit_margin


def setup_game():
    number_of_players = ask("HOW MANY PLAYERS (2,3, OR 4 CAN PLAY) ",
                            in_range(2, 4))

    player_prefs = ask_for_expert_mode()

    return number_of_players, player_prefs


def draw_map(stars):
    """
    Draw a map on the console

    :param stars: collection of stars to be displayed on the map. The first one
    is ignored
    """
    say("                      STAR MAP\n")
    say("                    ************\n")
    for y in range(15, -16, -1):
        line = list("                         |                             ")
        if y == 0:
            line = list(
                "1----1----1----1----1----*SOL-1----1----1----1----1    ")
        elif y % 3 == 0:
            line[25] = "+"
        y_hi = y * 10 / 3
        y_lo = (y + 1) * 10 / 3
        for s in range(1, len(stars)):
            if y_lo > stars[s].y >= y_hi:
                x = round(25 + stars[s].x / 2)
                name = stars[s].name
                line[x:x + len(name) + 1] = "*" + name
                break

        say("%s\n" % "".join(line))
    say("\nTHE MAP IS 100 LIGHT-YEARS BY 100 LIGHT-YEARS,\n")
    say("SO THE CROSS-LINES MARK 10 LIGHT-YEAR DISTANCES\n")


def display_new_star(new_star, stars):
    display_ga()
    say("A NEW STAR SYSTEM HAS BEEN DISCOVERED!  IT IS A CLASS IV\n")
    say("AND ITS NAME IS {}\n\n".format(new_star.name))
    draw_map(stars)
