import pygame
from constants import *
from eventmanager import register_event


class GameOver(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, score, restart_game, padding=50):
        super().__init__()
        self.restart_game = restart_game

        font = pygame.font.Font('freesansbold.ttf', 64)
        font.set_bold(True)
        self.restart_button_selected = False
        self.restart_button_title = font.render('Restart', True, BLACK)
        self.restart_button_title_selected = font.render('Restart', True, GREY)
        self.restart_button_rect = (width / 2 - self.restart_button_title.get_width() / 2,
                                    height - padding - self.restart_button_title.get_height() / 2,
                                    self.restart_button_title.get_width(), self.restart_button_title.get_height())

        font = pygame.font.Font('freesansbold.ttf', 80)
        font.set_bold(True)
        game_over_text = font.render('Game Over', True, BLACK)

        self.background = pygame.Surface([width, height])
        self.background.fill(pygame.Color(255, 255, 255, 180))
        self.background.blit(game_over_text, (width / 2 - game_over_text.get_width() / 2, padding,
                                              game_over_text.get_width(), game_over_text.get_height()))

        font = pygame.font.Font('freesansbold.ttf', 52)
        score_text = font.render(f'Score: {score}', True, BLACK)

        top = padding + game_over_text.get_height()
        blank_space = self.restart_button_rect[1] - top

        self.background.blit(score_text, (width / 2 - score_text.get_width() / 2,
                             top + blank_space / 2 - score_text.get_height() / 2,
                             score_text.get_width(), score_text.get_height()))

        self.image = self.background.copy()
        self.rect = (x, y, width, height)

        register_event(self.mouse_movement, pygame.MOUSEMOTION)
        register_event(self.mouse_click, pygame.MOUSEBUTTONUP)

    def mouse_click(self, event):
        if self.restart_button_selected:
            self.restart_button_selected = False
            self.restart_game(self)

    def mouse_movement(self, event):
        x, y = pygame.mouse.get_pos()

        restart_x, restart_y, restart_width, restart_height = self.restart_button_rect
        restart_x += self.rect[0]
        restart_y += self.rect[1]
        if restart_x <= x < restart_x + restart_width and restart_y <= y < restart_y + restart_height:
            self.restart_button_selected = True
        elif self.restart_button_selected:
            self.restart_button_selected = False

    def update(self, *args, **kwargs):
        self.image = self.background.copy()
        button_image = self.restart_button_title_selected if self.restart_button_selected else self.restart_button_title
        self.image.blit(button_image, self.restart_button_rect)
