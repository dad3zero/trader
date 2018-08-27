# Star Trader by Dave Kaufman, 1974
# Python version by Peter Sovietov, 2017

from __future__ import division
import math
from random import random as rnd

from startrader import model
from startrader import trader_cli as cli


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


INTRO = """
     THE DATE IS JAN 1, 2070 AND INTERSTELLAR FLIGHT
HAS EXISTED FOR 70 YEARS.  THERE ARE SEVERAL STAR
SYSTEMS THAT HAVE BEEN COLONIZED.  SOME ARE ONLY
FRONTIER SYSTEMS, OTHERS ARE OLDER AND MORE DEVELOPED.

     EACH OF YOU IS THE CAPTAIN OF TWO INTERSTELLAR
TRADING SHIPS.  YOU WILL TRAVEL FROM STAR SYSTEM TO
STAR SYSTEM, BUYING AND SELLING MERCHANDISE.  IF YOU
DRIVE A GOOD BARGAIN YOU CAN MAKE LARGE PROFITS.

     AS TIME GOES ON, EACH STAR SYSTEM WILL SLOWLY
GROW, AND ITS NEEDS WILL CHANGE.  A STAR SYSTEM THAT
HOW IS SELLING MUCH URANIUM AND RAW METALS CHEAPLY
MAY NOT HAVE ENOUGH FOR EXPORT IN A FEW YEARS.

     YOUR SHIPS CAN TRAVEL ABOUT TWO LIGHTYEARS IN A
WEEK AND CAN CARRY UP TO %s TONS OF CARGO.  ONLY
CLASS I AND CLASS II STAR SYSTEMS HAVE BANKS ON THEM.
THEY PAY 5%% INTEREST AND ANY MONEY YOU DEPOSIT ON ONE
PLANET IS AVAILABLE ON ANOTHER - PROVIDED THERE'S A LOCAL
BANK.
"""

REPORT = """
STAR SYSTEM CLASSES:
     I  COSMOPOLITAN
    II  DEVELOPED
   III  UNDERDEVELOPED
    IV  FRONTIER

MERCHANDISE:
    UR  URANIUM
   MET  METALS
    HE  HEAVY EQUIPMENT
   MED  MEDICINE
  SOFT  COMPUTER SOFTWARE
  GEMS  STAR GEMS

     EACH TRADING SHIP CAN CARRY MAX %s TONS CARGO.
STAR GEMS AND COMPUTER SOFTWARE, WHICH AREN'T SOLD BY THE
TON, DON'T COUNT.
"""

ADVICE = """
ALL SHIPS START AT SOL
ADVICE;  VISIT THE CLASS III AND IV SYSTEMS -
SOL AND THE CLASS II STARS PRODUCE ALOT OF HE,MED AND
SOFT, WHICH THE POORER STAR SYSTEMS (CLASS III AND
IV) NEED.  ALSO, THE POOR STARS PRODUCE THE RAW GOODS -
UR,MET,GEMS THAT YOU CAN BRING BACK TO SOL AND
THE CLASS II SYSTEMS IN TRADE

STUDY THE MAP AND CURRENT PRICE CHARTS CAREFULLY -
CLASS I AND II STARS MAKE EXCELLENT TRADING PARTNERS
WITH CLASS III OR IV STARS.
"""

STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]

MONTHS = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
    "NOV", "DEC"
]

GOODS_NAMES = ["UR", "MET", "HE", "MED", "SOFT", "GEMS"]
GOODS_TITLE = "%5s %5s %5s %5s %5s %5s" % tuple(GOODS_NAMES)

PRICES = [5000, 3500, 4000, 4500, 3000, 3000]

# *** DATA FOR ECONOMETRIC MODEL FOLLOWS ***
# [k, b], y = k * x + b

ECONOMIC = [
    [[-0.1, 1], [-0.2, 1.5], [-0.1, 0.5]],
    [[0, 0.75], [-0.1, 0.75], [-0.1, 0.75]],
    [[0, -0.75], [0.1, -0.75], [0.1, -0.75]],
    [[-0.1, -0.5], [0.1, -1.5], [0, 0.5]],
    [[0.1, -1], [0.2, -1.5], [0.1, -0.5]],
    [[0.1, 0.5], [-0.1, 1.5], [0, -0.5]]
]


