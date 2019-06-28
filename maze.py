import sys
import pygame
import random
from knapsack import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (169, 169, 169)
YELLOW = (222, 178, 0)
PINK = (225, 96, 253)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 99, 71)
GRAY = (119, 136, 153)
LIGHTORANGE = (255, 176, 56)
INTERMEDIARYORANGE = (255, 154, 0)
LIGHTBLUE = (60, 170, 255)
DARKBLUE = (0, 101, 178)
BEIGE = (178, 168, 152)

BORDER_THICKNESS = 1.0

HEIGHT_TOTAL = 700
WIDTH_TOTAL = 1200
WIDTH = 675
HEIGHT = 675
SCREEN_SIZE = (WIDTH_TOTAL, HEIGHT_TOTAL)

FONTSIZE_START = 50
FONTSIZE_COMMANDS_INTIAL = 30
FONTSIZE_MAZE = 20

SIZE = 45

BACKPACK = pygame.transform.scale(pygame.image.load('images/backpack.png'), (2 * SIZE, 2 * SIZE))

GOLD = pygame.transform.scale(pygame.image.load('images/gold.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))
RING = pygame.transform.scale(pygame.image.load('images/ring.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))
CLOCK = pygame.transform.scale(pygame.image.load('images/clock.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))
SHOES = pygame.transform.scale(pygame.image.load('images/shoes.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))
BELT = pygame.transform.scale(pygame.image.load('images/belt.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))
BATTERY = pygame.transform.scale(pygame.image.load('images/battery.png'), (int(SIZE - 2 * BORDER_THICKNESS), int(SIZE - 2 * BORDER_THICKNESS)))

IMAGES = {'Gold': GOLD, 'Ring': RING, 'Clock': CLOCK, 'Shoes': SHOES, 'Belt': BELT, 'Battery': BATTERY}
IMAGES_NAME = ['Gold', 'Ring', 'Clock', 'Shoes', 'Belt', 'Battery']

def text(background, message, color, size, coordinate_x, coordinate_y):
    font = pygame.font.SysFont(None, size)
    txt = font.render(message, True, color)
    background.blit(txt, [coordinate_x, coordinate_y])


class Item():
    def __init__(self, weight, value, name, image, pos_x, pos_y):
        self.weight = weight
        self.value = value

        self.name = name
        self.image = image

        self.pos_x = pos_x * SIZE + BORDER_THICKNESS
        self.pos_y = pos_y * SIZE + BORDER_THICKNESS

        self.matrix_pos_x = pos_x
        self.matrix_pos_y = pos_y

        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS

    def render(self, background):
        background.blit(self.image, self.image.get_rect().move((self.pos_x, self.pos_y)))


class Knapsack():
    def __init__(self, avaliable, pos_x, pos_y):
        self.items = []
        self.avaliable = avaliable
        self.value = 0

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS

    def render(self, background):
        # renderizar mochila na parte direita
        background.blit(BACKPACK, BACKPACK.get_rect().move((self.pos_x, self.pos_y)))
        temp_pos_x = self.pos_x + 2 * SIZE + 5
        for item in self.items:
            item.pos_y = self.pos_y
            item.pos_x = temp_pos_x + 5
            temp_pos_x += SIZE + 10
            item.render(background)


class NodeBorder():
    def __init__(self, pos_x, pos_y, width, height):
        self.color = BLACK
        self.thickness = BORDER_THICKNESS

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = width
        self.height = height

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])


class Node():
    def __init__(self, pos_x, pos_y):
        self.color = BROWN

        self.id = None
        self.visited = False
        self.explored = False

        self.matrix_pos_x = 0
        self.matrix_pos_y = 0

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = SIZE
        self.height = SIZE
        
        self.neighbors_not_visited = []
        self.neighbors_connected = []
        self.parent = None

        self.top_border = NodeBorder(self.pos_x, self.pos_y, SIZE, BORDER_THICKNESS)
        self.bottom_border = NodeBorder(self.pos_x, self.pos_y + SIZE - BORDER_THICKNESS, SIZE, BORDER_THICKNESS)
        self.right_border = NodeBorder(self.pos_x + SIZE - BORDER_THICKNESS, self.pos_y, BORDER_THICKNESS, SIZE)
        self.left_border = NodeBorder(self.pos_x, self.pos_y, BORDER_THICKNESS, SIZE)

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])

        self.top_border.render(background)
        self.bottom_border.render(background)
        self.right_border.render(background)
        self.left_border.render(background)


class Maze():
    def __init__(self, final_x, final_y):
        self.maze = []
        self.total_nodes = 0
        self.maze_created = False
        self.final_coordinate_x = final_x
        self.final_coordinate_y = final_y

        self.items = []
        self.items_algorithm = []
        self.weights = []
        self.values = []
        self.names = []

        self.knapsack = Knapsack(random.randint(15, 30), 678, 480)

        self.images_name = IMAGES_NAME.copy()

        self.initialize_maze()
        self.define_initial_neighbors_not_visited()

        self.generate_items()

    def initialize_maze(self):
        x = 0
        y = 0
        for i in range(0, WIDTH, SIZE):
            self.maze.append([])
            for j in range(0, HEIGHT, SIZE):
                self.maze[x].append(Node(i, j))
                self.total_nodes += 1
                y += 1
            x += 1

    def generate_items(self):
        positions = []
        positions.append((self.final_coordinate_x, self.final_coordinate_y))

        for i in range(6):
            weight = random.randint(2, 15)
            value = random.randint(5, 50)

            pos_x = random.randint(0, int(WIDTH / SIZE) - 1)
            pos_y = random.randint(0, int(WIDTH / SIZE) - 1)
            while (pos_x, pos_y) in positions:
                pos_x = random.randint(0, int(WIDTH / SIZE) - 1)
                pos_y = random.randint(0, int(WIDTH / SIZE) - 1)
            positions.append((pos_x, pos_y))

            random.shuffle(self.images_name)
            name = self.images_name.pop()
            image = IMAGES[name]
            item = Item(weight, value, name, image, pos_x, pos_y)
            self.items.append(item)
            self.weights.append(item.weight)
            self.values.append(item.value)
            self.names.append(item.name)

        self.items_algorithm = self.items.copy()

    def add_edge(self, node, neighbor):
        neighbor.neighbors_connected.append(node)
        node.neighbors_connected.append(neighbor)

    def remove_neighbors_visited(self):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].neighbors_not_visited = [x for x in self.maze[i][j].neighbors_not_visited if not x.visited]

    def define_initial_neighbors_not_visited(self):
        id = 0
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].matrix_pos_x = i
                self.maze[i][j].matrix_pos_y = j

                id += 1
                self.maze[i][j].id = id

                if (i > 0 and j > 0 and i < int(HEIGHT / SIZE) - 1 and j < int(HEIGHT / SIZE) - 1):
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left
                elif i == 0 and j == 0:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == 0:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                elif i == 0 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                elif (i == int(HEIGHT / SIZE) - 1 and j == int(WIDTH / SIZE) - 1):
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                elif j == 0:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                elif i == 0:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left
                elif i == int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left
                elif j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(self.maze[i][j - 1])  # left

    def break_border(self, node, neightbor, color):
        # right
        if (neightbor.matrix_pos_x == node.matrix_pos_x + 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.right_border.color = color
            neightbor.left_border.color = color
        # left
        elif (neightbor.matrix_pos_x == node.matrix_pos_x - 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.left_border.color = color
            neightbor.right_border.color = color
        # bot
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y + 1):
            node.bottom_border.color = color
            neightbor.top_border.color = color
        # top
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y - 1):
            node.top_border.color = color
            neightbor.bottom_border.color = color

    def dfs(self, background):
        current_cell = random.choice(random.choice(self.maze))
        current_cell.visited = True
        current_cell.color = DARKBLUE
        stack = [current_cell]
        visited_cells = 1

        while visited_cells != self.total_nodes or len(stack) != 0:
            self.remove_neighbors_visited()
            if len(current_cell.neighbors_not_visited) > 0:
                random_neighbor = random.choice(
                    current_cell.neighbors_not_visited)

                self.break_border(current_cell, random_neighbor, DARKBLUE)

                self.add_edge(current_cell, random_neighbor)
                current_cell = random_neighbor
                stack.append(current_cell)
                current_cell.visited = True
                current_cell.color = DARKBLUE
                visited_cells += 1
            else:
                current_cell.color = INTERMEDIARYORANGE

                if current_cell.top_border.color == DARKBLUE:
                    current_cell.top_border.color = INTERMEDIARYORANGE
                if current_cell.bottom_border.color == DARKBLUE:
                    current_cell.bottom_border.color = INTERMEDIARYORANGE
                if current_cell.right_border.color == DARKBLUE:
                    current_cell.right_border.color = INTERMEDIARYORANGE
                if current_cell.left_border.color == DARKBLUE:
                    current_cell.left_border.color = INTERMEDIARYORANGE

                if len(stack) == 1:
                    stack.pop()
                else:
                    stack.pop()
                    current_cell = stack[-1]
            self.render(background)
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 700, 20)
            pygame.display.update()
        self.maze_created = True

    def prim(self, background):
        initial_cell = random.choice(random.choice(self.maze))
        initial_cell.visited = True
        initial_cell.color = INTERMEDIARYORANGE

        without_neighbors_visited = [initial_cell]
        visited_cells_number = 1

        while visited_cells_number != self.total_nodes:
            self.remove_neighbors_visited()
            # filtra a lista de celulas com vizinhos não visitados
            without_neighbors_visited = [x for x in without_neighbors_visited if len(x.neighbors_not_visited) > 0]
            current_cell = random.choice(without_neighbors_visited)

            if len(current_cell.neighbors_not_visited) > 0:
                for cell_visited in without_neighbors_visited:
                    for cell in cell_visited.neighbors_not_visited:
                        cell.color = DARKBLUE

                random_neighbor = random.choice(current_cell.neighbors_not_visited)

                self.break_border(current_cell, random_neighbor, INTERMEDIARYORANGE)

                self.add_edge(current_cell, random_neighbor)

                random_neighbor.visited = True
                random_neighbor.color = INTERMEDIARYORANGE

                if len(random_neighbor.neighbors_not_visited) > 0:
                    without_neighbors_visited.append(random_neighbor)

                visited_cells_number += 1

            self.render(background)
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 700, 20)
            pygame.display.update()
        self.maze_created = True

    def kruskal(self, background):
        equals_id = False
        while not equals_id:
            # verifica se todas as celulas pertencem ao mesmo conjunto
            ids = set()
            for i in range(0, int(HEIGHT / SIZE)):
                for j in range(0, int(WIDTH / SIZE)):
                    ids.add(self.maze[i][j].id)
            if (len(ids) == 1):
                equals_id = True

            current_cell = random.choice(random.choice(self.maze))
            random_neighbor = random.choice(current_cell.neighbors_not_visited)

            if random_neighbor.id != current_cell.id:
                current_cell.color = INTERMEDIARYORANGE
                self.break_border(current_cell, random_neighbor, INTERMEDIARYORANGE)
                self.add_edge(current_cell, random_neighbor)
                random_neighbor.color = INTERMEDIARYORANGE
                id_neighbor = random_neighbor.id

                for i in range(0, int(HEIGHT / SIZE)):
                    for j in range(0, int(WIDTH / SIZE)):
                        if self.maze[i][j].id == id_neighbor:
                            self.maze[i][j].id = current_cell.id

            self.render(background)
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 700, 20)
            pygame.display.update()
        self.maze_created = True

    def take_item(self, item):
        self.items.remove(item)
        self.knapsack.items.append(item)
        self.knapsack.avaliable -= item.weight
        self.knapsack.value += item.value

    def render(self, background):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)

        if self.maze_created:
            self.maze[self.final_coordinate_x][self.final_coordinate_y].color = LIGHTBLUE

            for item in self.items:
                item.render(background)

            self.knapsack.render(background)


