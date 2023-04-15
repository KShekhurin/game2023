import pygame

class Animation:
    def __init__(self, time, atlas, y_offset, width, height, amount):
        self.size = (width, height)
        self.amount = amount
        self.current_frame = 0
        self.y_offset = y_offset
        self.run = False
        self.timer = 0
        self.time = time
        self.atlas = atlas

    def start(self):
        self.run = True
        self.timer = 0
    
    def stop(self):
        self.run = False

    def update(self):
        if self.run:
            self.timer += 1
            if self.timer > self.time:
                self.timer = 0
                self.current_frame = (self.current_frame + 1) % self.amount

    def get_frame(self):
        return self.atlas, (0, 0), (self.current_frame*self.size[0], self.y_offset, self.size[0], self.size[1])
    
class AnimationManager:
    def __init__(self, anim_dict):
        self.anim_dict = anim_dict
        self.current_anim = None

    def set_anim(self, name):
        if self.current_anim != None:
            self.current_anim.stop()

        self.current_anim = self.anim_dict[name]
        self.current_anim.start()

    def update(self):
        self.current_anim.update()

    def get_anim_frame(self):
        return self.current_anim.get_frame()