def make_ship(g):
    return model.Ship(
        goods=[0, 0, 15, 10, 10, 0],
        weight=25,
        day=g.day,
        year=g.year,
        sum=5000,
        star=None,
        status=0,
        player_index=0,
        name=""
    )


def make_star(g):
    return model.Star(
        goods=[0, 0, 0, 0, 0, 0],
        prices=[0, 0, 0, 0, 0, 0],
        prods=[0, 0, 0, 0, 0, 0],  # star's productivity/month
        x=0,
        y=0,
        level=model.COSMOPOLITAN,
        day=270,
        year=g.year - 1,
        name=STAR_NAMES[0]
    )


def make_account(g):
    return model.Account(
        sum=0,
        day=g.day,
        year=g.year
    )


def make_objects(g, obj, n):
    return [obj(g) for i in range(n)]


def own_game():
    """
    Defines own game parameters

    :return: tuple  ships_per_player, number_of_stars, game_duration,
    max_weight, min_distance, number_of_rounds, profit_margin
    :rtype tuple:
    """
    ships_per_player = cli.ask("HOW MANY SHIPS PER PLAYER (MAX 12) ",
                           lambda n: 0 < n <= 12)

    number_of_stars = cli.ask("HOW MANY STAR SYSTEMS (FROM 4 TO 13 STARS) ",
                          in_range(4, 13))

    game_duration = cli.ask("ENTER THE LENGTH OF GAME IN YEARS ", lambda n: n > 0)

    max_weight = cli.ask("WHAT'S THE MAX CARGOE TONNAGE(USUALLY 30) ",
                     lambda n: n >= 25)

    cli.say("WHAT'S THE MINIMUM DISTANCE BETWEEN STARS")
    min_distance = cli.ask("(MIN SPACING 10, MAX 25, USUALLY 15) ",
                       in_range(10, 25))

    number_of_rounds = cli.ask("HOW MANY BIDS OR OFFERS(USUALLY 3) ",
                           lambda n: n > 0)

    cli.say("SET THE PROFIT MARGIN(1,2,3,4 OR 5)...THE HIGHER\n")
    cli.say("THE NUMBER, THE LOWER THE PROFIT % ... USUALLY SET TO 2\n")
    profit_margin = cli.ask("...YOUR NUMBER ", in_range(1, 5)) * 18

    return ships_per_player, number_of_stars, game_duration, max_weight, \
           min_distance, number_of_rounds, profit_margin


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


def good_coords(g, index, x, y):
    """
    TEST STAR CO-ORDS
    FIRST CONVERT CO-ORDS TO NEXT HALF-BOARD
    SECOND, TEST PROXIMITY
    FINALLY, ENTER CO-ORDS AND INCREMENT HALF-BOARD CTR


    :param g:
    :param index:
    :param x: x coordinate to test
    :param y: y coordinate to test
    :return:
    """
    if g.half == 2:
        x, y, = y, x
    elif g.half == 3:
        y = -y
    elif g.half == 4:
        x, y = -y, x
    g.half += 1
    if g.half > 4:
        g.half = 1

    for star in g.stars:
        if distance(x, y, star.x, star.y) < g.max_distance:
            return False

    g.stars[index].x = rint(x)
    g.stars[index].y = rint(y)

    return True


def generate_coords(g, index, bounds):
    """
    Generates a coordinate for a star

    :param g:
    :param index:
    :param bounds: max value in the universe (max = 100)
    :return:
    """
    while True:
        x = (rnd() - 0.5) * bounds
        y = rnd() * bounds / 2
        if good_coords(g, index, x, y):
            return


def add_star(game, index, level):
    if level == model.FRONTIER:
        while True:
            x = (rnd() - 0.5) * 100
            y = 50 * rnd()
            if abs(x) >= 25 or y >= 25:
                if good_coords(game, index, x, y):
                    break
    elif level == model.UNDERDEVELOPED:
        generate_coords(game, index, 100)
    elif level == model.DEVELOPED:
        generate_coords(game, index, 50)

    game.stars[index].level = level


