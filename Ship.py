import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, dest_pos, *groups):
        super().__init__(*groups)

        self.spawn_pos = (pos[0] + 125, pos[1] + 63)
        self.dest_pos = dest_pos

        self.vec = pygame.math.Vector2((self.dest_pos[0] - self.spawn_pos[0], self.dest_pos[1] - self.spawn_pos[1]))
        self.vec = self.vec.normalize()

        self.rect = pygame.rect.Rect(pos, (250, 126))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.texture = pygame.image.load("img/ship.png")

        self.x, self.y = pos[0], pos[1]
        self.speed = 2
        
        self.state = "fight"

    def update(self, *events):
        self.x += self.vec.x * self.speed
        self.y += self.vec.y * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

        if self.x < -250:
            self.kill()

        self.draw()

    def run_away(self):
        self.speed = 8
        self.vec = pygame.math.Vector2((self.spawn_pos[0]-self.dest_pos[0], self.spawn_pos[1]-self.dest_pos[1]))
        self.vec = self.vec.normalize()

        self.texture = pygame.transform.flip(self.texture, True, False)

        self.state = "run"

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.texture, (0, 0))