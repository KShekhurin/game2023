import pygame
from Frames import Frame

class App:
    def __init__(self, loaded_frame: Frame, start_size=(480, 320)):
        self.start_size = start_size
        self.loaded_frame = loaded_frame

    def start(self):
        
        pygame.init()
        pygame.display.set_caption("Soy Cuba")
        pygame.font.init()
        
        self.clock = pygame.time.Clock()
        
        screen = pygame.display.set_mode(self.start_size)
        run = True

        self.loaded_frame.post_init(self)

        while run:
            self.clock.tick(50)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False

            screen.fill((0, 0, 0))
            self.loaded_frame.update(events)
            self.loaded_frame.draw(screen)

            pygame.display.flip()
    
    def reload_frame(self, new_frame: Frame):
        self.loaded_frame = new_frame
        self.loaded_frame.post_init(self)