def get_valide_star_name(stars):
    # TODO: this function should remove the used names and pick among the remaining ones for better efficiency
    while True:
        name = model.STAR_NAMES[1 + rint(13 * rnd())]
        for star in stars[1:]:
            if name == star.name:
                break
        else:
            break

    return name


def make_stars(game):
    game.half = 1
    add_star(game, 1, model.FRONTIER)
    add_star(game, 2, model.FRONTIER)
    add_star(game, 3, model.UNDERDEVELOPED)
    for i in range(4, len(game.stars)):
        level = i % 3 * 5
        add_star(game, i, level)

    for star in game.stars[1:]:
        star.name = get_valide_star_name(game.stars)


def name_ships(game):
    for p in range(game.number_of_players):
        start = p
        end = start + len(game.ships) // len(game.accounts)

        for index, ship in enumerate(game.ships[start:end]):
            cli.say("   CAPTAIN %d WHAT DO YOU CHRISTEN YOUR SHIP # %s\n" % (
                p + 1, index + 1))
            ship.name = cli.get_text()
            ship.player_index = p
        cli.say("\n")


def ask_for_expert_mode():
    cli.say("HAVE ALL PLAYERS PLAYED BEFORE ")
    if cli.get_text() == "Y":
        cli.say("DO YOU WANT TO SET UP YOUR OWN GAME ")
        if cli.get_text() == "Y":
            return own_game()

    return tuple()


def setup():
    number_of_players = cli.ask("HOW MANY PLAYERS (2,3, OR 4 CAN PLAY) ",
                            in_range(2, 4))

    player_prefs = ask_for_expert_mode()

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

    cli.say("INSTRUCTIONS (TYPE 'Y' OR 'N' PLEASE) ")
    if cli.get_text() == "Y":
        cli.say("%s\n" % (INTRO % game.max_weight))

    make_stars(game)
    name_ships(game)

    return game


def star_map(g):
    cli.say("                      STAR MAP\n")
    cli.say("                    ************\n")
    for y in range(15, -16, -1):
        line = list("                         1                             ")
        if y == 0:
            line = list(
                "1----1----1----1----1----*SOL-1----1----1----1----1    ")
        elif y % 3 == 0:
            line[25] = "-"
        y_hi = y * 10 / 3
        y_lo = (y + 1) * 10 / 3
        for s in range(1, len(g.stars)):
            if g.stars[s].y < y_lo and g.stars[s].y >= y_hi:
                x = rint(25 + g.stars[s].x / 2)
                name = g.stars[s].name
                line[x:x + len(name) + 1] = "*" + name
        cli.say("%s\n" % "".join(line))
    cli.say("\nTHE MAP IS 100 LIGHT-YEARS BY 100 LIGHT-YEARS,\n")
    cli.say("SO THE CROSS-LINES MARK 10 LIGHT-YEAR DISTANCES\n")


def update_prices(g, star):
    """
    M AND C DETERMINE A STAR'S PRODUCTIVITY/MONTH
    PROD/MO. = S(7,J) * M(I,R1)  +  C(I,R1)
    WHERE J IS THE STAR ID #,I THE MERCHANDISE #,
    AND R1 IS THE DEVELOPMENT CLASS OF THE STAR

    :param g:
    :param star:
    :return:
    """
    level = 0
    if star.level >= model.UNDERDEVELOPED:
        level += 1
    if star.level >= model.DEVELOPED:
        level += 1
    months = 12 * (g.year - star.year) + (g.day - star.day) / 30
    goods, prods, prices = star.goods, star.prods, star.prices
    for i in range(6):
        k, b = ECONOMIC[i][level]
        prods[i] = k * star.level + b
        prods[i] *= 1 + star.level / 15
        if abs(prods[i]) > 0.01:
            goods[i] = sgn(prods[i]) * min(abs(prods[i] * 12),
                                           abs(goods[i] + months * prods[i]))
            prices[i] = PRICES[i] * (1 - sgn(goods[i]) * abs(
                goods[i] / (prods[i] * g.margin)))
            prices[i] = 100 * rint(prices[i] / 100 + 0.5)
        else:
            prices[i] = 0
    star.day = g.day
    star.year = g.year


