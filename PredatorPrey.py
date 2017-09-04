import random
import sys
random.seed(None)


class Node:

    species = None
    x = None
    y = None
    health = None

    def __init__(self, spec=None):
        if spec is not None:
            self.species = spec
        else:
            self.species = 0
        self.x = None
        self.y = None
        self.health = self.species*2

    def set_location(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    def set_species(self, num):
        if num == 0 or num == 1 or num == 2:
            self.species = num
            if num is 0:  # Blank
                self.health = None
            if num is 1:  # Predator
                self.health = 2
            if num is 2:  # Prey
                self.health = 3
        else:
            sys.stderr.write('Species not correct, do not do math with them.')
            self.species = 0

    def prey_eat(self):
        self.health -= 2
        if self.health <= 0:
            self.species = 1
            self.health = 2

    def prey_reproduce(self):
        self.species = 2
        self.health = 5


class Map:
    height = 100
    width = 100
    play_board = []

    def __init__(self):
        prey = 0
        predator = 0
        empty = 0
        for x in range(self.width):
            row = []
            for y in range(self.height):
                i = random.randint(0, 10)
                if i <= 5:
                    row.append(Node(2))
                    prey += 1
                elif i <= 7:
                    row.append(Node(1))
                    predator += 1
                else:
                    row.append(Node(0))
                    empty += 1

            self.play_board.append(row)
        print('Map created')
        print('Prey: ', prey)
        print('Predator: ', predator)
        print('Empty: ', empty)
        print('Width: ', len(self.play_board))
        print('Height of row 5: ', len(self.play_board[5]))

    def get_board(self):
        return self.play_board

    # TODO find an alternative to nested for loops
    def turn(self):
        pb = self.play_board
        [[self.check_neighbors(x, y, pb[x][y]) for y in range(0, self.height, 1)] for x in range(0, self.width)]

    # Returns the neighbors of a node, If node is on edge this wraps
    def get_neighbors(self, x, y):
        top = self.play_board[x][(y - 1) % self.height]
        tr = self.play_board[(x + 1) % self.width][(y - 1) % self.height]
        right = self.play_board[(x + 1) % self.width][y]
        br = self.play_board[(x + 1) % self.width][(y + 1) % self.height]
        bottom = self.play_board[x][(y + 1) % self.height]
        bl = self.play_board[(x - 1) % self.width][(y + 1) % self.height]
        left = self.play_board[(x - 1) % self.width][y]
        tl = self.play_board[(x - 1) % self.width][(y - 1) % self.height]

        neighbors = [top, tr, right, br, bottom, bl, left, tl]
        return neighbors

    # TODO get accurate Rules and implement
    def check_neighbors(self, x, y, node):
        if node.species is 0:
            # Check for prey for reproduction
            prey = 0
            neighbors = self.get_neighbors(x, y)
            for neigh in neighbors:
                if neigh.species == 2:
                    prey += 1
            if prey >= 2:
                node.prey_reproduce()

        if node.species is 1:
            # Check for prey if no prey reduce health/die
            neighbors = self.get_neighbors(x, y)
            prey = []
            for neigh in neighbors:
                if neigh.species == 2:
                    prey.append(neigh)
            if len(prey) == 0:
                node.health -= 2
            else:
                prey[random.randint(0, (len(prey)-1))].prey_eat()
            if node.health <= 0:
                node.species = 0
            node.health -= 2

        if node.species is 2:
            # Check for overpopulation/health This is prey
            neighbors = self.get_neighbors(x, y)
            prey = []
            open_spots = []
            for neigh in neighbors:
                if neigh.species == 2:
                    prey.append(neigh)
                if neigh.species == 0:
                    open_spots.append(neigh)
            count = len(prey)
            if count == 0 or count >= 6:
                node.health -= 2
                return
            if node.health is None or node.health is 0:
                node.species = 0
                return
            if node.health > 2 and len(open_spots) >= 1:
                open_spots[random.randint(0, (len(open_spots))-1)].prey_reproduce()
                return
            node.health += 1
