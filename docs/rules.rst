##########
Game rules
##########

This page explains the rules behind the game.

Multiplayer
===========
Star Trader is supposed to be a multiplayer game. For this first iteration, it
will be a single player game.

The Star Map
============
The map is 200x200. The original unit was the light year.

Game parameters
===============
min_distance
    The minimum distance between two stars

max_weight
    The max weight of merchandise  a ship can carry.

ships_per_player
    The number of ships per player.

number_of_stars
    The number of stars in the star system. This value may be set by the user as
    a parameter, otherwise it depends on the number of players (3 * number of
    players + 1).

Star system creation
====================

Stars levels
------------
===== ==============
Class Name
===== ==============
I     Cosmopolitan
II    Developed
III   Underdeveloped
IV    Frontier
===== ==============

Star System creation
--------------------
The star system is created as follow:

 * The first star is created at the center of the star system. Its name is SOL
   and its `level I`.
 * Two `level IV` and one `level III` stars are created.
 * If more stars should be created, cycle trough `Frontier`, `Underdeveloped`
   and `developed`.
 * Class IIs appear inside the box 50 ly on a side(x and y from -25 to 25).
 * Class IVs are generated outside this box (between 50 and 100 ly).
 * Class IIIs are sprinkled troughout.

To make the star system *even*, stars are placed one after the other on the top
map (y >= 0), right (x >= 0), bottom (y <= 0) and left (x <= 0) then cycle
again.

If the number of stars is not set by the player, there should be twice the
number of players plus one stars. This mean that for one player, there should be
only 3 stars.

The original code as found on the
`Trade Wars Museum <http://wiki.classictw.com/index.php?title=Star_Trader_Source_Code_1>`_
is the following:

.. code-block:: basic

    1900 REM *** GOSUBS FOLLOW ***
    1910 REM <FRONTIER> GOSUB
    1920 X=(RND(0)-.5)*100
    1930 Y=50*RND(0)
    1940 IF (ABS(X)<25) AND (Y<25) THEN 1920
    1950 F=1
    1960 GOSUB 2190
    1970 IF F=0 THEN 1920
    1980 S[7,S1]=0
    1990 RETURN
    2000 REM *** <UNDERDEVELOPED> GOSUB
    2010 E=100
    2020 GOSUB 2110
    2030 S[7,S1]=5
    2040 RETURN
    2050 REM *** <DEVELOPED> GOSUB
    2060 E=50
    2070 GOSUB 2110
    2080 S[7,S1]=10
    2090 RETURN
    2100 REM *** <GENERATE CO-ORDS> GOSUB
    2110 X=(RND(0)-.5)*E
    2120 Y=RND(0)*E/2
    2130 F=1
    2140 GOSUB 2190
    2150 IF F=0 THEN 2110
    2160 RETURN
    2170 REM *** <TEST STAR CO-ORDS> GOSUB
    2180 REM FIRST CONVERT CO-ORDS TO NEXT HALF-BOARD
    2190 GOTO H OF 2300,2260,2240,2200
    2200 Z=X
    2210 X=-Y
    2220 Y=Z
    2230 GOTO 2300
    2240 Y=-Y
    2250 GOTO 2300
    2260 Z=X
    2270 X=Y
    2280 Y=Z
    2290 REM SECOND, TEST PROXIMITY
    2300 FOR J=1 TO S1-1
    2310 IF SQR((X-S[11,J])^2+(Y-S[12,J])^2) >= D9 THEN 2340
    2320 F=0
    2330 RETURN
    2340 NEXT J
    2350 REM FINALLY, ENTER CO-ORDS AND INCREMENT HALF-BOARD CTR
    2360 S[11,S1]=INT(X)
    2370 S[12,S1]=INT(Y)
    2380 H=1+(H <= 3)*H
    2390 RETURN