def text_level(g, star):
    level = int(star.level / 5)
    if level == 0:
        return "IV"
    elif level == 1:
        return "III"
    elif level == 2:
        return "II"
    else:
        return "I"


def update_account(game, account):
    """
    Update players accounts

    :param game:
    :param account:
    :return:
    """
    account.update(game.year, game.day)


def price_col(n):
    return "+" + str(n) if n > 0 else str(n)


def report(g):
    cli.display_ga()
    cli.say("JAN  1, %d%s YEARLY REPORT # %d\n" % (
        g.year, " " * 35, g.year - 2069))
    if g.year <= 2070:
        cli.say("%s\n" % (REPORT % g.max_weight))
    cli.say("%sCURRENT PRICES\n\n" % (" " * 20))
    cli.say("NAME  CLASS %s\n" % GOODS_TITLE)
    for i in range(len(g.stars)):
        update_prices(g, g.stars[i])
        prices = g.stars[i].prices
        for j in range(6):
            prices[j] = sgn(g.stars[i].goods[j]) * prices[j]
        cli.say("%4s %5s  %5s %5s %5s %5s %5s %5s\n" % (
            g.stars[i].name,
            text_level(g, g.stars[i]),
            price_col(prices[0]),
            price_col(prices[1]),
            price_col(prices[2]),
            price_col(prices[3]),
            price_col(prices[4]),
            price_col(prices[5])
        ))
        if i % 2 != 0:
            cli.say("\n")
    cli.say("\n('+' MEANS SELLING AND '-' MEANS BUYING)\n")
    cli.say("\n%sCAPTAINS\n\n" % (" " * 22))
    cli.say("NUMBER  $ ON SHIPS   $ IN BANK     CARGOES      TOTALS\n")
    for account in g.accounts:
        update_account(g, account)
    for p in range(g.number_of_players):
        cli.say("\n")
        on_ships = 0
        cargoes = 0
        for ship in g.ships:
            if ship.player_index == p:
                on_ships += ship.sum
                for j in range(6):
                    cargoes += ship.goods[j] * PRICES[j]
        in_bank = rint(g.accounts[p].sum)
        totals = on_ships + cargoes + in_bank
        cli.say("  %2d    %10d  %10d  %10d  %10d\n" % (
            p + 1, on_ships, in_bank, cargoes, totals
        ))


def get_names(objects):
    """
    Utility function to get a list of names from some model objects
    :param objects: A collection of objects with a name attribute
    :return: a list of str which are the names of the elements
    """
    return [o.name for o in objects]


def ship_days(ship, d):
    """
    Set the new time (day and year) on a ship

    :param ship: the ship
    :param d: number of days to add to the ship's date
    :type d: int
    """

    ship.add_time(d)


def travel(g, from_star):
    d = rint(distance(
        from_star.x, from_star.y, g.ship.star.x, g.ship.star.y) / g.ship_speed)
    if rnd() <= g.ship_delay / 2:
        w = 1 + rint(rnd() * 3)
        if w == 1:
            cli.say("LOCAL HOLIDAY SOON\n")
        elif w == 2:
            cli.say("CREWMEN DEMAND A VACATION\n")
        elif w == 3:
            cli.say("SHIP DOES NOT PASS INSPECTION\n")
        cli.say(" - %d WEEK DELAY.\n" % w)
        d += 7 * w
    ship_days(g.ship, d)
    m = int((g.ship.day - 1) / 30)
    cli.say("THE ETA AT %s IS %s %d, %d\n" % (
        g.ship.star.name, MONTHS[m], g.ship.day - 30 * m, g.ship.year))
    d = rint(rnd() * 3) + 1
    if rnd() <= g.ship_delay / 2:
        d = 0
    ship_days(g.ship, 7 * d)
    g.ship.status = d


def next_eta(g):
    targets = get_names(g.stars)
    while True:
        ans = cli.get_text()
        if ans == "MAP":
            star_map(g)
        elif ans == "REPORT":
            report(g)
        elif ans == g.ship.star.name:
            cli.say("CHOOSE A DIFFERENT STAR SYSTEM TO VISIT")
        elif ans in targets:
            from_star = g.ship.star
            g.ship.star = g.stars[get_names(g.stars).index(ans)]
            travel(g, from_star)
            break
        else:
            cli.say("%s IS NOT A STAR NAME IN THIS GAME" % ans)
        cli.say("\n")


