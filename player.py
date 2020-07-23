import pygame
from spritesheet import SpriteSheet
from constants import *
from eventmanager import register_event
import game


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        spritesheet = SpriteSheet('./assets/sprites.png')

        chassis_rects = [(2 + 2 * 34 * i, 2, 32, 32) for i in range(3)]
        big_wheels_rects = [(206, 2, 16, 16), (206, 19, 16, 16)]
        small_wheel_rects = [(242, 2, 16, 16), (242, 19, 16, 16)]
        self.chassis_images = [pygame.transform.scale(img, (ROVER_SIZE, ROVER_SIZE))
                               for img in spritesheet.images_at(*chassis_rects, color_key=-1)]
        self.big_wheels_images = [pygame.transform.scale(img, (WHEEL_SIZE, WHEEL_SIZE))
                                  for img in spritesheet.images_at(*big_wheels_rects, color_key=-1)]
        self.small_wheel_images = [pygame.transform.scale(img, (WHEEL_SIZE, WHEEL_SIZE))
                                   for img in spritesheet.images_at(*small_wheel_rects, color_key=-1)]
        self.image = self.chassis_images[2]
        self.rect = (x, y, ROVER_SIZE, ROVER_SIZE)
        self.x_pos, self.y_pos = x, y
        self.x_vel, self.y_vel = 0, 0
        self.dead = False
        self.on_ground = True
        self.jumping = False
        self.wheel_animation = 0
        self.draw_rover_ground()

        register_event(self.jump, pygame.KEYDOWN, lambda e: e.key == pygame.K_SPACE)
        register_event(self.jump, pygame.KEYUP, lambda e: e.key == pygame.K_SPACE)
        register_event(lambda e: self.accelerate(-MOVE_SPEED), pygame.KEYDOWN, lambda e: e.key == pygame.K_a)
        register_event(lambda e: self.accelerate(MOVE_SPEED), pygame.KEYDOWN, lambda e: e.key == pygame.K_d)
        register_event(lambda e: self.accelerate(MOVE_SPEED), pygame.KEYUP, lambda e: e.key == pygame.K_a)
        register_event(lambda e: self.accelerate(-MOVE_SPEED), pygame.KEYUP, lambda e: e.key == pygame.K_d)

    def jump(self, event):
        if self.on_ground:
            self.on_ground = False
            self.jumping = True
        if event and event.type == pygame.KEYUP:
            self.jumping = False
        if self.jumping and -self.y_vel < MAX_JUMP:
            self.y_vel -= G * 0.05
        elif self.jumping:
            self.jumping = False

    def accelerate(self, amount):
        self.x_vel += amount

    def update(self, *args, **kwargs):
        if not self.on_ground and self.y_vel > 0:
            height_below = game.get_game().terrain.get_y_at(self.x_pos + 100)
            if height_below < self.y_pos:
                self.on_ground = True
                self.y_vel = 0

        if self.on_ground:
            self.x_pos += self.x_vel

        if self.on_ground:
            self.wheel_animation += WHEEL_SPEED
            self.wheel_animation %= 2
            self.draw_rover_ground()
        else:
            if self.jumping:
                self.jump(None)
            else:
                self.y_vel += G / 60
            self.y_pos += self.y_vel
            self.draw_rover_air()

    def draw_rover_ground(self):
        wheel_size = WHEEL_SIZE/2
        wheels_pos_x = [wheel_size / 2, wheel_size + 4 + wheel_size / 2, ROVER_SIZE - 4 - wheel_size / 2]
        wheels_pos_y = [game.get_game().terrain.get_y_at(self.x_pos + x) for x in wheels_pos_x]
        average_wheel_pos = sum(wheels_pos_y) / 3
        wheels_pos_y = [max(min(y, average_wheel_pos + 10), average_wheel_pos - 10) for y in wheels_pos_y]
        player_height = average_wheel_pos - 110
        self.y_pos = player_height + 110
        wheel_num = int(self.wheel_animation)

        self.rect = (self.x_pos, player_height, ROVER_SIZE, ROVER_SIZE)
        self.image = self.chassis_images[0].copy()
        self.image.blit(self.big_wheels_images[wheel_num], (wheels_pos_x[0] - wheel_size / 2,
                                                            wheels_pos_y[0] - player_height - wheel_size))
        self.image.blit(self.big_wheels_images[wheel_num], (wheels_pos_x[1] - wheel_size / 2,
                                                            wheels_pos_y[1] - player_height - wheel_size))
        self.image.blit(self.small_wheel_images[wheel_num], (wheels_pos_x[2] - wheel_size / 2,
                                                             wheels_pos_y[2] - player_height - wheel_size))

    def draw_rover_air(self):
        image_num = 2 if self.y_vel > 0 else 1

        self.rect = (self.x_pos, self.y_pos - 110, ROVER_SIZE, ROVER_SIZE)
        self.image = self.chassis_images[image_num].copy()
