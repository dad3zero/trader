INTRO = """
    The date is Jan 1, 2070 and Interstellar flight has existed for 70 years. There are several Star Systems that have been colonized. Some are only frontier systems, other are older and more developped.

    Each of you is the Cpatain of two Interstellar Trading Ships. You will travel from star system to star system, buying and selling merchandise. If you drive a good bargain, you can make large profits.

    As time goes on, each star system will slowly grow, and its needs will change. A star system that how is selling much uranium and raw metals cheaply may not have enough for export in a few years.
     
    Your ships can travel about two lightyears in a week and can carry up to 30 tons of cargo. Only class I and class II star systems have banks on them. They pay 5 % interest and any money you deposit on one planet is available on another - provided there's a local bank.
"""

REPORT = """
STAR SYSTEM CLASSES:
     I  COSMOPOLITAN
    II  DEVELOPED
   III  UNDERDEVELOPED
    IV  FRONTIER

MERCHANDISE:
    UR  URANIUM
   MET  METALS
    HE  HEAVY EQUIPMENT
   MED  MEDICINE
  SOFT  COMPUTER SOFTWARE
  GEMS  STAR GEMS

     EACH TRADING SHIP CAN CARRY MAX {} TONS CARGO.
STAR GEMS AND COMPUTER SOFTWARE, WHICH AREN'T SOLD BY THE
TON, DON'T COUNT.

"""

ADVICE = """
ALL SHIPS START AT SOL
ADVICE;  VISIT THE CLASS III AND IV SYSTEMS -
SOL AND THE CLASS II STARS PRODUCE ALOT OF HE,MED AND
SOFT, WHICH THE POORER STAR SYSTEMS (CLASS III AND
IV) NEED.  ALSO, THE POOR STARS PRODUCE THE RAW GOODS -
UR,MET,GEMS THAT YOU CAN BRING BACK TO SOL AND
THE CLASS II SYSTEMS IN TRADE

STUDY THE MAP AND CURRENT PRICE CHARTS CAREFULLY -
CLASS I AND II STARS MAKE EXCELLENT TRADING PARTNERS
WITH CLASS III OR IV STARS.
"""

STAR_NAMES = [
    "SOL", "YORK", "BOYD", "IVAN", "REEF", "HOOK", "STAN", "TASK", "SINK",
    "SAND", "QUIN", "GAOL", "KIRK", "KRIS", "FATE"
]

MONTHS = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
    "NOV", "DEC"
]

INSTRUCTIONS = """Captain, enter:
    [MAP] to display the map
    [REPORT] to display the report
    Any Star name to travel to it
What is your choice ?
"""

GOODS_NAMES = ["UR", "MET", "HE", "MED", "SOFT", "GEMS"]
GOODS_TITLE = "{:5} {:5} {:5} {:5} {:5} {:5} ".format(*GOODS_NAMES)
PRICES = [5000, 3500, 4000, 4500, 3000, 3000]


def text_level(level):
    level = int(level / 5)
    if level == 0:
        return "IV"
    elif level == 1:
        return "III"
    elif level == 2:
        return "II"
    else:
        return "I"