class Player():
    def __init__(self, initial_x, initial_y):
        self.pos_x = initial_x * SIZE + BORDER_THICKNESS
        self.pos_y = initial_y * SIZE + BORDER_THICKNESS

        self.matrix_pos_x = initial_x
        self.matrix_pos_y = initial_y

        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS

        self.color = RED

    def update(self, maze, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and self.pos_x > BORDER_THICKNESS and (maze[self.matrix_pos_x][self.matrix_pos_y].left_border.color is not BLACK)):
                    self.pos_x -= SIZE
                    self.matrix_pos_x -= 1

                if (event.key == pygame.K_RIGHT and self.pos_x + BORDER_THICKNESS < WIDTH - SIZE and (maze[self.matrix_pos_x][self.matrix_pos_y].right_border.color is not BLACK)):
                    self.pos_x += SIZE
                    self.matrix_pos_x += 1

                if (event.key == pygame.K_UP and self.pos_y > BORDER_THICKNESS and (maze[self.matrix_pos_x][self.matrix_pos_y].top_border.color is not BLACK)):
                    self.pos_y -= SIZE
                    self.matrix_pos_y -= 1

                if (event.key == pygame.K_DOWN and self.pos_y + BORDER_THICKNESS < HEIGHT - SIZE and (maze[self.matrix_pos_x][ self.matrix_pos_y].bottom_border.color is not BLACK)):
                    self.pos_y += SIZE
                    self.matrix_pos_y += 1

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])


