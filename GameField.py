import pygame
from Bomb import *
from random import randrange
from Helicopter import *
from Ship import *
from App import explosion

class GameField:
    def __init__(self, player, bomb_group, helic_group, cuba, ship, sover_label, lives_label, lose_callback):
        self.player = player
        self.bombs = bomb_group
        self.helics = helic_group
        self.cuba = cuba
        self.sover_label = sover_label
        self.lives_labes = lives_label
        self.lose = lose_callback
        self.ship = ship

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
        self.helic_timer = 100
        self.helic_time = 200
        self.small_bomb_time = 150
        self.main_bomb_time = 444
        self.has_main_bomb = True

        self.sover = 100
        self.lives = 5
        self.sover_decr_speed = 0.04

        self.has_ship = False
        self.ship_timer = 350
        self.ship_time = 400

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
            
            if self.player.state != "damaged":
                for helic in self.helics.sprites():
                    if self.player.damage_rect.colliderect(helic.rect):
                        self.player.set_state("damaged")
                        helic.damage()
                        self.lives -= 1
                        self.lives_labes.delete_life()
                        break

            if self.player.get_state() == "bomb":
                if self.player.rect.colliderect(self.cuba.sprites()[0].rect):
                    self.sover += 5 * (self.player.bomb_type+1)
                    if self.sover > 100: self.sover = 100
                    self.player.set_state("empty")

                    if self.has_ship:
                        self.ship.sprites()[0].run_away()
                        self.has_ship = False

            if self.has_ship:
                if self.ship.sprites()[0].rect.colliderect(self.cuba.sprites()[0].rect):
                    self.sover = 0

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
            self.sover_label.set_level(self.sover)

            if self.sover < 1 or self.lives < 1:
                self.state = "lost"
                self.lose()

            self.helic_timer += 1
            if self.helic_timer > self.helic_time:
                self.helic_timer = 0
                rnd_speed = randrange(2, 6)
                rnd_height = randrange(20, 600)
                Helicopter(rnd_height, rnd_speed, self.helics)

            if not self.has_ship:
                self.ship_timer += 1
                if self.ship_timer > self.ship_time:
                    self.ship_timer = 0
                    self.has_ship = True
                    
                    rnd_ship_y = randrange(-50, 320)
                    Ship((-250, rnd_ship_y), (822, 198), self.ship)

            

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
