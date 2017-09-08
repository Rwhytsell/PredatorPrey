import random
import sys
import copy
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
                self.health = 4
        else:
            sys.stderr.write('Species not correct, do not do math with them.')
            self.species = 0

    def move_here(self, species, health):
        if species == 0 or species == 1 or species == 2:
            self.species = species
            if species is 0:  # Blank
                self.health = health
            if species is 1:  # Predator
                self.health = health
            if species is 2:  # Prey
                self.health = health
        else:
            sys.stderr.write('Species not correct, do not do math with them.')
            self.species = 0

    def prey_eat(self):
            self.species = 1

    def prey_reproduce(self):
        self.species = 2
        self.health = 1


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
                if i <= 7:
                    row.append(Node(2))
                    prey += 1
                elif i <= 9:
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

    def turn(self):
        pb = self.play_board
        [[self.check_neighbors(x, y, pb[x][y]) for y in range(0, self.height)] for x in range(0, self.width)]

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

    #
    # PREDATOR AND PREY CELLULAR AUTOMATON
    # The world is grid of cells, with 3 possibilities: Predator(Red, 1), Prey(Green, 2), or Empty(Black, 0).
    # Both predator and prey have a set health, that changes over time.
    # The simulation works in steps, with the following rules:
    #    -For prey:
    #        -Tries to move in a random direction.
    #        -Health increases.
    #        -When health reaches a threshold:
    #           -They will reproduce, creating a new "Prey"
    #            -Their health resets to 1
    #    -For predator:
    #        -Tries to move in a random direction.
    #        -Health decreases.
    #        -When health reaches 0, they die and turn into "Nothing".
    #       -If the adjacent square is a prey:
    #            -They will eat it, turning it into a "predator" (reproducing)
    #            -Their health will increase by the amount of health the eaten prey had
    def check_neighbors(self, x, y, node):
        # If the node is empty no checks are performed
        if node.species is 0:
            return

        if node.species is 1:
            # This is a predator. Check for prey if no prey reduce health/die
            neighbors = self.get_neighbors(x, y)
            prey = []
            open_ = []

            for neigh in neighbors:
                if neigh.species is 2:
                    prey.append(neigh)
                if neigh.species is 0:
                    open_.append(neigh)
            open_length = len(open_)

            if len(prey) is 0:
                if node.health > 0 and open_length > 0:
                    node.health -= 1
                    open_[random.randint(0, (open_length-1))].move_here(1, node.health)
                    node.set_species(0)
                    return

            else:
                target = prey[random.randint(0, (len(prey)-1))]
                if node.health >= target.health:
                    target.prey_eat()

            if node.health is None or node.health <= 0:
                node.species = 0
                return

        if node.species is 2:
            # Check for overpopulation/health This is prey
            neighbors = self.get_neighbors(x, y)
            open_spots = []
            for neigh in neighbors:
                if neigh.species is 0:
                    open_spots.append(neigh)
            count = len(open_spots)
            if count >= 7 or count < 1:
                node.health -= 2
            if node.health is None or node.health is 0:
                node.species = 0
                return
            if node.health > 6 and len(open_spots) >= 1:
                open_spots[random.randint(0, (len(open_spots))-1)].prey_reproduce()
                node.health = 4
                return
            node.health += 1
