import random
import sys
random.seed(None)


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
            if num is 0: # Blank
                self.health = None
            if num is 1: # Predator
                self.health = 4
            if num is 2: # Prey
                self.health = 5

        else:
            sys.stderr.write('Species not correct, do not do math with them.')
            self.species = 0

    def prey_eaten(self):
        self.species = 2
        self.health = 4

    def prey_reproduce(self):
        self.species = 1
        self.health = 5


class Map:
    height = 100
    width = 100
    play_board = []

    @classmethod
    def __init__(cls):
        for x in range(cls.width):
            row = []
            for y in range(cls.height):
                row.append(Node)
            cls.play_board.append(row)

    # This is the main logic for the Predator-Prey simulation
    def turn(self):
        pb = self.play_board
        for x in range(0, self.width, 1):
            for y in range(0, self.height, 1):
                self.check_neighbors(x, y, pb[x][y])

    # TODO Check to see if node is on the edge of the board and wrap
    def get_neighbors(self, x, y):
        top = self.play_board[x][y - 1]
        tr = self.play_board[x + 1][y - 1]
        right = self.play_board[x + 1][y]
        br = self.play_board[x + 1][y + 1]
        bottom = self.play_board[x][y + 1]
        bl = self.play_board[x - 1][y - 1]
        left = self.play_board[x - 1][y]
        tl = self.play_board[x - 1][y - 1]
        neighbors = [top, tr, right, br, bottom, bl, left, tl]
        return neighbors

    def check_neighbors(self, x, y, node):
        if node.species is 0:
            # Check for prey for reproduction
            prey = 0
            neighbors = self.get_neighbors(x, y)
            for neigh in neighbors:
                if neigh.species == 2:
                    prey += 1
            if prey >= 4:
                node.set_species(2)

        if node.species is 1:
            # Check for prey if no prey reduce health/die
            neighbors = self.get_neighbors(x, y)
            prey = []
            for neigh in neighbors:
                if neigh.species == 2:
                    prey.append(neigh)
            if len(prey) == 0:
                node.health -= 1
            else:
                prey[random.randint(0, len(prey))].prey_eaten()
            if node.health == 0:
                node.species = 0

        if node.species is 2:
            # Check for overpopulation/health
            neighbors = self.get_neighbors(x, y)
            prey = []
            open = []
            for neigh in neighbors:
                if neigh.species == 2:
                    prey.append(neigh)
                if neigh.species == 0:
                    open.append(neigh)
            count = len(prey)
            if count == 0 or count >= 6:
                node.health -= 1
            if node.health > 2 and len(open) >= 1:
                open[random.randint(0, len(open))].prey_reproduce()
