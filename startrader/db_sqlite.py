#!/usr/bin/env python 

import sqlite3 as sqlite

CREATE_CONFIG = "CREATE TABLE trader_config (" \
                "key TEXT not null constraint config_pk primary key, " \
                "value TEXT);"

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

    def load_config(self):
        """
        Loads the config parameters.
        
        :return:
        """
        pass

    def _create_database(self):
        starsystem = self._connect.cursor()
        starsystem.execute(CREATE_UNIVERSE)

