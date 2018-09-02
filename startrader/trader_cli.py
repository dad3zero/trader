#!/usr/bin/env python

import sys

from startrader import assets
from startrader import model


def say(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()


def get_text():
    while True:
        sentence = sys.stdin.readline().upper().strip()
        if sentence != "":
            return sentence


def get_int():
    try:
        return int(get_text())
    except ValueError:
        return None


def in_range(low, high):
    return lambda n: low <= n <= high


def ask(text, checked):
    while True:
        say(text)
        number = get_int()
        if number is not None and checked(number):
            return number


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


def name_ships(fleets):
    say("As Captains, you have to name your ships.\n")
    for index, player in enumerate(fleets):
        say("   CAPTAIN {}\n".format(index))
        say("   What is your name ?\n".format(index))
        player.name = get_text()
        for ship_index, ship in enumerate(player.ships):
            say("   Name your ship # {}\n".format(ship_index))
            ship.name = get_text()
            ship.player_index = index


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
                "+----+----+----+----+----*SOL-+----+----+----+----+    ")
        elif y % 3 == 0:
            line[25] = "+"
        y_hi = y * 10 / 3
        y_lo = (y + 1) * 10 / 3
        for star_index in range(1, len(stars)):
            if y_lo > stars[star_index].y >= y_hi:
                x = round(25 + stars[star_index].x / 2)
                name = stars[star_index].name
                line[x:x + len(name) + 1] = "*" + name
                break

        say("%s\n" % "".join(line))
    say("\nTHE MAP IS 100 LIGHT-YEARS BY 100 LIGHT-YEARS,\n")
    say("SO THE CROSS-LINES MARK 10 LIGHT-YEAR DISTANCES\n")


def display_eta(star_name, scheduled_arrival):
    arrival_month = int((scheduled_arrival[1] - 1) / 30)

    say("THE ETA AT {} IS {} {}, {}\n".format(
        star_name,
        assets.MONTHS[arrival_month],
        scheduled_arrival[1] - 30 * arrival_month,
        scheduled_arrival[0]))


def display_new_star(new_star, stars):
    display_ga()
    say("A NEW STAR SYSTEM HAS BEEN DISCOVERED!  IT IS A CLASS IV\n")
    say("AND ITS NAME IS {}\n\n".format(new_star.name))
    draw_map(stars)


def display_star_class_upgrade(star):
    if star.level in (model.UNDERDEVELOPED,
                      model.DEVELOPED,
                      model.COSMOPOLITAN):
        display_ga()
        say("STAR SYSTEM %s IS NOW A CLASS %s SYSTEM\n" % (
            star.name, assets.text_level(star)))


def display_delay(weeks_delay):
    if weeks_delay < 1:
        return

    if weeks_delay == 1:
        say("LOCAL HOLIDAY SOON\n")
    elif weeks_delay == 2:
        say("CREWMEN DEMAND A VACATION\n")
    elif weeks_delay == 3:
        say("SHIP DOES NOT PASS INSPECTION\n")
    say(" - {:2} WEEK DELAY.\n".format(weeks_delay))


def display_report(game):
    display_ga()
    say("JAN  1, {:4}                                    YEARLY REPORT # {:2}\n"
        .format(game.year, game.year - 2069))

    if game.year <= 2070:
        say(assets.REPORT.format(game.max_weight))

    say("                    CURRENT PRICES\n\n")
    say("NAME  CLASS {}\n".format(assets.GOODS_TITLE))

    for index, star in enumerate(game.stars):
        prices = star.prices
        say("{:4} {:5}  {:+5} {:+5} {:+5} {:+5} {:+5} {:+5}\n".format(
            star.name,
            assets.text_level(star.level),
            prices[0],
            prices[1],
            prices[2],
            prices[3],
            prices[4],
            prices[5]
        ))
        if index % 2 != 0:
            say("\n")

    say("\n('+' MEANS SELLING AND '-' MEANS BUYING)\n")
    say("\n{:22}CAPTAINS\n\n".format(" "))
    say("Name    $ ON SHIPS   $ IN BANK     CARGOES      TOTALS\n")

    for fleet in game.fleets:
        say("\n")

        on_ships = sum([ship.sum for ship in fleet.ships])

        # I admit that the following is a bit weired
        player_ships_goods = [ship.goods for ship in fleet.ships]
        cargoes = sum(sum(cargo[:-1]) * cargo[-1]
                      for cargo in zip(*player_ships_goods, assets.PRICES))

        in_bank = round(fleet.sum)
        totals = on_ships + cargoes + in_bank
        say("  {:2}    {:10}  {:10}  {:10}  {:10}\n".format(
            fleet.name, on_ships, in_bank, cargoes, totals
        ))
