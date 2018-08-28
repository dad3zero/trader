#!/usr/bin/env python 

import random
import math

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
        self.half = half
        self.ship = ship
        self.ships = []
        self.stars = []
        self.accounts = []
        self._ships_per_player = ships_per_player

        self.end_year = self.year + end_year

        for i in range(ships_per_player * number_of_players):
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
                       else 3 * number_of_players + 1):
            self.stars.append(Star(
                goods=[0, 0, 0, 0, 0, 0],
                prices=[0, 0, 0, 0, 0, 0],
                prods=[0, 0, 0, 0, 0, 0],  # star's productivity/month
                x=0,
                y=0,
                level=COSMOPOLITAN,
                day=270,
                year=self.year - 1,
                name=self._get_valide_star_name() if i == 0 else STAR_NAMES[0]
            ))

        for i in range(number_of_players):
            self.accounts.append(Account(sum=0, day=self.day, year=self.year))

    def _get_valide_star_name(self):
        while True:
            name = STAR_NAMES[1 + round(13 * random.random())]
            for star in self.stars[1:]:
                if name == star.name:
                    break
            else:
                break

        return name

    def _validate_coordinates(self, x, y):
        if self.half == 2:
            x, y, = y, x
        elif self.half == 3:
            y = -y
        elif self.half == 4:
            x, y = -y, x
        self.half += 1
        if self.half > 4:
            self.half = 1

        for star in self.stars:
            if star.distance(x, y) < self.max_distance:
                return tuple()

        return round(x), round(y)

    def add_star(self):
        if len(self.stars) >= 15:
            return

        n = sum([star.level for star in self.stars])
        if n / len(self.stars) < 10:
            return

        while True:
            x = (random.random() - 0.5) * 100
            y = 50 * random.random()
            if abs(x) >= 25 or y >= 25:
                coords = self._validate_coordinates(x, y)
                if coords:
                    new_x, new_y = coords
                    break

        new_star = Star(
            goods=[0, 0, 0, 0, 0, 0],
            prices=[0, 0, 0, 0, 0, 0],
            prods=[0, 0, 0, 0, 0, 0],  # star's productivity/month
            x=new_x,
            y=new_y,
            level=FRONTIER,
            day=self.day,
            year=self.year,
            name=self._get_valide_star_name()
        )

        self.stars.append(new_star)

        return new_star

    @property
    def number_of_players(self):
        return len(self.accounts)

    @property
    def shipz(self):  # TODO should replace current attribute
        return sum([account.ships for account in self.accounts], [])  # TODO: rewrite this with itertools


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
        self.star = star  # TODO: should become the location
        self.status = status
        self.player_index = player_index
        self.name = name
        self.speed = 2 / 7

    @property
    def location(self):
        return self.star

    @location.setter
    def location(self, where):
        self.star = where

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

    def distance_to(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


class Account:
    def __init__(self, sum, day, year):

        self.name: str
        self.sum = sum
        self.day = day
        self.year = year
        self.ships = []

    def update(self, year, day):
        self.sum = self.sum * (1 + 0.05 * (
            year - self.year + (day - self.day) / 360
        ))

        self.day = day
        self.year = year