def landing(g):
    d, y = g.ships[0].day, g.ships[0].year
    ship_index = 0
    for i in range(1, len(g.ships)):
        if g.ships[i].day > d or g.ships[i].year > y:
            pass
        elif g.ships[i].day == d and rnd() > 0.5:
            pass
        else:
            d, y = g.ships[i].day, g.ships[i].year
            ship_index = i
    g.ship = g.ships[ship_index]
    if g.year < g.ship.year:
        g.day = 1
        g.year = g.ship.year
        report(g)
        if g.year >= g.end_year:
            return False
    g.day = g.ship.day
    m = int((g.day - 1) / 30)
    cli.say("\n%s\n* %s %s, %d\n" % ("*" * 17, MONTHS[m], (g.day - 30 * m), g.year))
    cli.say("* %s HAS LANDED ON %s\n" % (g.ship.name, g.ship.star.name))
    s = g.ship.status + 1
    if s == 2:
        cli.say("1 WEEK LATE - 'OUR COMPUTER MADE A MISTAKE'\n")
    elif s == 3:
        cli.say("2 WEEKS LATE - 'WE GOT LOST.SORRY'\n")
    elif s == 4:
        cli.say("3 WEEKS LATE - PIRATES ATTACKED MIDVOYAGE\n")
    cli.say("\n$ ON BOARD %s   NET WT\n" % GOODS_TITLE)
    cli.say("%10d    %2d    %2d    %2d    %2d    %2d    %2d     %2d\n" % (
        g.ship.sum,
        g.ship.goods[0],
        g.ship.goods[1],
        g.ship.goods[2],
        g.ship.goods[3],
        g.ship.goods[4],
        g.ship.goods[5],
        g.ship.weight
    ))
    return True


def price_window(g, index, units, current_round):
    w = 0.5
    star_units = g.ship.star.goods[index]
    if units < abs(star_units):
        w = units / (2 * abs(star_units))
    return w / (current_round + 1)


def buy_rounds(g, index, units):
    star = g.ship.star
    star_units = rint(star.goods[index])
    if units > 2 * -star_units:
        units = 2 * -star_units
        cli.say("     WE'LL BID ON %d UNITS.\n" % units)
    for r in range(g.number_of_rounds):
        if r != max(g.number_of_rounds - 1, 2):
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
            g.ship.goods[index] -= units
            if index < 4:
                g.ship.weight -= units
            g.ship.sum += price
            star.goods[index] += units
            return
        elif price > (1 + price_window(g, index, units, r)
        ) * star.prices[index] * units:
            break
        else:
            star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
    cli.say("     WE'LL PASS THIS ONE\n")


def buy(g):
    cli.say("\nWE ARE BUYING:\n")
    for i in range(6):
        star_units = rint(g.ship.star.goods[i])
        if star_units < 0 and g.ship.goods[i] > 0:
            cli.say("     %s WE NEED %d UNITS.\n" % (GOODS_NAMES[i], -star_units))
            while True:
                units = cli.ask("HOW MANY ARE YOU SELLING ", lambda n: n >= 0)
                if units == 0:
                    break
                elif units <= g.ship.goods[i]:
                    buy_rounds(g, i, units)
                    break
                else:
                    cli.say("     YOU ONLY HAVE %d" % g.ship.goods[i])
                    cli.say(" UNITS IN YOUR HOLD\n     ")


def sold(g, index, units, price):
    cli.say("     SOLD!\n")
    g.ship.goods[index] += units
    if index < 4:
        g.ship.weight += units
    g.ship.star.goods[index] -= units
    g.ship.sum -= price


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
                sold(game, index, units, price)
                return
            else:
                cli.say("     YOU BID $ %d BUT YOU HAVE ONLY $ %d" % (
                    price, game.ship.sum))
                p = game.ship.player_index
                if star.level >= model.DEVELOPED and game.ship.sum + game.accounts[
                    p].sum >= price:
                    cli.say("     ")
                    bank_call(game)
                    if price <= game.ship.sum:
                        sold(game, index, units, price)
                        return
                break
        elif price < (1 - price_window(game, index, units, r)
        ) * star.prices[index] * units:
            break
        star.prices[index] = 0.8 * star.prices[index] + 0.2 * price / units
    cli.say("     THAT'S TOO LOW\n")


