"""
Star system creation tools
"""

from typing import List
import random
import enum


class StarLevel(enum.Enum):
    COSMOPOLITAN = 1
    DEVELOPED = 2
    UNDERDEVELOPED = 3
    FRONTIER = 4


class Star:
    """
    Star object in the universe. Once set, the object cannot be moved to
    another coordinate.
    """
    def __init__(self, name: str, level: StarLevel, x: int, y: int):
        self.name = name
        self._x = int(x)
        self._y = int(y)
        self.level = level

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


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
            (year * 12 + (month - 1)) * 30 + day

    @property
    def year(self):
        """
        The date's year, should be greater than 2070
        :return:
        """
        return self._days // (12 * 30)

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

        return cls(year, month, day)

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


STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]


def create_starsystem(star_names: List[str], number_of_stars=4):
    """
    Prototype fonction for star system creation.

    :param star_names: a list of names to use as star names.
    :param number_of_stars: number of stars to create
    :return: a list of stars.
    """
    stars = []

    stars.append(Star(star_names[0], StarLevel.COSMOPOLITAN,
                      *get_sol_coordinates()))
    stars.append(Star(get_valid_starname([star.name for star in stars],
                                         star_names),
                      StarLevel.FRONTIER,
                      *get_frontier_class_coordinates()))
    stars.append(Star(get_valid_starname([star.name for star in stars],
                                         star_names),
                      StarLevel.FRONTIER,
                      *get_frontier_class_coordinates()))
    stars.append(Star(get_valid_starname([star.name for star in stars],
                                         star_names),
                      StarLevel.UNDERDEVELOPED,
                      *get_underdeveloped_class_coordinates()))

    return stars


def get_sol_coordinates():
    """
    Create coordinates for SOL which should be the central star.
    :return: a tuple of coordinates
    """
    return 0, 0


def get_developed_class_coordinates():
    """
    Creates a new class II star coordinates. A class II star appears in the
    central 50 ly box.
    :return: a tuple of coordinates with values from -25 to 25
    """
    x = round(random.random() * 50) - 25
    y = round(random.random() * 50) - 25

    return x, y


def get_underdeveloped_class_coordinates():
    """
    Creates a new class III star coordinates. A class III star appears anywhere.
    :return: a tuple of coordinates with values from -50 to 50
    """
    x = round(random.random() * 100) - 50
    y = round(random.random() * 100) - 50

    return x, y


def get_frontier_class_coordinates():
    """
    Creates a new class IV star coordinates. A class IV star appears outside of
    the central 50 ly box.
    :return: a tuple of coordinates with values from -50 to -25 or 25 to 50.
    """
    x = random.random()
    x = round((x if x > 0.5 else x - 1) * 50)

    y = random.random()
    y = round(( y if y > 0.5 else y - 1) * 50)

    return x, y


def get_valid_starname(current_star_names: List[str],
                       all_star_names: List[str]):
    """
    Extract a random value from second list if not in first one.

    :param current_star_names: The list of current star's names
    :param all_star_names: The list of all available names
    :return: a name from the second list
    """
    available_star_names = [star
                            for star in all_star_names
                            if star not in current_star_names]

    name = available_star_names[
        int(random.uniform(0, len(
            available_star_names)))]

    return name

