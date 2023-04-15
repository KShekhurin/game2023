import sys
import pygame
from Widgets import Button, ButtonDesignParams, Catcher, Image, Label, PicButton, PicButtonDesignParams, Slider, SliderWithValue


class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self, app):
        self.app = app

    def append_widget(self, widget):
        self.drawable.append(widget)
        self.updatable.append(widget)

    def append_many_widgets(self, widgets):
        for widget in widgets:
            self.append_widget(widget)

    def update(self, events):
        for updatable in self.updatable:
            updatable.update(events)

    def draw(self, screen):
        for drawable in self.drawable:
            drawable.draw(screen)


class MenuFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_settings(self):
        self.app.reload_frame(SettingsFrame())

    def goto_story(self):
        self.app.reload_frame(self.story_frame)
        
    def exit(self):
        sys.exit() # Да, это плохо. Я протяну колбеки, но потом.

    def post_init(self, app):
        super().post_init(app)

        self.story_frame = StoryFrame(
            "./img/story/f1.png",
            StoryFrame(
                "./img/story/f2.png",
                self
            )
        )
        
        self.buttons_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        background = Image(
            (0,0), (800, 600), "./img/mainm_bg.png", self.background_group
        )
        
        new_game_params = PicButtonDesignParams()
        new_game_params.pic = "./img/ng.png"
        new_game_params.focuse_pic = "./img/ng_f.png"
        PicButton((20, 10 + 300), (300, 70), "", new_game_params, self.goto_story, self.buttons_group)
        
        settings_params = PicButtonDesignParams()
        settings_params.pic = "./img/set.png"
        settings_params.focuse_pic = "./img/set_f.png"
        PicButton((20, 90 + 300), (300, 70), "", settings_params, self.goto_settings, self.buttons_group)

        exit_params = PicButtonDesignParams()
        exit_params.pic = "./img/exit.png"
        exit_params.focuse_pic = "./img/exit_f.png"
        PicButton((20, 170 + 300), (300, 70), "", exit_params, self.exit, self.buttons_group)

        Label((70, 100), "Съешь ещё больше этих сладких французских булок.", self.buttons_group)

        self.append_many_widgets((
            self.background_group,
            self.buttons_group
        ))

class SettingsFrame(Frame):
    def __init__(self):
        super().__init__()
    
    def goto_menu(self):
        self.app.reload_frame(MenuFrame())

    def post_init(self, app):
        super().post_init(app)

        self.buttons_group = pygame.sprite.Group()
    
        
        Label((250, 20), "Громкость:", self.buttons_group)
        SliderWithValue((250, 20 + 50), (255, 70), 0, self.buttons_group)

        back_params = PicButtonDesignParams()
        back_params.pic = "./img/back.png"
        back_params.focuse_pic = "./img/back_f.png"

        save_params = PicButtonDesignParams()
        save_params.pic = "./img/save.png"
        save_params.focuse_pic = "./img/save_f.png"
        
        PicButton((250, 20 + 150), (300, 70), "Сохранить", save_params, None, self.buttons_group)
        PicButton((575, 525), (200, 50), "Вернуться", back_params, self.goto_menu, self.buttons_group)

        self.append_many_widgets((
            self.buttons_group,
        ))

class StoryFrame(Frame):
    def __init__(self, image, next_frame):
        super().__init__()

        def goto_next():
            self.app.reload_frame(next_frame)
        
        self.background_group = pygame.sprite.Group()
        self.label_group = pygame.sprite.Group()
        self.catcher_group = pygame.sprite.Group()

        label = Label(
            (0, 0), "Для продолжения нажмите пробел...", self.label_group
        )
        background = Image(
            (0, 0), (800, 600), image, self.background_group
        )
        catcher = Catcher(pygame.K_SPACE, goto_next)
        
        self.updatable.append(catcher)
        self.append_many_widgets((
            self.background_group,
            self.label_group
        ))
        
        
        
        
