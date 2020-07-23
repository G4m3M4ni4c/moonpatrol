import pygame
from typing import Callable


class Terrain:
    def __init__(self, screen: pygame.Surface, color: pygame.Color, func: Callable[[int], int], gap=10):
        self.screen = screen
        self.color = color
        self.get_point = func
        self.gap = gap
        self.x_pos = 0
        self.ordinals = []
        self.generate_missing_ordinals()

    def generate_missing_ordinals(self, append_left=False):
        expected_ordinal_count = self.screen.get_width() // self.gap + 2
        actual_ordinal_count = len(self.ordinals)
        new_ordinals = []

        start = 0 if append_left else actual_ordinal_count - 1
        end = expected_ordinal_count - actual_ordinal_count if append_left else expected_ordinal_count
        for i in range(start, end):
            x = self.x_pos + i * self.gap
            y = self.get_point(x)
            new_ordinals.append(y)

        if append_left:
            self.ordinals = new_ordinals + self.ordinals
        else:
            self.ordinals += new_ordinals

    def get_y_at(self, screen_x):
        if not (0 <= screen_x < self.screen.get_width()):
            return None

        offset = self.x_pos % self.gap
        x_offset = screen_x - offset
        return self.screen.get_height() - self.get_point(x_offset + self.x_pos)

    def goto(self, x_pos):
        self.x_pos = x_pos
        self.ordinals = []
        self.generate_missing_ordinals()

    def move(self, amount):
        old_ordinal_offset = self.x_pos % self.gap
        self.x_pos += amount

        travel = old_ordinal_offset + amount
        if 0 < travel < self.gap:
            return

        remove_amount = int(travel // self.gap)
        if travel < self.gap:
            if remove_amount < 0:
                self.ordinals = self.ordinals[:remove_amount]
            self.generate_missing_ordinals(append_left=True)
        else:
            self.ordinals = self.ordinals[remove_amount:]
            self.generate_missing_ordinals()

    def get_end_pos(self):
        return self.x_pos + self.gap * len(self.ordinals)

    def draw(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        offset = self.x_pos % self.gap
        base_points = [(width, height), (0, height)]
        points = base_points + [(i * self.gap - offset, height - y) for i, y in enumerate(self.ordinals)]
        pygame.draw.polygon(self.screen, self.color, points)
