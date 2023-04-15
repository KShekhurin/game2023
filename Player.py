import pygame
from Animation import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)

        self.rect = pygame.rect.Rect(pos, (155, 126))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        atlas = pygame.image.load("img/player_atlas.png")
        empty_right = Animation(5, atlas, 0, 155, 126, 2)
        empty_left = Animation(5, atlas, 126, 155, 126, 2)
        bomb_left = Animation(5, atlas, 253, 155, 126, 2)
        bomb_right = Animation(5, atlas, 379, 155, 126, 2)
        self.anim_manager = AnimationManager({
            "empty_left": empty_left,
            "empty_right": empty_right,
            "bomb_left": bomb_left,
            "bomb_right": bomb_right
        })
        self.anim_manager.set_anim("empty_right")

        self.x = pos[0]
        self.y = pos[1]
        self.direction = pygame.math.Vector2((0, 0))
        self.speed = 4

        self.state = "empty"
        self.bomb_type = None
        self.dir = "right"

    def update(self, *events):
        self.direction.x = 0
        self.direction.y = 0

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.direction.x = -1
        if pressed[pygame.K_RIGHT]:
            self.direction.x = 1    
        if pressed[pygame.K_UP]:
            self.direction.y = -1
        if pressed[pygame.K_DOWN]:
            self.direction.y = 1    
    
        for event in events[0]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dir = "left"
                    if self.state == "empty":
                        self.anim_manager.set_anim("empty_left")
                    elif self.state == "bomb":
                        self.anim_manager.set_anim("bomb_left")

                if event.key == pygame.K_RIGHT:
                    self.dir = "right"
                    if self.state == "empty":
                        self.anim_manager.set_anim("empty_right")
                    elif self.state == "bomb":
                        self.anim_manager.set_anim("bomb_right")

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

        self.anim_manager.update()

        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(*self.anim_manager.get_anim_frame())

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state
        
        if self.state == "empty":
            self.bomb_type = None
            if self.dir == "right":
                self.anim_manager.set_anim("empty_right")
            if self.dir == "left":
                self.anim_manager.set_anim("empty_left")
        elif self.state == "bomb":
            if self.dir == "right":
                self.anim_manager.set_anim("bomb_right")
            if self.dir == "left":
                self.anim_manager.set_anim("bomb_left")
