#!/usr/bin/env python 

import sqlite3 as sqlite
from startrader.creation import starsystem

CREATE_CONFIG = "CREATE TABLE IF NOT EXISTS trader_config (" \
                "key TEXT not null constraint config_pk primary key, " \
                "value TEXT);"

CREATE_UNIVERSE = "CREATE TABLE IF NOT EXISTS starsystem (" \
                  "name TEXT NOT NULL, " \
                  "level TEXT NOT NULL," \
                  "coord_x INT NOT NULL, " \
                  "coord_y INT NOT NULL );"

CREATE_FLEET = "CREATE TABLE IF NOT EXISTS fleet (" \
               "ship_name TEXT NOT NULL, " \
               "location_x INT NOT NULL, " \
               "location_y INT NOT NULL " \
               ")"

LOAD_STARSYSTEM = "SELECT name, level, coord_x, coord_y FROM starsystem"
ADD_STAR = "INSERT INTO starsystem VALUES (?, ?, ?, ?)"

LOAD_CONFIG = "SELECT key, value FROM trader_config ORDER BY key"
ADD_CONFIG = "INSERT INTO trader_config VALUES (?, ?)"


class NoSuchComponentError(Exception):
    pass


class UniverseDb:
    def __init__(self):
        self._connect = sqlite.connect("trader.db")

        self._create_database()
        self._initiate_config()


    def __del__(self):
        if self._connect:
            self._connect.close()

    def _create_database(self):
        """
        Creates the the initial structure of the database.
        """
        c_creation = self._connect.cursor()
        c_creation.execute(CREATE_CONFIG)
        c_creation.execute(CREATE_UNIVERSE)
        c_creation.execute(CREATE_FLEET)

        self._connect.commit()

    def _initiate_config(self):
        """
        Set the initial default data for the config of the game.
        """
        default_config = {'min_distance': 15,
                          'number_rounds': 3,
                          'ship_delay': 0.1,
                          'margin': 36,
                          'level_inc': 1.25,
                          'end_year': 5,
                          'ships_per_player': 2,
                          'max_weight': 30,
                          'star_date': (2070 * 12) * 30 + 1}

        param_cursor = self._connect.cursor()
        try:
            for key in default_config:
                param_cursor.execute(ADD_CONFIG, (key, default_config[key]))
            self._connect.commit()
        except sqlite.IntegrityError:
            self._connect.rollback()

    def load_config(self):
        """
        Loads the config parameters.

        :return: a dictionnary of all of the config keys
        :rtype dict:
        :raise sqlite.OperationalError:
        """
        config = self._connect.cursor()
        try:
            config.execute(LOAD_CONFIG)
            data = config.fetchall()
        except sqlite.OperationalError as e:
            if "no such table" in e.args[0]:
                self._create_config()
                self._initiate_config()
                config.execute(LOAD_CONFIG)
                data = config.fetchall()
            else:
                raise e

        data = dict(data)
        data["star_date"] = starsystem.StarDate.for_days(int(data['star_date']))

        return data

    def load_starsystem(self):
        """
        Loads the star system

        :return: la list of Stars objects
        :rtype list:
        :raises NoSuchComponentError:
        """
        starsystem_data = self._connect.cursor()
        try:
            starsystem_data.execute(LOAD_STARSYSTEM)
            stars = starsystem_data.fetchall()
        except sqlite.OperationalError as e:
            if "no such table" in e.args[0]:
                raise NoSuchComponentError("Starsystem")

        return [starsystem.Star(star[0], star[1], star[2], star[3])
                for star in stars]

    def load_fleet(self, fleet_id):
        fleet_data = self._connect.cursor()
        try:
            pass
        except sqlite.OperationalError as e:
            pass

    def save_starsystem(self, stars: list):
        """
        Save a star system. Data is supposed to be valid prior to this method
        call.

        :param stars: an iterable of Star objects to be saved.
        """
        for star in stars:
            self._connect.cursor().execute(ADD_STAR, (star.name,
                                                      star.level.value,
                                                      star.x,
                                                      star.y))

        self._connect.commit()

