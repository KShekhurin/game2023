import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, type, *group):
        super().__init__(*group)

        self.type = type

        self.rect = pygame.rect.Rect(pos, (124, 203))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.texture = pygame.image.load("img/bomb.png")

    def update(self, *events):
        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.texture, (0, 0))