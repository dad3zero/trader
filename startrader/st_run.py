#!/usr/bin/env python 

from typing import Tuple
from startrader import db_sqlite
import pygame
import os
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

planet_images = os.listdir('images')

class StateMachine:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class Scene:
    def __init__(self):
        pass

    def on_update(self):
        pass

    def on_event(self, event):
        pass

    def on_draw(self, screen):
        pass

def drawtitle():
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.SysFont('Arial', 32)
    text = font.render('pyStar Trader', True, white, (0, 0, 0))
    textRect = text.get_rect(left=50, top=50)

    return text, textRect

def draw_name(screen, x, y, name, distance=None):
    font = pygame.font.SysFont('Arial', 20)
    text = font.render(name, True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect(left=x + 24, top=y - 24)
    screen.blit(text, textRect)
    if distance is not None:
        text = pygame.font.SysFont('Arial', 18).render(str(int(distance)), True, (255, 255, 255), (0, 0, 0))
        screen.blit(text,
                    text.get_rect(left=x + 30, top=y - 4))


def get_object_coordinates(object) -> Tuple[int, int]:
    """
    Returns object coordinate in the pygame coordinate system.

    Star Trader uses a positive/negative coordinate system where the center is
    0, 0. Pygame uses a positive coordinate system where 0, 0 is the upper left.
    This function translates the coordinates.

    :param object: any object with x and y attribute where x and y are int
    :return: coordinates in Pygame coordinate system
    """
    x_origin = SCREEN_WIDTH // 2
    y_origin = SCREEN_HEIGHT // 2

    ratio = (min(SCREEN_HEIGHT, SCREEN_WIDTH) // 2) / 100

    return x_origin + object.x * ratio, y_origin + object.y * ratio

def draw_stars(screen, stars):
    """
    Draws a star on a screen object. Strongly coupled to the image size.

    :param screen:
    :param stars:
    """
    for star, image in zip(stars, planet_images):
        planet = pygame.image.load(os.path.join("images",
                                                star.image
                                                if star.image
                                                else image))

        planet_x, planet_y = get_object_coordinates(star)

        screen.blit(planet, (planet_x - 24, planet_y - 24))


def main():
    db = db_sqlite.UniverseDb()
    stars = db.load_starsystem()
    if len(stars) == 0:
        from startrader.creation import starsystem
        print('Star system not created, creating standard one.')
        stars = starsystem.create_starsystem(starsystem.STAR_NAMES)
        db.save_starsystem(stars)

        stars = db.load_starsystem()

    pygame.init()
    pygame.display.set_caption('Minimal program')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))

    print(len(stars))
    draw_stars(screen, stars)
    screen.blit(*drawtitle())

    pygame.display.flip()

    while True:

        screen.fill((0, 0, 0))
        draw_stars(screen, stars)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for star in stars:
            planet_x, planet_y = get_object_coordinates(star)
            if planet_x - 24 < mouse_x < planet_x + 24 and planet_y - 24 < mouse_y < planet_y + 24:
                draw_name(screen, planet_x, planet_y, star.name,
                          None if star.name == "SOL"
                          else star.distance_to(stars[0]))
                current_star = star
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(current_star.name, current_star.distance_to(stars[0]))

        pygame.display.update()

if __name__ == '__main__':
    main()