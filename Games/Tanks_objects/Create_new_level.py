import pygame
from Games import config
from Games.Tanks_objects import Walls
from Games.Tanks_objects import Tanks
import os
import csv
import time


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = [pygame.Color(0, 0, 0), pygame.Color(255, 0, 0), pygame.Color(0, 0, 255)]
        self.board = [['0'] * width for _ in range(height)]
        self.vis_board = [['0'] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen1):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen1, ('white'), (self.left + x * self.cell_size,
                                                           self.top + y * self.cell_size,
                                                           self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x1, y1 = mouse_pos
        for y in range(self.height):
            if self.top + y * self.cell_size < y1 < self.top + (y + 1) * self.cell_size:
                for x in range(self.width):
                    if self.left + x * self.cell_size < x1 < self.left + (x + 1) * self.cell_size:
                        return x, y

    def on_click(self, cell_coords):
        if cell_coords:
            # walls1[walls[index][0]](None, cell_coords, walls[index])
            try:
                self.board[cell_coords[1]][cell_coords[0]].kill()
            except Exception:
                pass
            try:
                wall = walls1[walls[index % len(walls)][0]](game, cell_coords, walls[index % len(walls)])
                all_sprites.add(wall)
            except Exception:
                wall = '0'
            self.board[cell_coords[1]][cell_coords[0]] = wall
            self.vis_board[cell_coords[1]][cell_coords[0]] = str(walls[index % len(walls)])

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


walls = ['0', 'b', 'bl', 'br', 'bu', 'bd', 'i', 'il', 'ir', 'iu', 'id', 'w', 'xz', 'sh']
walls1 = {
    'b': Walls.Brick,
    'i': Walls.Iron,
    's': Walls.Bush,
    'x': Walls.IronXZ,
    'w': Walls.Water
}
index = 0
all_sprites = pygame.sprite.Group()
game = None
x, y = 0, 0


class Creater:
    def __init__(self, game1):
        global game, all_sprites, index, x, y
        board = Board(*config.SIZE_BOARD_FOR_TANKS)
        board.set_view(0, 0,  config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0])
        running = True
        game = game1
        all_sprites = pygame.sprite.Group()
        pygame.init()
        size = config.WIDTH, config.HEIGHT
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        f = True
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if board.get_cell(event.pos):
                            x, y = board.get_cell(event.pos)
                    if event.button == 4:
                        index += 1
                    if event.button == 5:
                        index -= 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            f = False
                            with open(f'Games/Tanks_objects/data/levels/level{len(next(os.walk("Games/Tanks_objects/data/levels"))[2])}.csv',
                                      'w', newline='', encoding="utf8") as csvfile:
                                writer = csv.writer(
                                    csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                for i in board.vis_board:
                                    writer.writerow(i)



            if f:
                board.on_click((x, y))

                board.render(screen)
                all_sprites.draw(screen)
                all_sprites.update()
            else:
                font = pygame.font.SysFont('monospace', 50)
                text = font.render("Сохранено!", True, (194, 152, 0))
                screen.blit(text, (config.WIDTH // 2 - text.get_width() // 2, config.HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                time.sleep(2)
                for i in all_sprites:
                    i.kill()
                exit()
            pygame.display.flip()
        for i in all_sprites:
            i.kill()