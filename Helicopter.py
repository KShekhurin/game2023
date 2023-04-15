import pygame

class Helicopter(pygame.sprite.Sprite):
    def __init__(self, height, *groups):
        super().__init__(*groups)

        