class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.start = False
        self.winner = False
        self.exit = False

        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Knapsack Maze')

        self.final_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.final_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)

        self.maze = Maze(self.final_coordinate_x, self.final_coordinate_y)
        self.player = Player(self.final_coordinate_x, self.final_coordinate_y)

        self.initial_avaliable = self.maze.knapsack.avaliable

        self.matrix, self.max_value = knapsack_iterative(self.maze.knapsack.avaliable, self.maze.weights, self.maze.values)
        self.items_taken = find_solution(self.matrix, self.maze.weights, self.maze.knapsack.avaliable)

        self.items_taken_names = []
        for item in self.items_taken:
            self.items_taken_names.append(self.maze.names[item - 1])

    def update(self, event):
        if not self.winner:
            self.player.update(self.maze.maze, event)

    def initial_game(self):
        self.background.fill(DARKBLUE)
        pygame.draw.rect(self.background, RED, [50, 40, 1000, 580])
        pygame.draw.rect(self.background, LIGHTBLUE, [50, 100, 1000, 450])
        pygame.draw.rect(self.background, BLACK, [120, 150, 850, 380])
        pygame.draw.rect(self.background, DARKBLUE, [120, 150, 850, 100])
        text(self.background, "KNAPSACK MAZE", ORANGE, FONTSIZE_START, 410, 185)
        text(self.background, "PRESS (ESC) TO CLOSE GAME", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 410, 480)
        pygame.display.update()
        pygame.time.wait(250)
        text(self.background, "PRESS (D) TO START GAME (DFS)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 400, 330)
        text(self.background, "PRESS (P) TO START GAME (PRIM'S)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 390, 370)
        text(self.background, "PRESS (K) TO START GAME (KRUSKAL)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 380, 410)
        pygame.display.update()
        pygame.time.wait(250)

    def render(self):
        self.background.fill(BLACK)
        
        self.maze.render(self.background)

        self.player.render(self.background)

        if not self.winner:
            text(self.background, "You are a bounty hunter, who earns his living by searching for valuable items", WHITE, FONTSIZE_MAZE, 678, 10)
            text(self.background, "in the legendary MAZE ADVENTURES and selling them at PAWNSHOP, located just", WHITE, FONTSIZE_MAZE, 678, 25)
            text(self.background, "outside the maze. However, you are very fond of your DORA THE EXPLORER", WHITE, FONTSIZE_MAZE, 678, 40)
            text(self.background, "backpack and you never carry more weight than it takes, otherwise you", WHITE, FONTSIZE_MAZE, 678, 55)
            text(self.background, "risk ruining it. Your challenge then is to always choose the best", WHITE, FONTSIZE_MAZE, 678, 70)
            text(self.background, "combinations of items trying to earn as much money as possible but", WHITE, FONTSIZE_MAZE, 678, 85)
            text(self.background, "without carrying too much weight and end up ripping your beatiful backpack.", WHITE, FONTSIZE_MAZE, 678, 100)

            x = 678
            y = 120
            for item in self.maze.items_algorithm:
                self.background.blit(item.image, item.image.get_rect().move((x, y)))
                text(self.background, "Value: " + str(item.value) + "$", WHITE, FONTSIZE_MAZE + 5, x + SIZE + 20, y + 15)
                text(self.background, "Weight: " + str(item.weight) + "KG", WHITE, FONTSIZE_MAZE + 5, x + SIZE + 170, y + 15)
                y += SIZE + 5

            pygame.draw.rect(self.background, RED, [1050, 120, SIZE, SIZE])
            text(self.background, "- PLAYER", WHITE, FONTSIZE_MAZE, 1050 + SIZE + 3, 120 + 10)
            pygame.draw.rect(self.background, LIGHTBLUE, [1050, 120 + SIZE + 2, SIZE, SIZE])
            text(self.background, "- MARKET", WHITE, FONTSIZE_MAZE, 1050 + SIZE + 3, 120 + SIZE + 1 + 10)

            text(self.background, "PRESS (T) IN ITEM TO TAKE", WHITE, FONTSIZE_MAZE, 678, 580)
            text(self.background, "PRESS (F) IN GOAL TO DELIVER ITEMS", WHITE, FONTSIZE_MAZE, 678, 600)
            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 678, 620)
            text(self.background, "PRESS (Q) TO GIVE UP", WHITE, FONTSIZE_MAZE, 678, 640)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 678, 660)

            text(self.background, "KNAPSACK AVAILABLE: " + str(self.maze.knapsack.avaliable) + "KG OF " + str(self.initial_avaliable) + "KG", WHITE, FONTSIZE_MAZE + 10, 678, 430)
            text(self.background, "KNAPSACK VALUE: " + str(self.maze.knapsack.value) + "$", WHITE, FONTSIZE_MAZE + 10, 678, 450)

        elif self.winner:
            text(self.background, "BETTER ITEMS TO CAUGHT: " + str(self.items_taken_names), WHITE, FONTSIZE_MAZE, 678, 580)
            text(self.background, "MAXIMUM VALUE: " + str(self.max_value) + "$", WHITE, FONTSIZE_MAZE, 678, 620)

            x = 678
            y = 120
            for item in self.maze.items_algorithm:
                self.background.blit(item.image, item.image.get_rect().move((x, y)))
                text(self.background, "Value: " + str(item.value) + "$", WHITE, FONTSIZE_MAZE + 5, x + SIZE + 20, y + 15)
                text(self.background, "Weight: " + str(item.weight) + "KG", WHITE, FONTSIZE_MAZE + 5, x + SIZE + 170, y + 15)
                y += SIZE + 5
            
            if self.maze.knapsack.value == self.max_value:

                text(self.background, "YOU WIN", BLUE, FONTSIZE_MAZE + 15, 970, 640)
                text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE + 8, 910, 660)
                text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE + 8, 890, 680)
            else:
                text(self.background, "YOU LOSE", RED, FONTSIZE_MAZE + 15, 965, 640)
                text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE + 8, 910, 660)
                text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE + 8, 890, 680)

        pygame.display.update()

    def run(self):
        while not self.start:
            self.initial_game()
            pygame.display.update()
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[
                    pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.dfs(self.background)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.prim(self.background)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.kruskal(self.background)

        pygame.display.update()

        while not self.exit:
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.exit = True
            e = pygame.event.get()
            if self.winner:
                self.background.fill(BLACK)
            for event in e:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if self.player.matrix_pos_x == self.final_coordinate_x and self.player.matrix_pos_y == self.final_coordinate_y:
                            self.winner = True
                    if event.key == pygame.K_t:
                        for item in self.maze.items:
                            if self.player.matrix_pos_x == item.matrix_pos_x and self.player.matrix_pos_y == item.matrix_pos_y:
                                if self.maze.knapsack.avaliable >= item.weight:
                                    self.maze.take_item(item)
                                    text(self.background, "ITEM GOT CAUGHT", ORANGE, FONTSIZE_MAZE + 5, 678, 680)
                                    pygame.display.update()
                                    pygame.time.wait(1500)
                                else: 
                                    text(self.background, "COULD NOT PICK UP ITEM BECAUSE WEIGHT IS GREATER THAN AVAILABLE", ORANGE, FONTSIZE_MAZE, 678, 680)
                                    pygame.display.update()
                                    pygame.time.wait(1500)
                    if event.key == pygame.K_r:
                        main()
                    if event.key == pygame.K_q:
                        self.winner = True
            self.update(e)
            self.render()

        pygame.quit()
        sys.exit(0)


def main():
    mygame = Game()
    mygame.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interruption')
