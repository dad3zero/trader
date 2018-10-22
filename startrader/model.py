#!/usr/bin/env python 

import random
import math
import enum
import dataclasses


class EvolutionLevel(enum.Enum):
    """
    Work in progress: use enums for levels
    # TODO: test this enum
    """
    COSMOPOLITAN = 15
    DEVELOPED = 10
    UNDERDEVELOPED = 5
    FRONTIER = 0


class Merchandise(enum.Enum):
    UR = "Uranium"
    MET = "Metals"
    GEMS = "Star Gems"
    SOFT = "Computer Software"
    HE = "Heavy Equipment"
    MED = "Medicine"


COSMOPOLITAN = 15
DEVELOPED = 10
UNDERDEVELOPED = 5
FRONTIER = 0

STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]


class StarDate:
    """
    Defines a Star Date for the game.

    The time concept ingame is a similar to the real-world one but simplified.
    So, this class is inspired by the datetime class for date management. In
    game, the time is irrelevant, so we only manage dates.

    The month duration have been unified so each month lasts 30 days. A year
    lasts 12 months.

    The epoch is set to 2070.
    """

    STAR_EPOCH = 2070

    def __init__(self, year=2070, month=1, day=1):
        """
        Creates a date with the standard parameters.

        :param year: year of the date, should be greater than 2070
        :param month: month of the date, should be between 1 and 12
        :param day: day of the date, should be between 1 and 30
        """

        if year < StarDate.STAR_EPOCH:
            raise ValueError(f"year must be after {StarDate.STAR_EPOCH}")

        if not 0 < month <= 12:
            raise ValueError('month must be in 1..12')

        if not 0 < day <= 30:
            raise ValueError('day must be in 1..30')

        self._days =\
            ((year - StarDate.STAR_EPOCH) * 12 + (month - 1)) * 30 + day

    @property
    def year(self):
        """
        The date's year, should be greater than 2070
        :return:
        """
        return self._days // (12 * 30) + StarDate.STAR_EPOCH

    @property
    def month(self):
        """
        The date's month between 1 and 12
        """

        days_in_year = self._days % (12 * 30)
        return days_in_year // 30 + 1

    @property
    def day(self):
        """
        The date's day between 1 and 30
        """
        return self._days % 30

    @property
    def days(self):
        """
        The total number of days fro year 0
        """
        return self._days

    @classmethod
    def for_days(cls, days):
        year, remaining_days = divmod(days, 12 * 30)
        month = remaining_days // 30 + 1
        day = remaining_days % 30
        if day == 0:
            day = 1

        return cls(cls.STAR_EPOCH + year, month, day)

    def __eq__(self, other):
        return self._days == other.days

    def __ne__(self, other):
        return self._days != other.days

    def __lt__(self, other):
        return self._days < other.days

    def __gt__(self, other):
        return self._days > other.days

    def __le__(self, other):
        return self._days <= other.days

    def __ge__(self, other):
        return self._days >= other.days

    def __sub__(self, other):
        """
        If other is another stardate, returns the difference as days. If other
        is an int, returns a new stardate [other] days before.

        :param other: A Stardate or an int
        :return:
        """
        if hasattr(other, "days"):
            return self._days - other.days

        else:
            return StarDate.for_days(self._days - other)

    def __add__(self, other):
        return StarDate.for_days(self._days + other)


class Game:
    """
    Describes a Game object to collect all games data
    """

    def __init__(self, fleets_info, max_distance=15, ship_delay=0.1,
                 number_of_rounds=3, max_weight=30, margin=36, level_inc=1.25,
                 end_year=5, half=1, ships_per_player=2,
                 number_of_stars=None):

        self.max_distance = max_distance
        self.ship_delay = ship_delay
        self.number_of_rounds = number_of_rounds
        self.max_weight = max_weight
        self.margin = margin
        self.level_inc = level_inc
        self.stardate = StarDate()
        self.half = half
        self.ship = None  # reference the active ship
        self.stars = []
        self.fleets = []
        self._ships_per_player = ships_per_player

        self.end_year = self.stardate + end_year

        self.add_star(x=0, y=0, level=COSMOPOLITAN, day=270, year=self.year - 1)
        self.half = 1
        self.add_star(level=FRONTIER, day=270, year=self.year - 1)
        self.add_star(level=FRONTIER, day=270, year=self.year - 1)
        self.add_star(level=UNDERDEVELOPED, day=270, year=self.year - 1)

        for i in range(4,
                       number_of_stars
                       if number_of_stars is not None
                       else 3 * len(fleets_info) + 1):
            level = i % 3 * 5
            self.add_star(level=level, day=270, year=self.year - 1)

        for fleet_captain, fleet_ships in fleets_info:
            self.fleets.append(Fleet(fleet_captain,
                                     fleet_ships,
                                     credit=0,
                                     stardate=self.stardate,
                                     ships_count=ships_per_player,
                                     homeport=self.stars[0]))

    def _get_valid_star_name(self):
        if len(self.stars) == 0:
            name = STAR_NAMES[0]

        else:
            star_names = [star.name for star in self.stars]
            available_star_names = [star
                                    for star in STAR_NAMES
                                    if star not in star_names]
            name = available_star_names[
                round(random.uniform(0, len(available_star_names)))]  # TODO: seem to generate an out of range value

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
            name=self._get_valid_star_name(),
            level=level,
            x=new_x,
            y=new_y,
            stardate=StarDate.for_days(year * 360 + day) if day is not None and year is not None else self.stardate
        )

        self.stars.append(new_star)

        return new_star

    @property
    def year(self):
        return self.stardate.year

    @property
    def day(self):
        return self.stardate.day

    @property
    def ships(self):
        # TODO: Replace list construction with itertools
        return sum([account.ships for account in self.fleets], [])

    @property
    def number_of_players(self):
        return len(self.fleets)


