#!/usr/bin/env python 

import sys

def say(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()


def get_text():
    while True:
        s = sys.stdin.readline().upper().strip()
        if s != "":
            return s


def get_int():
    try:
        return int(get_text())
    except ValueError:
        return None


def ask(text, checked):
    while True:
        say(text)
        n = get_int()
        if n is not None and checked(n):
            return n


def display_ga():
    say("\n                    *** GENERAL ANNOUNCEMENT ***\n\n")



