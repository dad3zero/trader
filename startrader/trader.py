# Star Trader by Dave Kaufman, 1974
# Python version by Peter Sovietov, 2017

from __future__ import division
import math
from random import random as rnd

from startrader import model
from startrader import assets
from startrader import trader_cli as cli
from startrader import trader_economy as eco

in_range = lambda lo, hi: lambda n: lo <= n <= hi


def sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def rint(x):
    return int(round(x))


def distance(x1, y1, x2, y2):
    """
    Provides the 2D distance between 2 coordinates

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def initiate_game(number_of_players, player_prefs):
    """
    Initiate a game object depending on the number of players and parameters

    :param number_of_players:
    :param player_prefs:
    :return:
    """
    if player_prefs:
        ships_per_player, number_of_stars, game_duration, max_weight, \
            min_distance, number_of_rounds, profit_margin = player_prefs

        game = model.Game(number_of_players=number_of_players,
                          ships_per_player=ships_per_player,
                          number_of_stars=number_of_stars,
                          end_year=game_duration,
                          max_weight=max_weight,
                          max_distance=min_distance,
                          number_of_rounds=number_of_rounds,
                          margin=profit_margin)

    else:
        game = model.Game(number_of_players=number_of_players)

    return game


def setup():
    number_of_players, player_prefs = cli.setup_game()

    game = initiate_game(number_of_players, player_prefs)

    cli.say("INSTRUCTIONS (TYPE 'Y' OR 'N' PLEASE) ")
    if cli.get_text() == "Y":
        cli.say(assets.INTRO.format(game.max_weight))

    cli.name_ships(game.fleets)

    return game


def update_prices(stars, to_year, to_day, margin):
    # TODO: should move to economic module
    for star in stars:
        update_star_prices(star, to_year, to_day, margin)


def update_star_prices(star, to_year, to_day, margin):
    # TODO: should move to economic module
    """
    Update the star prices to the game's date.

    M AND C DETERMINE A STAR'S PRODUCTIVITY/MONTH
    PROD/MO. = S(7,J) * M(I,R1)  +  C(I,R1)
    WHERE J IS THE STAR ID #,I THE MERCHANDISE #,
    AND R1 IS THE DEVELOPMENT CLASS OF THE STAR
    """
    level = 0

    if star.level >= model.UNDERDEVELOPED:
        level += 1
    if star.level >= model.DEVELOPED:
        level += 1

    months_diff = 12 * (to_year - star.year) + (to_day - star.day) / 30

    goods, prods, prices = star.goods, star.prods, star.prices

    for i in range(6):
        k, b = eco.ECONOMIC[i][level]
        prods[i] = k * star.level + b
        prods[i] *= 1 + star.level / 15
        if abs(prods[i]) > 0.01:
            goods[i] = sgn(prods[i]) * min(abs(prods[i] * 12),
                                           abs(goods[i] + months_diff * prods[i]))
            prices[i] = assets.PRICES[i] * (1 - sgn(goods[i]) * abs(
                goods[i] / (prods[i] * margin)))
            prices[i] = 100 * rint(prices[i] / 100 + 0.5)
        else:
            prices[i] = 0
    star.day = to_day
    star.year = to_year


def update_account(account, to_year, to_day):
    """
    Update players accounts

    """
    account.update(to_year, to_day)


def display_report(game):
    update_prices(game.stars, game.year, game.day, game.margin)
    for account in game.fleets:
        update_account(account, game.year, game.day)

    cli.display_report(game)


def get_names(collection):
    """
    Utility function to get a list of names from some model objects
    :param collection: A collection of objects with a name attribute
    :return: a list of str which are the names of the elements
    """
    return [element.name for element in collection]


def evaluate_all_delay(ship_reliability):
    """
    Returns a delay between 0 and 4

    :param ship_reliability: threshold for triggering a delay
    :return: an int between 0 and 4
    """
    if rnd() <= ship_reliability / 2:
        weeks_delay = 1 + round(rnd() * 3)
    else:
        weeks_delay = 0

    extra_delay = 0 if rnd() <= ship_reliability / 2 else rint(rnd() * 3) + 1

    return weeks_delay, extra_delay


def next_eta(game):
    """
    Function for user interraction.

    User car either type
    - MAP to display the map
    - REPORT to display the report
    - any planet name to get there.
    :param game:
    :return:
    """
    targets = get_names(game.stars)

    while True:
        answer = cli.get_text()
        if answer == "MAP":
            cli.draw_map(game.stars)

        elif answer == "REPORT":
            display_report(game)  # TODO check maybe not needed to update data

        elif answer == game.ship.star.name:
            cli.say("Already in port, choose another star system to visit")

        elif answer in targets:
            scheduled_arrival = game.ship.travel_to(answer, evaluate_all_delay)
            return answer, scheduled_arrival

        else:
            cli.say("{} is not a valid order.\n"
                    "Please, type MAP, REPORT or a star name".format(answer))
        cli.say("\n")


def get_earliest_ship(ships):
    """
    Extract the next ship to take action. That ship is the one with the earliest
    date. If two ships should take action the same day, they have an equal
    chance to be picked as the first.

    :param ships: A collection of ships
    :return: the next ship to take action
    """
    earliest_ship = ships[0]

    for ship in ships[1:]:
        if ship.year > earliest_ship.year:
            pass
        elif ship.year == earliest_ship.year and ship.day > earliest_ship.day:
            pass
        elif ship.year == earliest_ship.year and ship.day == earliest_ship.day \
                and rnd() > 0.5:
            pass
        else:
            earliest_ship = ship

    return earliest_ship


def landing(game):
    earliest_ship = get_earliest_ship(game.ships)

    game.ship = earliest_ship

    if game.year < earliest_ship.year:
        game.day = 1
        game.year = earliest_ship.year
        display_report(game)
        if game.year >= game.end_year:
            return False

    game.day = earliest_ship.day

    cli.say_arrival_informations(earliest_ship, game.year, game.day)

    return True


def buy_rounds(game, index, units):
    star = game.ship.star
    star_units = rint(star.goods[index])

    if units > 2 * -star_units:
        units = 2 * -star_units
        cli.say("     WE'LL BID ON {} UNITS.\n".format(units))
    for bid_round in range(game.number_of_rounds):
        if bid_round != max(game.number_of_rounds - 1, 2):
            cli.say("     WE OFFER ")
        else:
            cli.say("     OUR FINAL OFFER:")

        cli.say(100 * rint(0.009 * star.prices[index] * units + 0.5))

        price = cli.ask(" WHAT DO YOU BID ", in_range(
            star.prices[index] * units / 10,
            star.prices[index] * units * 10
        ))

        if price <= star.prices[index] * units:
            cli.say("     WE'LL BUY!\n")
            game.ship.goods[index] -= units
            game.ship.sum += price
            star.goods[index] += units
            return

        elif price > (
                1 + eco.price_window(game.ship.star.goods[index], units,
                                     bid_round)
        ) * star.prices[index] * units:
            break

        else:
            star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
    cli.say("     WE'LL PASS THIS ONE\n")


def trade_phase(game):
    cli.say("\nWE ARE BUYING:\n")

    for i in range(6):
        star_units = round(game.ship.star.goods[i])
        if star_units < 0 < game.ship.goods[i]:
            cli.say("     {} WE NEED {} UNITS.\n".format(assets.GOODS_NAMES[i],
                                                         -star_units))
            while True:
                units = cli.ask("HOW MANY ARE YOU SELLING ? ", lambda n: n >= 0)
                if units == 0:
                    break
                elif units <= game.ship.goods[i]:
                    buy_rounds(game, i, units)
                    break
                else:  # Beware, case also for negative values.
                    cli.say("     YOU ONLY HAVE {}  UNITS IN YOUR HOLD\n"
                            .format(game.ship.goods[i]))


def sell_rounds(game, index, units):
    star = game.ship.star
    for r in range(game.number_of_rounds):
        if r != max(game.number_of_rounds - 1, 2):
            cli.say("     WE WANT ABOUT ")
        else:
            cli.say("     OUR FINAL OFFER:")
        cli.say(100 * rint(0.011 * star.prices[index] * units + 0.5))
        price = cli.ask(" YOUR OFFER ", in_range(
            star.prices[index] * units / 10,
            star.prices[index] * units * 10
        ))
        if price >= star.prices[index] * units:
            if price <= game.ship.sum:
                cli.say("     SOLD!\n")
                eco.sold(game.ship, index, units, price)
                return
            else:
                cli.say("     YOU BID $ %d BUT YOU HAVE ONLY $ %d" % (
                    price, game.ship.sum))
                p = game.ship.player_index
                if star.level >= model.DEVELOPED and game.ship.sum + \
                        game.fleets[
                            p].sum >= price:
                    cli.say("     ")
                    bank_call(game)
                    if price <= game.ship.sum:
                        cli.say("     SOLD!\n")
                        eco.sold(game.ship, index, units, price)
                        return
                break
        elif price < (
                1 - eco.price_window(game.ship.star.goods[index], units, r)) * \
                star.prices[index] * units:
            break
        star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
    cli.say("     THAT'S TOO LOW\n")


def sell(game):
    cli.say("\nWE ARE SELLING:\n")
    for i in range(6):
        star_units = rint(game.ship.star.goods[i])
        if game.ship.star.prods[i] <= 0 or game.ship.star.goods[i] < 1:
            pass
        elif i <= 3 and game.ship.cargo_weight >= game.max_weight:  # TODO: fix cargo weight check
            pass
        else:
            cli.say(
                "     %s UP TO %d UNITS." % (assets.GOODS_NAMES[i], star_units))
            while True:
                units = cli.ask("HOW MANY ARE YOU BUYING ",
                                in_range(0, star_units))
                if units == 0:
                    break
                elif i > 3 or units + game.ship.cargo_weight <= game.max_weight:  # TODO: fix cargo weight check
                    sell_rounds(game, i, units)
                    break
                else:
                    cli.say("     YOU HAVE {} TONS ABOARD, SO {}".format(
                        game.ship.cargo_weight, units))
                    cli.say(" TONS PUTS YOU OVER\n")
                    cli.say("     THE {} TON LIMIT.\n".format(game.max_weight))
                    cli.say("     ")


def bank_call(game):
    cli.say("DO YOU WISH TO VISIT THE LOCAL BANK ")
    if cli.get_text() != "Y":
        return

    player = game.ship.player_index
    account = game.fleets[player]
    update_account(account, game.year, game.day)

    cli.say("     YOU HAVE $ {} IN THE BANK\n".format(account.sum))
    cli.say("     AND $ {} ON YOUR SHIP\n".format(game.ship.sum))
    if account.sum >= 0:
        value = cli.ask("     How much do you wish to transfer to ship ",
                    in_range(0, account.sum))
        eco.transfer_credit(account, game.ship, value)

    if game.ship.sum >= 0:
        value = cli.ask("     How much do you wish to collect from your ship ",
                    in_range(0, game.ship.sum))
        eco.transfer_credit(game.ship, account, value)


def run_game(game):
    cli.draw_map(game.stars)
    display_report(game)
    cli.say(assets.ADVICE)

    for ship in game.ships:
        cli.ask_for_destination(game.fleets[ship.player_index].name, ship.name)


def start_game(game):
    cli.draw_map(game.stars)
    display_report(game)
    cli.say(assets.ADVICE)

    for ship in game.ships:
        cli.say("\nCaptain {}, WHICH STAR WILL {} TRAVEL TO ".format(
            game.fleets[ship.player_index].name, ship.name))

        game.ship = ship # TODO: check as looks useless now

        destination, scheduled_arrival = next_eta(game)
        cli.display_eta(destination, scheduled_arrival)

    while landing(game):
        star = game.ship.star
        fleet = game.fleets[game.ship.player_index]
        update_star_prices(star, game.year, game.day, game.margin)
        trade_phase(game)
        sell(game)
        if star.level >= model.DEVELOPED and game.ship.sum + fleet.sum != 0:
            bank_call(game)
        cli.say("\nWHAT IS YOUR NEXT PORT OF CALL ")
        next_eta(game)
        if star.level_increment(game.level_inc):
            cli.display_star_class_upgrade(star)
            new_star = game.add_star()
            if new_star:
                cli.display_new_star(new_star, game.stars)
    cli.display_ga()
    cli.say("GAME OVER\n")


if __name__ == '__main__':
    GAME = setup()
    start_game(GAME)
