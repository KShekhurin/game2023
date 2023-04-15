import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.image = pygame.Surface((48, 48))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)

    def update(self, *events):
        pass
