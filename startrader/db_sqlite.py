#!/usr/bin/env python 

import sqlite3 as sqlite

CREATE_CONFIG = "CREATE TABLE trader_config (" \
                "key TEXT not null constraint config_pk primary key, " \
                "value TEXT);"

LOAD_CONFIG = "SELECT key, value FROM trader_config ORDER BY key"
ADD_CONFIG = "INSERT INTO trader_config VALUES (?, ?)"

CREATE_UNIVERSE = "CREATE TABLE IF NOT EXISTS starsystem (" \
                  "name TEXT NOT NULL, " \
                  "coord_x INT NOT NULL, " \
                  "coord_y INT NOT NULL );"


class UniverseDb:
    def __init__(self):
        self._connect = sqlite.connect("trader.db")

    def __del__(self):
        if self._connect:
            self._connect.close()

    def _create_config(self):
        config = self._connect.cursor()
        config.execute(CREATE_CONFIG)
        self._connect.commit()

    def _initiate_config(self):
        default_config = {'min_distance': 15,
                          'number_rounds': 3,
                          'ship_delay': 0.1,
                          'margin': 36,
                          'level_inc': 1.25,
                          'end_year': 5,
                          'half': 1,
                          'ships_per_player': 2,
                          'max_weight': 30}

        for key in default_config:
            self._connect.cursor().execute(ADD_CONFIG, (key,
                                                        default_config[key]))
        self._connect.commit()

    def load_config(self):
        """
        Loads the config parameters.

        :return:
        """
        config = self._connect.cursor()
        try:
            config.execute(LOAD_CONFIG)
            data = config.fetchall()
        except sqlite.OperationalError as e:
            print('got the error')
            if "no such table" in e.args[0]:
                raise ValueError('plop')
            else:
                raise e

    def _create_database(self):
        starsystem = self._connect.cursor()
        starsystem.execute(CREATE_UNIVERSE)