def sell(game):
    cli.say("\nWE ARE SELLING:\n")
    for i in range(6):
        star_units = rint(game.ship.star.goods[i])
        if game.ship.star.prods[i] <= 0 or game.ship.star.goods[i] < 1:
            pass
        elif i <= 3 and game.ship.weight >= game.max_weight:
            pass
        else:
            cli.say("     %s UP TO %d UNITS." % (GOODS_NAMES[i], star_units))
            while True:
                units = cli.ask("HOW MANY ARE YOU BUYING ", in_range(0, star_units))
                if units == 0:
                    break
                elif i > 3 or units + game.ship.weight <= game.max_weight:
                    sell_rounds(game, i, units)
                    break
                else:
                    cli.say("     YOU HAVE %d TONS ABOARD, SO %d" % (
                        game.ship.weight, units))
                    cli.say(" TONS PUTS YOU OVER\n")
                    cli.say("     THE %d TON LIMIT.\n" % game.max_weight)
                    cli.say("     ")


def bank_call(game):
    cli.say("DO YOU WISH TO VISIT THE LOCAL BANK ")
    if cli.get_text() != "Y":
        return
    p = game.ship.player_index
    account = game.accounts[p]
    update_account(game, account)
    cli.say("     YOU HAVE $ %d IN THE BANK\n" % account.sum)
    cli.say("     AND $ %d ON YOUR SHIP\n" % game.ship.sum)
    if account.sum >= 0:
        x = cli.ask("     HOW MUCH DO YOU WISH TO WITHDRAW ",
                in_range(0, account.sum))
        account.sum -= x
        game.ship.sum += x
    x = cli.ask("     HOW MUCH DO YOU WISH TO DEPOSIT ",
                in_range(0, game.ship.sum))
    game.ship.sum -= x
    account.sum += x


def update_class(game, star):
    n = 0
    for i in range(6):
        if star.goods[i] >= 0:
            pass
        elif star.goods[i] < star.prods[i]:
            return False
        else:
            n += 1
    if n > 1:
        return False
    star.level += game.level_inc
    if star.level in (model.UNDERDEVELOPED,
                      model.DEVELOPED,
                      model.COSMOPOLITAN):
        cli.display_ga()
        cli.say("STAR SYSTEM %s IS NOW A CLASS %s SYSTEM\n" % (
            star.name, text_level(game, star)))
    return True


def new_star(game):
    if len(game.stars) >= 15:
        return

    n = sum([star.level for star in game.stars])
    if n / len(game.stars) < 10:
        return

    game.stars.append(make_star(game))
    add_star(game, len(game.stars) - 1, model.FRONTIER)
    game.stars[-1].name = get_valide_star_name(game.stars)
    game.stars[-1].day = game.day
    game.stars[-1].year = game.year

    cli.display_ga()
    cli.say("A NEW STAR SYSTEM HAS BEEN DISCOVERED!  IT IS A CLASS IV\n")
    cli.say("AND ITS NAME IS %s\n\n" % game.stars[-1].name)
    star_map(game)


def start_game(game):
    star_map(game)
    report(game)
    cli.say(ADVICE)
    for ship in game.ships:
        cli.say("\nPLAYER %d, WHICH STAR WILL %s TRAVEL TO " % (
            ship.player_index + 1, ship.name))
        game.ship = ship
        game.ship.star = game.stars[0]
        next_eta(game)
    while landing(game):
        star = game.ship.star
        account = game.accounts[game.ship.player_index]
        update_prices(game, star)
        buy(game)
        sell(game)
        if star.level >= model.DEVELOPED and game.ship.sum + account.sum != 0:
            bank_call(game)
        cli.say("\nWHAT IS YOUR NEXT PORT OF CALL ")
        next_eta(game)
        if update_class(game, star):
            new_star(game)
    cli.display_ga()
    cli.say("GAME OVER\n")


if __name__ == '__main__':
    GAME = setup()
    start_game(GAME)