class StarSystem:
    def __init__(self):
        self.stars = []


class Ship:
    """
    Describes a ship in the game

    Ship's stardate represents the date for this ship next action.
    """

    def __init__(self, merchandises, stardate,
                 credit=5000, star=0, status=0, player_index=0,
                 name="", capacity=30):

        self.name = name
        self.speed = 2 / 7  # in clicks/day, 2 clicks per week
        # minimal travel time is 52.5 days with current min distance, max
        # distance on map (283 clicks if 100 x 100) travelled in 990 days
        self.capacity = capacity
        self.sum = credit
        self.flight_reliability = 0.1  # risk for delay, the lower, the better

        self.stardate = stardate
        self.star = star  # TODO: should become the location

        self.merchandises = merchandises
        self.status = status  # TODO: is it really used ?
        self.player_index = player_index

    @property
    def goods(self):
        return self.merchandises

    @property
    def location(self):
        return self.star

    @location.setter
    def location(self, where):
        self.star = where

    @property
    def cargo_weight(self):
        return sum(self.merchandises[:4])

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

        self.star = star
        self.stardate += final_days

        scheduled_arrival = self.stardate, expected_delay

        self._set_arrival_date(7 * extra_delay)
        self.status = extra_delay

        return scheduled_arrival

    def _set_arrival_date(self, days):
        self.stardate += days


class Star:
    """
    Describes a star (world) in the game
    """

    def __init__(self, name, level, x, y, stardate):
        self.name = name
        self.level = level

        self.x = x
        self.y = y

        self.stardate = stardate

        # Following data should move to an economy object
        self.merchandises = [0, 0, 0, 0, 0, 0]
        self.prices = [0, 0, 0, 0, 0, 0]
        self.prods = [0, 0, 0, 0, 0, 0]  # productivity / month

    @property
    def goods(self):
        return self.merchandises

    def level_increment(self, level_increment):
        """
        Compute if the star should level up and updates star level

        :param level_increment:
        :return:
        """
        n = 0
        for i in range(6):
            if self.goods[i] >= 0:
                pass
            elif self.goods[i] < self.prods[i]:
                return False
            else:
                n += 1
        if n > 1:
            return False

        self.level += level_increment
        return True

    def distance_to(self, x, y):
        """

        :param x: x coordinate to the destination
        :param y: y coordinate to the destination
        :return:
        :rtype: int
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


class Product:
    def __init__(self, name, quantity=0, price=0, prods=0):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.prods = prods


@dataclasses.dataclass
class Merchandise:
    product: str
    quantity: int
    unit_weight: int
    buying_price: int
    origin: Star


class Fleet:
    def __init__(self, name, ships_names, credit, stardate, ships_count, homeport):
        """
        A fleet represents the player assets and game features.

        Currently, this is a statefull class which creation is supposed to be
        the start of the game as it initiates  ships.

        :param credit: initial credit
        :param stardate: fleet starting stardate
        :param ships_count: number of ship per player to be created
        :param homeport: Star homeport, new data for game extension
        """
        self.name: str = name
        self.stardate = stardate
        self.sum = credit
        self.ships = []
        self.homeport = homeport

        for ship_name in ships_names:
            self.ships.append(Ship(
                merchandises=[0, 0, 15, 10, 10, 0],
                stardate=self.stardate,
                credit=5000,
                star=self.homeport,
                status=0,
                player_index=0,
                name=ship_name
            ))

    def add_ship(self, name, cargo=[0, 0, 0, 0, 0, 0], cash=0):
        new_ship = Ship(cargo.copy(), self.stardate, cash, self.homeport, 0, 0, name)
        if new_ship in self.ships:
            raise ValueError('Ship cannot exist in duplicate')

        self.ships.append(new_ship)

    @property
    def day(self):
        return self.stardate.day

    @property
    def year(self):
        return self.stardate.year

    def update(self, to_stardate):
        self.sum = self.sum * (1 + 0.05 * (to_stardate - self.stardate) / 360)

        self.stardate = to_stardate
