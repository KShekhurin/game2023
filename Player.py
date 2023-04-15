import pygame
from Animation import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)

        self.rect = pygame.rect.Rect(pos, (65, 68))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        atlas = pygame.image.load("img/atlas.png")
        walk_left_anim = Animation(5, atlas, 0, 65, 68, 3)
        walk_right_anim = Animation(5, atlas, 0, 65, 68, 3)
        stand_anim = Animation(100, atlas, 68, 65, 68, 1)
        self.anim_manager = AnimationManager({
            "walk_left": walk_left_anim,
            "walk_right": walk_right_anim,
            "stand": stand_anim
        })
        self.anim_manager.set_anim("stand")

        self.x = pos[0]
        self.y = pos[1]
        self.direction = pygame.math.Vector2((0, 0))
        self.speed = 2

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.anim_manager.set_anim("walk")

            if event.type == pygame.KEYUP:
                self.anim_manager.set_anim("stand")

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
