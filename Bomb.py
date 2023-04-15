import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, type, *group):
        super().__init__(*group)

        self.type = type

        size = (45, 100) if type == 0 else (69, 150)
        texture = "img/weapon.png" if type == 0 else "img/great_weapon.png"
        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.texture = pygame.image.load(texture)

    def update(self, *events):
        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.texture, (0, 0))