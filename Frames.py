import sys
import pygame
from Widgets import *
from Player import *
from Bomb import *
from GameField import *
from Cuba import *

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

    def start_game(self):
        self.app.reload_frame(GameFrame())

    def goto_story(self):
        self.app.reload_frame(self.story_frame)

    def return_to_menu(self):
        self.app.reload_frame(self)
        
    def goto_help(self):
        self.app.reload_frame(HelpFrame(self.return_to_menu))
        
    def exit(self):
        sys.exit() # Да, это плохо. Я протяну колбеки, но потом.

    def post_init(self, app):
        super().post_init(app)

        self.story_frame = StoryFrame(
            app,
            "./img/story/f1.png",
            StoryFrame(
                app,
                "./img/story/f2.png",
                StoryFrame(
                    app,
                    "./img/story/f3.png",
                    StoryFrame(
                        app,
                        "./img/story/f4.png",
                        StoryFrame(
                            app,
                            "./img/story/f5.png",
                            StoryFrame(
                                app,
                                "./img/story/f6.png",
                                StoryFrame(
                                    app,
                                    "./img/story/f7.png",
                                    self
                                )
                            )
                        )
                    )
                )
            )
        )
        
        self.buttons_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        background = Image(
            (0,0), self.app.start_size, "./img/mainm_bg.png", self.background_group
        )
        
        new_game_params = PicButtonDesignParams()
        new_game_params.pic = "./img/ng.png"
        new_game_params.focuse_pic = "./img/ng_f.png"
        PicButton((20, 10 + 300), (300, 70), "", new_game_params, self.start_game, self.buttons_group)
        
        settings_params = PicButtonDesignParams()
        settings_params.pic = "./img/set.png"
        settings_params.focuse_pic = "./img/set_f.png"
        PicButton((20, 90 + 300), (300, 70), "", settings_params, self.goto_settings, self.buttons_group)

        story_params = PicButtonDesignParams()
        story_params.pic = "./img/story.png"
        story_params.focuse_pic = "./img/story_f.png"
        PicButton((20, 170 + 300), (300, 70), "", story_params, self.goto_story, self.buttons_group)

        exit_params = PicButtonDesignParams()
        exit_params.pic = "./img/exit.png"
        exit_params.focuse_pic = "./img/exit_f.png"
        PicButton((20, 250 + 300), (300, 70), "", exit_params, self.exit, self.buttons_group)

        help_params = PicButtonDesignParams()
        help_params.pic = "./img/help.png"
        help_params.focuse_pic = "./img/help_f.png"
        PicButton((1000 - 20 - 70, 20), (70, 70), "", help_params, self.goto_help, self.buttons_group)
        
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

class GameFrame(Frame):
    def __init__(self):
        super().__init__()

    def post_init(self, app):
        super().post_init(app)

        self.background_group = pygame.sprite.Group()
        Image((0, 0), self.app.start_size, "img/game_bg.png", self.background_group)

        self.gui_group = pygame.sprite.Group()
        Label((10, 20), "Суверенитет: ", self.gui_group)
        Label((10, 60), "Пуговицы: ", self.gui_group)
        self.sover_label = Label((200, 20), "100%", self.gui_group)
        self.lives_label = Label((200, 60), "5", self.gui_group)

        self.player_group = pygame.sprite.Group()
        Player((100, 100), self.player_group)

        self.bombs_group = pygame.sprite.Group()

        self.cuba_group = pygame.sprite.Group()
        Cuba(self.cuba_group)

        self.game_field = GameField(self.player_group.sprites()[0], self.bombs_group, self.cuba_group, self.sover_label, self.lives_label, self.lose)

        self.append_many_widgets((
            self.background_group,
            self.gui_group,
            self.cuba_group,
            self.bombs_group,
            self.player_group,
        ))
        self.updatable.append(self.game_field)

    def lose(self):
        self.app.reload_frame(LostFrame())

class LostFrame(Frame):
    def __init__(self):
        super().__init__()

    def post_init(self, app):
        super().post_init(app)

        self.background_group = pygame.sprite.Group()
        Image((0, 0), self.app.start_size, "img/lost_bg.png", self.background_group)

        self.append_many_widgets((
            self.background_group,
        ))

class StoryFrame(Frame):
    def __init__(self, image, next_frame):
        super().__init__()

class HelpFrame(Frame):
    def __init__(self, back_call):
        super().__init__()
        self.back_call = back_call
        
    def post_init(self, app):
        super().post_init(app)
        self.buttons_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        
        Image((0, 0), self.app.start_size, "./img/help_bg.png", self.background_group)
        back_params = PicButtonDesignParams()
        
        back_params.pic = "./img/back.png"
        back_params.focuse_pic = "./img/back_f.png"
        PicButton((1000 - 200, 750 - 50 - 15), (200, 50), "Вернуться", back_params, self.back_call, self.buttons_group)
        
        self.append_many_widgets((
            self.background_group,
            self.buttons_group
        ))

        
        
class StoryFrame(Frame):
    def __init__(self, app, image, next_frame):
        super().__init__()
        self.app = app
        
        def goto_next():
            self.app.reload_frame(next_frame)
        
        self.background_group = pygame.sprite.Group()
        self.label_group = pygame.sprite.Group()
        self.catcher_group = pygame.sprite.Group()

        label = Label(
            (0, 0), "Для продолжения нажмите пробел...", self.label_group
        )
        background = Image(
            (0, 0), self.app.start_size, image, self.background_group
        )
        catcher = Catcher(pygame.K_SPACE, goto_next)
        
        self.updatable.append(catcher)
        self.append_many_widgets((
            self.background_group,
            self.label_group
        ))
        
        
        
        
