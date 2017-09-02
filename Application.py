import sys
import pygame
import random
from threading import Thread
import PredatorPrey

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
pp = PredatorPrey.Map()


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


# TODO numpy matrix's
def map_to_pixel(pp_map):
    pixel_map = [[0 for x in range(100)] for y in range(100)]
    for x in range(1, 100, 1):
        for y in range(1, 100, 1):
            print('X: ', x, end='')
            print(' Y: ', y)
            if pp_map[x][y].species == 0:
                pixel_map[x][y] = 0
            elif pp_map[x][y].species == 1:
                pixel_map[x][y] = 1
            else:
                pixel_map[x][y] = 2
    return pixel_map


def random_colors(w, h):
    ra = random.randint
    pa = paint
    while not is_stopped:
        for x in range(1, w, 5):
            for y in range(1, h, 5):
                color_int = ra(1, 2)
                pa(x, y, color_int)


def paint_map(board):
    map_arr = map_to_pixel(board)
    pa = paint
    length = len(map_arr)
    for x in range(length):
        for y in range(x):
            pa(x, y, map_arr[x][y])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_stopped = True
            sys.exit(0)
    paint_map(pp.get_board())
    pygame.display.flip()
    random_colors(width, height)
