#!/usr/bin/env python 


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
        print("DO YOU WANT TO SET UP YOUR OWN GAME ? ")
        if get_text() == "Y":
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
