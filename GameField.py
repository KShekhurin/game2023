import pygame
from Bomb import *
from random import randrange

class GameField:
    def __init__(self, player, bomb_group, cuba, sover_label, lives_label, lose_callback):
        self.player = player
        self.bombs = bomb_group
        self.cuba = cuba
        self.sover_label = sover_label
        self.lives_labes = lives_label
        self.lose = lose_callback

        self.state = "game"

        self.bomb_grid = [
            [(915, 417), False],
            [(778, 572), False],
            [(557, 511), False],
            [(441, 657), False],
            [(41, 522), False],
            [(416, 434), False]
        ]
        self.main_bomb_pos = (150, 550)
        for bg in self.bomb_grid:
            Bomb(bg[0], 0, self.bombs)
        Bomb(self.main_bomb_pos, 1, self.bombs)
        self.bombs_count = 7
        self.small_timer = 0
        self.main_timer = 0
        self.small_bomb_time = 150
        self.main_bomb_time = 444
        self.has_main_bomb = True

        self.sover = 100
        self.lives = 5
        self.sover_decr_speed = .7

    def update(self, *events):
        if self.state == "game":
            if self.player.get_state() == "empty":
                for bomb in self.bombs.sprites():
                    if self.player.rect.colliderect(bomb.rect):
                        self.bombs_count -= 1
                        bomb_pos = (bomb.rect.x, bomb.rect.y)
                        if bomb_pos == self.main_bomb_pos:
                            self.has_main_bomb = False
                        
                        for i in range(0, len(self.bomb_grid)):
                            if bomb_pos == self.bomb_grid[i][0]:
                                self.bomb_grid[i][1] = False
                                break

                        self.player.set_state("bomb")
                        self.player.bomb_type = bomb.type
                        bomb.kill()
                        break

            if self.player.get_state() == "bomb":
                if self.player.rect.colliderect(self.cuba.sprites()[0].rect):
                    self.sover += 5 * (self.player.bomb_type+1)
                    self.player.set_state("empty")

            if not self.has_main_bomb:
                self.main_timer += 1
            if self.bombs_count <= 3:
                self.small_timer += 1

            if self.main_timer >= self.main_bomb_time:
                self.has_main_bomb = True
                self.bombs_count += 1
                self.main_timer = 0
                Bomb(self.main_bomb_pos, 1, self.bombs)

            if self.small_timer >= self.small_bomb_time:
                self.spawn_random_bomb()
                self.small_timer = 0

            self.sover -= self.sover_decr_speed
            self.sover_label.text = str(int(self.sover))

            if self.sover < 1:
                self.state = "lost"
                self.lose()

            

    def spawn_random_bomb(self):
        while True:
            rint = randrange(6)
            if self.bomb_grid[rint][1]:
                continue
            else:
                Bomb(self.bomb_grid[rint][0], 0, self.bombs)
                self.bomb_grid[rint][1] = True
                self.bombs_count += 1
                break
