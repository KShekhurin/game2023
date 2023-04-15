import pygame
from Animation import *

class Helicopter(pygame.sprite.Sprite):
    def __init__(self, height, speed, *groups):
        super().__init__(*groups)

        self.rect = pygame.rect.Rect((165, height), (165, 53))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        helic_atlas = pygame.image.load("img/helic_atlas.png")
        fly_anim = Animation(2, helic_atlas, 0, 165, 53, 4)
        damage = Animation(100, helic_atlas, 53, 165, 53, 1)
        self.anim_manager = AnimationManager({
            "fly": fly_anim,
            "damage": damage
        })
        self.anim_manager.set_anim("fly")

        self.x, self.y = -165, height
        self.speed = speed

        self.state = "fly"
        self.damage_timer = 0
        self.damage_time = 20

    def update(self, *events):
        if self.state == "fly":
            self.x += self.speed
            self.rect.x = self.x

            if self.x > 750+165:
                self.kill()

        if self.state == "damage":
            self.damage_timer += 1
            if self.damage_timer > self.damage_time:
                self.kill()

        self.anim_manager.update()
        
        self.draw()

    def damage(self):
        self.state = "damage"
        self.anim_manager.set_anim("damage")

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(*self.anim_manager.get_anim_frame())