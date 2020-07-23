import pygame
from spritesheet import SpriteSheet
from constants import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, remove_self):
        super().__init__()
        spritesheet = SpriteSheet('./assets/sprites.png')
        large_explosion_rects = [(2 + 2 * 50 * i, 36, 48, 32) for i in range(3)]
        small_explosion_rects = [(302 + 2 * 34 * i, 52, 32, 16) for i in range(2)]
        last_explosion_rect = (438, 52, 16, 16)
        self.large_explosion_images = [pygame.transform.scale(img, (WIDE_TILE_SIZE, ROVER_SIZE))
                                       for img in spritesheet.images_at(*large_explosion_rects, color_key=-1)]
        self.small_explosion_images = [pygame.transform.scale(img, (ROVER_SIZE, WHEEL_SIZE))
                                       for img in spritesheet.images_at(*small_explosion_rects, color_key=-1)]
        self.last_explosion_image = pygame.transform.scale(spritesheet.image_at(last_explosion_rect, color_key=-1),
                                                           (WHEEL_SIZE, WHEEL_SIZE))
        self.x_pos, self.y_pos = x, y
        self.image = self.large_explosion_images[0]
        self.rect = (x, y, ROVER_SIZE, WIDE_TILE_SIZE)
        self.frame_timer = 0
        self.skip_frames = 8
        self.remove_self = remove_self

    def update(self, *args, **kwargs):
        self.frame_timer += 1
        if self.frame_timer % self.skip_frames > 0:
            return

        image_num = int(self.frame_timer // self.skip_frames)
        if image_num < 3:
            self.image = self.large_explosion_images[image_num]
        elif image_num < 5:
            self.image = self.small_explosion_images[image_num - 3]
            self.rect = (self.x_pos + WHEEL_SIZE / 2, self.y_pos + WHEEL_SIZE / 2, ROVER_SIZE, WHEEL_SIZE)
        elif image_num < 6:
            self.image = self.last_explosion_image
            self.rect = (self.x_pos + WHEEL_SIZE, self.y_pos + WHEEL_SIZE / 2, WHEEL_SIZE, WHEEL_SIZE)
        else:
            self.remove_self(self)

