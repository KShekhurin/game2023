import pygame

class Cuba(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

        self.rect = pygame.rect.Rect((700, 20), (281, 256))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.texture = pygame.image.load("img/cuba.png")

    def update(self, *events):
        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.texture, (0, 0))