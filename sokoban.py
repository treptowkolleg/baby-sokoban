### Diese Datei soll unverändert bleiben und keinesfalls bearbeitet (edititert) werden. 
### Der Inhalt wird in der Hauptdatei main.py benutzt. Machen Sie alle Änderungen dort!

import pygame   # pip install pygame
import time     # built-in
import random   # built-in


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Cell:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def at(self, cell):
        return self.x==cell.x and self.y==cell.y


class World:
    SIZE = 20 # cell size in pixels
    
    def __init__(self, seed=None, width=20, height=20):
        self.w = width
        self.h = height
        if seed is None:
            seed = time.time()
        print(f"using seed: {seed} moves: ", end='')
        random.seed(seed)
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE*self.w, self.SIZE*self.h))
        pygame.display.set_caption(f"Sokoban Game {seed}")
        pygame.key.set_repeat(200, 100)
        self.set_box()
        self.set_target()
        self.set_player()
        self.draw()
    
    def draw_cell(self, cell, color):
        if cell is not None:
            pygame.draw.rect(self.screen, color, (self.SIZE*cell.x, self.SIZE*cell.y, self.SIZE, self.SIZE))
        
    def draw(self):
        self.screen.fill(BLACK)
        for x in range(self.w):
            for y in range(self.h):
                pygame.draw.rect(self.screen, GRAY, (self.SIZE*x, self.SIZE*y, self.SIZE, self.SIZE), 1)
        self.draw_cell(self.box, GREEN)
        self.draw_cell(self.target, YELLOW)
        self.draw_cell(self.me, RED)
        pygame.display.flip()
        pygame.time.delay(100)
        
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

    def set_cell(self, x=None, y=None) -> Cell:
        if x is None:
            x = random.randint(0,self.w-1)
        if y is None:
            y = random.randint(0,self.h-1)
        return Cell(x, y)
        
    def set_player(self, x=None, y=None):
        self.me = self.set_cell(x, y)
        
    def set_box(self, x=None, y=None):
        self.box = self.set_cell(x, y)
        
    def set_target(self, x=None, y=None):
        self.target = self.set_cell(x, y)
    
    def winning(self):
        if not self.has_target(self.box):
            return False
        font = pygame.font.SysFont(None, 100)
        text = font.render("Winner!", True, WHITE) 
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        print(".")  
        return True
                
    def left(self):
        print("L", end ='')
        self.move(-1,0)
        
    def right(self):
        print("R", end ='')
        self.move(+1,0)
        
    def up(self):
        print("U", end ='')
        self.move(0,-1)
        
    def down(self):
        print("D", end ='')
        self.move(0,+1)
        
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
        
    def has_box(self, cell):
        if self.box.at(cell):
            return True
        return False
                
    def has_target(self, cell):
        if self.target.at(cell):
            return True
        return False
                
    def move(self, dx, dy):
        next = Cell(self.me.x+dx, self.me.y+dy)
        if not self.inside(next):
            return 
        if self.has_box(next):
            next2 = Cell(next.x+dx, next.y+dy)
            if not self.inside(next2):
                return  # cannot push outside
            if self.has_box(next2):
                return  # cannot push 2 boxes
            self.box = next2
            
        self.me = next
        self.draw()