import sys
import pygame
import random
from threading import Thread

random.seed(None)
size = width, height = 500, 500
play_width = width/5
play_height = height/5
is_stopped = False

# These are the codes that pygame uses, I am not sure what format it is
black = 0
red = 16386570
blue = 658170
color_arr = [black, red, blue]

pygame.init()
screen = pygame.display.set_mode(size)


def paint(x, y, color_int):
    screen.set_at((x, y), color_arr[color_int])
    screen.set_at((x + 1, y), color_arr[color_int])
    screen.set_at((x, y + 1), color_arr[color_int])
    screen.set_at((x + 1, y + 1), color_arr[color_int])
    screen.set_at((x + 2, y), color_arr[color_int])
    screen.set_at((x, y + 2), color_arr[color_int])
    screen.set_at((x + 2, y + 2), color_arr[color_int])
    screen.set_at((x + 2, y + 1), color_arr[color_int])
    screen.set_at((x + 1, y + 2), color_arr[color_int])


def random_colors(w, h):
    while not is_stopped:
        for x in range(1, w, 5):
            for y in range(1, h, 5):
                color_int = random.randint(1, 2)
                paint(x, y, color_int)

color_thread = Thread(target=random_colors, args=(width, height))
color_thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_stopped = True
            sys.exit(0)
    pygame.display.flip()
