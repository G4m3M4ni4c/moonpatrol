import pygame
from typing import Callable
from constants import *
from eventmanager import register_event


class Menu:
    def __init__(self, screen: pygame.Surface, start_game: Callable[[], None]):
        self.screen = screen
        self.start_game = start_game
        self.background = pygame.transform.scale(pygame.image.load('./assets/menu_background.jpg').convert(),
                                                 self.screen.get_size())

        font = pygame.font.Font('freesansbold.ttf', 64)
        font.set_bold(True)
        width = screen.get_width()
        height = screen.get_height()

        self.start_button_selected = False
        self.start_button_title = font.render('Start', True, WHITE)
        self.start_button_rect = (width * 0.3, height * 0.42, width * 0.4, height * 0.16)

        register_event(self.mouse_movement, pygame.MOUSEMOTION)
        register_event(self.mouse_click, pygame.MOUSEBUTTONUP)

    def mouse_click(self, event):
        if self.start_button_selected:
            self.start_button_selected = False
            self.start_game()

    def mouse_movement(self, event):
        x, y = pygame.mouse.get_pos()

        start_x, start_y, start_width, start_height = self.start_button_rect
        if start_x <= x < start_x + start_width and start_y <= y < start_y + start_height:
            self.start_button_selected = True
        elif self.start_button_selected:
            self.start_button_selected = False

    def tick(self):
        pass

    def draw(self):
        self.screen.blit(self.background, self.screen.get_rect())

        border_1 = 4
        border_2 = 10
        start_x, start_y, start_width, start_height = self.start_button_rect

        button_color = ORANGE if self.start_button_selected else RED
        pygame.draw.rect(self.screen, WHITE, (start_x, start_y, start_width, start_height))
        pygame.draw.rect(self.screen, BLACK, (start_x - border_1 + border_2, start_y - border_1 + border_2,
                                              start_width + (border_1 - border_2) * 2,
                                              start_height + (border_1 - border_2) * 2))
        pygame.draw.rect(self.screen, button_color, (start_x + border_2, start_y + border_2,
                                                     start_width - border_2 * 2, start_height - border_2 * 2))
        start_title_width = self.start_button_title.get_width()
        start_title_height = self.start_button_title.get_height()
        self.screen.blit(self.start_button_title, (start_x + (start_width - start_title_width) / 2,
                                                   start_y + (start_height - start_title_height) / 2,
                                                   start_title_width, start_title_height))
