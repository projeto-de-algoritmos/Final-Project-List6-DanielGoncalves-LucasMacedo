import sys
import pygame
import random

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

HEIGHT_TOTAL = 900
WIDTH_TOTAL = 1600
WIDTH = 900
HEIGHT = 900
SCREEN_SIZE = (WIDTH_TOTAL, HEIGHT_TOTAL)

FONTSIZE_START = 50
FONTSIZE_COMMANDS_INTIAL = 30
FONTSIZE_MAZE = 20

SIZE = 45

def text(background, message, color, size, coordinate_x, coordinate_y):
    font = pygame.font.SysFont(None, size)
    txt = font.render(message, True, color)
    background.blit(txt, [coordinate_x, coordinate_y])


class Item():
    def __init__(self, weight, value, name, color, pos_x, pos_y):
        self.weight = weight
        self.value = value

        self.name = name
        self.color = color

        self.pos_x = pos_x * SIZE + BORDER_THICKNESS
        self.pos_y = pos_y * SIZE + BORDER_THICKNESS

        self.matrix_pos_x = pos_x
        self.matrix_pos_y = pos_y

        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])


class Knapsack():
    def __init__(self, avaliable, pos_x, pos_y, color):
        self.items = []
        self.avaliable = avaliable
        self.value = 0

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS

        self.color = color

    def render(self, background):
        # renderizar mochila na parte direita
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])
        # TODO renderizar itens que estao na mochila ao lado da mochila
        temp_pos_x = self.pos_x + SIZE
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
    def __init__(self, initial_x, initial_y, final_x, final_y):
        self.maze = []
        self.total_nodes = 0
        self.maze_created = False
        self.initial_coordinate_x = initial_x
        self.initial_coordinate_y = initial_y
        self.final_coordinate_x = final_x
        self.final_coordinate_y = final_y

        self.items = []

        self.knapsack = Knapsack(random.randint(10, 30), 920, 400, BLUE)

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
        # funcao responsavel por criar os itens no labirinto, criar as 6 posicoes, 6 valores e 6 pesos e imagens
        # TODO: Imagem no lugar da cor e Nome
        positions = []
        positions.append((self.initial_coordinate_x, self.initial_coordinate_y))
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

            color = WHITE
            item = Item(weight, value, i + 1, color, pos_x, pos_y)
            self.items.append(item)

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
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 950, 20)
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
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 920, 20)
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
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 920, 20)
            pygame.display.update()
        self.maze_created = True

    def bfs(self, background, player):
        initial_node = self.maze[player.matrix_pos_x][player.matrix_pos_y]
        initial_node.explored = True
        find = False
        queue = [initial_node]
        while len(queue) > 0 and not find:
            queue[0].color = PINK

            if queue[0].top_border.color == INTERMEDIARYORANGE:
                queue[0].top_border.color = PINK
            if queue[0].bottom_border.color == INTERMEDIARYORANGE:
                queue[0].bottom_border.color = PINK
            if queue[0].right_border.color == INTERMEDIARYORANGE:
                queue[0].right_border.color = PINK
            if queue[0].left_border.color == INTERMEDIARYORANGE:
                queue[0].left_border.color = PINK

            u = queue.pop(0)
            for i in u.neighbors_connected:
                if i.explored == False:
                    i.parent = u
                    i.explored = True
                    queue.append(i)
                    if i.matrix_pos_x == self.final_coordinate_x and i.matrix_pos_y == self.final_coordinate_y:
                        find = True
            self.render(background)
            text(background, "SOLVING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, 920, 20)
            player.render(background)
            pygame.display.update()
        
        current = self.maze[self.final_coordinate_x][self.final_coordinate_y]
        while (current.parent).parent != None:
            current = current.parent
            current.color = ORANGE

            if current.top_border.color == PINK:
                current.top_border.color = ORANGE
            if current.bottom_border.color == PINK:
                current.bottom_border.color = ORANGE
            if current.right_border.color == PINK:
                current.right_border.color = ORANGE
            if current.left_border.color == PINK:
                current.left_border.color = ORANGE

            self.render(background)
            player.render(background)
            pygame.display.update()

    def take_item(self, item):
        print("antes AVAILABLE")
        print(self.knapsack.avaliable)
        print("antes VALUE")
        print(self.knapsack.value)

        self.items.remove(item)
        self.knapsack.items.append(item)
        self.knapsack.avaliable -= item.weight
        self.knapsack.value += item.value

        print("AVAILABLE")
        print(self.knapsack.avaliable)
        print("VALUE")
        print(self.knapsack.value)

    def render(self, background):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)

        if self.maze_created:
            self.maze[self.initial_coordinate_x][self.initial_coordinate_y].color = BEIGE
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
        self.solved = False
        self.winner = False
        self.exit = False

        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Knapsack Maze')
        self.initial_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.initial_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)

        self.final_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.final_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)

        while self.final_coordinate_x == self.initial_coordinate_x or self.final_coordinate_y == self.initial_coordinate_y:
            self.final_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
            self.final_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)

        self.maze = Maze(self.initial_coordinate_x, self.initial_coordinate_y, self.final_coordinate_x, self.final_coordinate_y)
        self.player = Player(self.initial_coordinate_x, self.initial_coordinate_y)

    def update(self, event):
        if not self.solved and not self.winner:
            self.player.update(self.maze.maze, event)

        # if (self.player.matrix_pos_x == self.maze.final_coordinate_x and self.player.matrix_pos_y == self.maze.final_coordinate_y):
            # self.winner = True

    def initial_game(self):
        self.background.fill(DARKBLUE)
        pygame.draw.rect(self.background, RED, [50, 40, 1500, 580])
        pygame.draw.rect(self.background, LIGHTBLUE, [50, 100, 1500, 450])
        pygame.draw.rect(self.background, BLACK, [120, 150, 1350, 380])
        pygame.draw.rect(self.background, DARKBLUE, [120, 150, 1350, 100])
        text(self.background, "KNAPSACK MAZE", ORANGE, FONTSIZE_START, 650, 185)
        text(self.background, "PRESS (ESC) TO CLOSE GAME", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 650, 480)
        pygame.display.update()
        pygame.time.wait(250)
        text(self.background, "PRESS (D) TO START GAME (DFS)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 650, 330)
        text(self.background, "PRESS (P) TO START GAME (PRIM'S)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 640, 370)
        text(self.background, "PRESS (K) TO START GAME (KRUSKAL)", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL, 630, 410)
        pygame.display.update()
        pygame.time.wait(250)

    def end_of_game(self):
        self.maze.bfs(self.background, self.player)

    def render(self):
        self.background.fill(BLACK)

        self.maze.render(self.background)

        self.player.render(self.background)

        if not self.solved and not self.winner:
            pygame.draw.rect(self.background, RED, [920, 20, SIZE, SIZE])
            text(self.background, "- PLAYER", WHITE, FONTSIZE_MAZE, 920 + SIZE + 3, 20 + 6)
            pygame.draw.rect(self.background, BEIGE, [920, 20 + SIZE + 1, SIZE, SIZE])
            text(self.background, "- STARTING POINT", WHITE, FONTSIZE_MAZE, 920 + SIZE + 3, 20 + SIZE + 1 + 6)
            pygame.draw.rect(self.background, LIGHTBLUE, [920, 20 + 2 * SIZE + 2, SIZE, SIZE])
            text(self.background, "- GOAL", WHITE, FONTSIZE_MAZE, 920 + SIZE + 3, 20 + 2 * SIZE + 1 + 6)

            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 920, 200)
            text(self.background, "PRESS (Q) TO GIVE UP", WHITE, FONTSIZE_MAZE, 920, 230)
            text(self.background, "PRESS (T) IN ITEM TO TAKE", WHITE, FONTSIZE_MAZE, 920, 250)
            text(self.background, "PRESS (F) IN GOAL TO DELIVER ITEMS", WHITE, FONTSIZE_MAZE, 920, 270)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 920, 300)

            text(self.background, "KNAPSACK AVAILABLE " + str(self.maze.knapsack.avaliable), WHITE, FONTSIZE_MAZE + 15, 920, 700)

        elif self.winner:
            text(self.background, "YOU WIN", BLUE, FONTSIZE_MAZE + 3, 920, 210)
            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 920, 230)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 920, 250)
        else:
            text(self.background, "YOU LOSE", RED, FONTSIZE_MAZE + 3, 920, 210)
            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 920, 230)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 920, 250)

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
                                print("AVALIABLE")
                                print(self.maze.knapsack.avaliable)
                                print("PESO DO ITEM")
                                print(item.weight)
                                if self.maze.knapsack.avaliable >= item.weight:
                                    self.maze.take_item(item)
                                    text(self.background, "ITEM GOT CAUGHT", WHITE, FONTSIZE_MAZE, 920, 800)
                                    pygame.display.update()
                                    pygame.time.wait(1500)
                                else: 
                                    text(self.background, "COULD NOT PICK UP ITEM BECAUSE WEIGHT IS GREATER THAN AVAILABLE", WHITE, FONTSIZE_MAZE, 920, 800)
                                    pygame.display.update()
                                    pygame.time.wait(1500)
                    if event.key == pygame.K_r:
                        main()
                    if (not self.solved and event.key == pygame.K_q and not self.winner):
                        self.background.fill(BLACK)
                        self.end_of_game()
                        self.solved = True
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
