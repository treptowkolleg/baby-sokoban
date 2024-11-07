import random
import time

import pygame

from src.cell import Cell

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class World:


    SIZE = 20  # cell size in pixels

    def __init__(self, seed=None, boxes=2, width=20, height=20):

        pygame.mixer.init()
        self.bgm2 = pygame.mixer.Sound("./wav/smw_course_clear.wav")
        self.w = width
        self.h = height
        self.boxCount = boxes
        self.me: None | Cell = None
        self.box: None | Cell = None
        self.box_index: None | int = None
        self.boxes = list()
        self.target: None | Cell = None
        self.target_index: None | int = None
        self.targets = list()
        self.moves = 0


        if seed is None:
            seed = time.time()
        print(f"using seed: {seed} moves: ", end='')
        random.seed(seed)
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE * self.w, self.SIZE * self.h))
        pygame.display.set_caption(f"Sokoban Game {seed}")
        pygame.key.set_repeat(200, 100)
        self.set_box()
        self.set_target()
        self.set_player()
        self.draw()

    def set_box(self, x=None, y=None):
        for i in range(self.boxCount):
            self.boxes.append(self.set_cell(x, y))
        random.sample(self.boxes,3)

    def set_target(self, x=None, y=None):
        for _ in range(self.boxCount):
            self.targets.append(self.set_cell(x,y))

    def set_player(self, x=None, y=None):
        self.me = self.set_cell(x, y)

    def set_cell(self, x=None, y=None) -> Cell:
        if x is None:
            x = random.randint(0,self.w-1)
        if y is None:
            y = random.randint(0,self.h-1)
        return Cell(x, y)

    def draw(self):
        self.screen.fill(BLACK)
        for x in range(self.w):
            for y in range(self.h):
                pygame.draw.rect(self.screen, GRAY, (self.SIZE * x, self.SIZE * y, self.SIZE, self.SIZE), 1)
        for target in self.targets:
            self.draw_cell(target, YELLOW)
        for box in self.boxes:
            self.draw_cell(box, GREEN)
        self.draw_cell(self.me, RED)
        pygame.display.flip()
        pygame.time.delay(50)

    def draw_cell(self, cell: Cell, color):
        if cell is not None:
            pygame.draw.rect(self.screen, color, (self.SIZE * cell.x, self.SIZE * cell.y, self.SIZE, self.SIZE))

    def winning(self):
        if not self.has_target():
            return False
        print(self.moves,end='')
        pygame.mixer.music.stop()
        self.bgm2.play()
        font = pygame.font.SysFont(None, 100)
        string = "Winner! (" + str(self.moves) +  " Moves)"
        text = font.render(string, True, WHITE)
        self.screen.blit(text, (
        self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(8000)
        print(".")
        return True

    def waitKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'q'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        return 'a'
                    if event.key == pygame.K_RIGHT:
                        return 'd'
                    if event.key == pygame.K_UP:
                        return 'w'
                    if event.key == pygame.K_DOWN:
                        return 's'
                    if event.key == pygame.K_q:
                        return 'q'

    def left(self):
        #print("L", end='')
        self.move(-1, 0)

    def right(self):
        #print("R", end='')
        self.move(+1, 0)

    def up(self):
        #print("U", end='')
        self.move(0, -1)

    def down(self):
        #print("D", end='')
        self.move(0, +1)

    def inside(self, cell):
        if cell.x < 0:
            return False
        if cell.x >= self.w:
            return False
        if cell.y < 0:
            return False
        if cell.y >= self.h:
            return False
        return True

    def has_box(self,cell: Cell):
        if self.box.at(cell):
            return True
        return False

    def has_target(self):
        hit = len(self.boxes)
        for target in self.targets:
            for box in self.boxes:
                if target.at(box):
                    hit = hit - 1
        if hit == 0:
            return True
        return False

    def get_box(self, index: int):
        self.box = self.boxes[index]
        self.box_index = index

    def get_target(self, index: int):
        self.target = self.targets[index]
        self.target_index = index

    def move(self, dx, dy):
        self.moves += 1
        next = Cell(self.me.x + dx, self.me.y + dy)
        if not self.inside(next):
            return
        if self.has_box(next):
            next2 = Cell(next.x + dx, next.y + dy)
            if not self.inside(next2):
                return  # cannot push outside
            if self.has_box(next2):
                return  # cannot push 2 boxes
            self.box = next2
            self.boxes[self.box_index] = next2
        self.me = next
        self.draw()

