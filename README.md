# Star Trader

As I was looking for a Python implementation of Space Trader, I found this
project originally created by true-grue (Peter Sovietov). As this is not really
*Pythonic*, I choose to fork it.


### Refactoring process
The original code is mostly procedural. Overall, it has a good set of functions
but most of them bear too much responsibilities. Some of them also mix user
interaction and functional behavior. The state of the game is defined in
objects. Unfortunately, in a *generic* kind of objects.

So, the first step was to define real game related objects to define their
responsibilities. Then, every function complexity is reduced. This leads of
course to other functions which sometimes happen to be objects methods.

Functions should then be dispatched on dedicated modules: trader_cli is meant to
contain only user interaction without any game logic. The main should contain
only orchestration functions.

Display is updated to the `format()` method which simplifies the display, making
no use of some tweaks.  

### Original readme  

The following is taken from the original readme.

The original game was written by Dave Kaufman in BASIC and information about the game was published in "People's Computer Company" newsletter in 1974.
Here is a Python version of the game (work in progress, there could still be bugs!).

![Star Trader screenshot](star_trader.png)

The game code was printed in 1975, in the wonderful book [What to Do After You Hit Return](https://archive.org/details/Whattodoafteryouhitreturn).
I think this book still has a huge education potential.
BASIC games from the book like "Star Trader" are quite complex.
They use lots of processes/algorithms/rules instead of data (graphics, audio, text -- it was a game designer Chris Crawford, who introduced the concept of process intensity in the games).
Still, it's possible with the help of the book to understand how "Star Trader" works and how to make your own, better version of the game.

Wouldn't it be great to see someday modern version of "What to Do After You Hit Return" with Python (or Lua, or ...) code?

