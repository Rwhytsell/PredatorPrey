import random
import sys


class Node:

    def __init__(self):
        self.species = 0
        self.x = None
        self.y = None
        self.health = None

    def set_location(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    def set_species(self, num):
        if num is 0 | 1 | 2:
            self.species = num
            if num is 0:
                self.health = None
            if num is 1:
                self.health = 4
            if num is 2:
                self.health = 3

        else:
            sys.stderr.write('Species not correct, do not do math with them.')
            self.species = 0

    def move(self, direction):
        if direction == 0:
            self.x -= 1
        if direction == 1:
            self.x += 1
        if direction == 2:
            self.y -= 1
        if direction == 3:
            self.y += 1
