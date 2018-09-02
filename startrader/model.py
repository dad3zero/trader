#!/usr/bin/env python 

import random
import math
import enum


class EvolutionLevel(enum.Enum):
    """
    Work in progress: use enums for levels
    # TODO: test this enum
    """
    COSMOPOLITAN = 15
    DEVELOPED = 10
    UNDERDEVELOPED = 5
    FRONTIER = 0


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
                 ships_per_player=2, number_of_stars=None):

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
        self.ship = None
        self.stars = []
        self.fleets = []
        self._ships_per_player = ships_per_player

        self.end_year = self.year + end_year

        for i in range(number_of_players):
            self.fleets.append(Fleet(sum=0,
                                     day=self.day,
                                     year=self.year,
                                     ships=ships_per_player))

        self.add_star(x=0, y=0, level=COSMOPOLITAN, day=270, year=self.year - 1)
        self.half = 1
        self.add_star(level=FRONTIER, day=270, year=self.year - 1)
        self.add_star(level=FRONTIER, day=270, year=self.year - 1)
        self.add_star(level=UNDERDEVELOPED, day=270, year=self.year - 1)

        for i in range(4,
                       number_of_stars
                       if number_of_stars is not None
                       else 3 * number_of_players + 1):
            level = i % 3 * 5
            self.add_star(level=level, day=270, year=self.year - 1)

    def _get_valid_star_name(self):
        if len(self.stars) == 0:
            name = STAR_NAMES[0]

        else:
            star_names = [star.name for star in self.stars]
            available_star_names = [star
                                    for star in STAR_NAMES
                                    if star not in star_names]
            name = available_star_names[
                round(random.uniform(0, len(available_star_names)))]

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
            if star.distance_to(x, y) < self.max_distance:
                return tuple()

        return round(x), round(y)

    def _can_add_star(self):
        if len(self.stars) >= 15:
            return False

        # Currently, this test will fail initialization so it is reported
        # TODO: check how to limit expansion without limiting creation
        # n = sum([star.level for star in self.stars])
        # try:
        #     if n / len(self.stars) < 10:
        #         return False
        # except ZeroDivisionError:
        #     return True

        return True

    def _pick_coordinate(self, level):
        if level == UNDERDEVELOPED:
            bounds = 100
        elif level == DEVELOPED:
            bounds = 50
        elif level == FRONTIER:
            while True:
                x = (random.random() - 0.5) * 100
                y = random.random() * 50
                if abs(x) >= 25 or y >= 25:
                    coords = self._validate_coordinates(x, y)
                    if coords:
                        return x, y

        while True:
            x = (random.random() - 0.5) * bounds
            y = random.random() * bounds / 2
            coords = self._validate_coordinates(x, y)
            if coords:
                return coords

    def add_star(self, x=0, y=0, level=FRONTIER, day=None, year=None):
        if not self._can_add_star():
            return

        if len(self.stars) == 0:
            new_x = 0
            new_y = 0

        elif x != 0 and y != 0 and self._validate_coordinates(x, y):
            new_x = x
            new_y = y

        else:
            new_x, new_y = self._pick_coordinate(level)

        new_star = Star(
            x=new_x,
            y=new_y,
            level=level,
            day=day if day is not None else self.day,
            year=year if year is not None else self.year,
            name=self._get_valid_star_name()
        )

        self.stars.append(new_star)

        return new_star

    @property
    def ships(self):
        # TODO: Replace list construction
        return sum([account.ships for account in self.fleets], [])

    @property
    def number_of_players(self):
        return len(self.fleets)

    @property
    def shipz(self):  # TODO should replace current attribute
        return sum([account.ships for account in self.fleets],
                   [])  # TODO: rewrite this with itertools


class Ship:
    """
    Describes a ship in the game
    """

    def __init__(self, goods, day=1,
                 year=2070, sum=5000, star=0, status=0, player_index=0,
                 name=""):
        self.goods = goods
        self.day = day
        self.year = year
        self.sum = sum
        self.flight_reliability = 0.1  # risk for delay, the lower, the better
        self.star = star  # TODO: should become the location
        self.status = status  # TODO: is it really used ?
        self.player_index = player_index
        self.name = name
        self.speed = 2 / 7

    @property
    def location(self):
        return self.star

    @location.setter
    def location(self, where):
        self.star = where

    @property
    def cargo_weight(self):
        return sum(self.goods[:4])

    def travel_to(self, star, delay_function=lambda x: tuple()):
        """
        Experimental method for a travel.

        :param star: destination star
        :param delay_function: function which should return a delay as a 2
        elements tuple, expected and extra as days.
        :return: the scheduled arrival as a tuple containing the year, days and
        the expected delay which can be 0.
        :rtype: tuple
        """
        travel_time = round(self.star.distance_to(star.x, star.y) / self.speed)

        expected_delay, extra_delay = delay_function(self.flight_reliability)

        travel_time += expected_delay * 7

        final_days = self.day + travel_time
        years, days = divmod(final_days, 360)

        self.star = star
        self.day = days
        self.year += years

        scheduled_arrival = self.year, self.day, expected_delay

        self.set_arrival_date(7 * extra_delay)
        self.status = extra_delay

        return scheduled_arrival

    def set_arrival_date(self, days):
        final_days = self.day + days
        years, days = divmod(final_days, 360)

        self.day = days
        self.year += years


class Star:
    """
    Describes a star (world) in the game
    """

    def __init__(self, x, y, level, day, year, name):
        self.goods = [0, 0, 0, 0, 0, 0]
        self.prices = [0, 0, 0, 0, 0, 0]
        self.prods = [0, 0, 0, 0, 0, 0]  # productivity / month
        self.x = x
        self.y = y
        self.level = level
        self.day = day
        self.year = year
        self.name = name

    def distance_to(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


class Fleet:
    def __init__(self, sum, day, year, ships):
        self.name: str = None
        self.speed = 2 / 7  # TODO: ship speed should be attribut of a ship
        self.sum = sum
        self.day = day
        self.year = year
        self.ships = []

        for i in range(ships):
            self.ships.append(Ship(
                goods=[0, 0, 15, 10, 10, 0],
                day=self.day,
                year=self.year,
                sum=5000,
                star=0,
                status=0,
                player_index=0,
                name=""
            ))

    def update(self, year, day):
        self.sum = self.sum * (1 + 0.05 * (
                year - self.year + (day - self.day) / 360
        ))

        self.day = day
        self.year = year
