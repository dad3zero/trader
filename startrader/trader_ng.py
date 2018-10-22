#!/usr/bin/env python 


def ask(text, checked):
    while True:
        answer = int(input(text))
        if answer is not None and checked(answer):
            return answer


def own_game():
    """
    Defines own game parameters

    :return: tuple  ships_per_player, number_of_stars, game_duration,
    max_weight, min_distance, number_of_rounds, profit_margin
    :rtype tuple:
    """
    ships_per_player = ask("HOW MANY SHIPS PER PLAYER (MAX 12) ",
                           lambda n: 0 < n <= 12)

    number_of_stars = ask("HOW MANY STAR SYSTEMS (FROM 4 TO 13 STARS) ",
                          lambda n: 4 <= n <= 13)

    game_duration = ask("ENTER THE LENGTH OF GAME IN YEARS ", lambda n: n > 0)

    max_weight = ask("WHAT'S THE MAX CARGOE TONNAGE(USUALLY 30) ",
                     lambda n: n >= 25)

    print("WHAT'S THE MINIMUM DISTANCE BETWEEN STARS")
    min_distance = ask("(MIN SPACING 10, MAX 25, USUALLY 15) ",
                       lambda n: 10 <= n <= 25)

    number_of_rounds = ask("HOW MANY BIDS OR OFFERS(USUALLY 3) ",
                           lambda n: n > 0)

    print("SET THE PROFIT MARGIN(1,2,3,4 OR 5)...THE HIGHER\n")
    print("THE NUMBER, THE LOWER THE PROFIT % ... USUALLY SET TO 2\n")
    profit_margin = ask("...YOUR NUMBER ", lambda n: 1 <= n <= 5) * 18

    return ships_per_player, number_of_stars, game_duration, max_weight, \
        min_distance, number_of_rounds, profit_margin


def ask_for_expert_mode():

    game_params = {"ships_per_player": 2,
                   "number_of_stars": 4,
                   "game_duration": 5,
                   "standard_cargo": 30,
                   "max_distance_between_stars": 15,  # 10 to 25
                   "trading_bids": 3,
                   "profit_margin": 5,  # 1 to 5 * 18
                   }

    played = input("HAVE ALL PLAYERS PLAYED BEFORE (Y/n)? ").lower()
    if played == "Y":
        setup_own_game = input("DO YOU WANT TO SET UP YOUR OWN GAME ? ")
        if setup_own_game == "Y":
            return own_game()


def setup_game():
    try:
        number_of_players = int(input("How many players (2 to 4) ?"))
    except ValueError:
        print("Should be a number")
        
    player_prefs = ask_for_expert_mode()


def setup():
    print("Welcome in Star Trader. This is a new game.")
    setup_game()


setup()
