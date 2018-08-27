#!/usr/bin/env python 


COSMOPOLITAN = 15
DEVELOPED = 10
UNDERDEVELOPED = 5
FRONTIER = 0

STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]


class Game:
    """
    Describes a Game object to collect all games data
    """
    def __init__(self, ship_speed=2 / 7, max_distance=15, ship_delay=0.1,
                 number_of_rounds=3, max_weight=30, margin=36, level_inc=1.25,
                 day=1, year=2070, end_year=5, number_of_players=2, half=1,
                 ship=None, ships_per_player=2, number_of_stars=None):

        self.ship_speed = ship_speed
        self.max_distance = max_distance
        self.ship_delay = ship_delay
        self.number_of_rounds = number_of_rounds
        self.max_weight = max_weight
        self.margin = margin
        self.level_inc = level_inc
        self.day = day
        self.year = year
        self.number_of_players = number_of_players
        self.half = half
        self.ship = ship
        self.ships = []
        self.stars = []
        self.accounts = []

        self.end_year = self.year + end_year

        for i in range(ships_per_player * self.number_of_players):
            self.ships.append(Ship(
                goods=[0, 0, 15, 10, 10, 0],
                weight=25,
                day=self.day,
                year=self.year,
                sum=5000,
                star=None,
                status=0,
                player_index=0,
                name=""
            ))

        for i in range(number_of_stars
                       if number_of_stars is not None
                       else 3 * self.number_of_players + 1):
            self.stars.append(Star(
                goods=[0, 0, 0, 0, 0, 0],
                prices=[0, 0, 0, 0, 0, 0],
                prods=[0, 0, 0, 0, 0, 0],  # star's productivity/month
                x=0,
                y=0,
                level=COSMOPOLITAN,
                day=270,
                year=self.year - 1,
                name=STAR_NAMES[0]))

        for i in range(self.number_of_players):
            self.accounts.append(Account(sum=0, day=self.day, year=self.year))


class Ship:
    """
    Describes a ship in the game
    """
    def __init__(self, goods, weight=25, day=1,
                 year=2070, sum=5000, star=None, status=0, player_index=0,
                 name=""):

        self.goods = goods
        self.weight = weight
        self.day = day
        self.year = year
        self.sum = sum
        self.star = star
        self.status = status
        self.player_index = player_index
        self.name = name
        self.speed = 2 / 7

    def add_time(self, days):
        final_days = self.day + days
        years, days = divmod(final_days, 360)

        self.day = days
        self.year += years


class Star:
    """
    Describes a star (world) in the game
    """
    def __init__(self, goods, prices, prods, x, y, level, day, year, name):

        self.goods = goods
        self.prices = prices
        self.prods = prods
        self.x = x
        self.y = y
        self.level = level
        self.day = day
        self.year = year
        self.name = name


class Account:
    def __init__(self, sum, day, year):

        self.sum = sum
        self.day = day
        self.year = year

    def update(self, year, day):
        self.sum = self.sum * (1 + 0.05 * (
            year - self.year + (day - self.day) / 360
        ))

        self.day = day
        self.year = year

