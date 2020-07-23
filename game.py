import pygame
import random
from opensimplex import OpenSimplex
from terrain import Terrain
from player import Player
from explosion import Explosion
from constants import *
from spritesheet import SpriteSheet
from gameover import GameOver


class Game:
    def __init__(self, screen: pygame.Surface):
        global current_game
        current_game = self
        self.screen = screen

        spritesheet = SpriteSheet('./assets/sprites.png')
        self.life_image = pygame.transform.scale(spritesheet.image_at((423, 345, 16, 8), color_key=-1), (64, 32))
        self.checkpoint_image = pygame.transform.scale(spritesheet.image_at((389, 335, 8, 8), color_key=-1), (32, 32))

        self.simplex = OpenSimplex()
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.next_hole = self.screen.get_width() + random.random() * HOLE_SPACE_VAR
        self.holes = []
        self.checkpoint = 0
        self.checkpoint_score = 0
        self.lives = 3
        self.score = 0
        self.highest_score = 0

        self.terrain = Terrain(screen, MARTIAN_BROWN, self.terrain_point)
        self.all_sprites = pygame.sprite.Group()

        self.player = Player(START_LOCATION, 0)
        self.all_sprites.add(self.player)

    def tick(self):
        if not self.player.dead:
            self.generate_holes()
            self.terrain.move(SCROLL_SPEED)
            self.score += 1
            if self.score > self.highest_score:
                self.highest_score = self.score

            if self.player_collide_with_hole():
                self.explode()

            if self.terrain.x_pos >= self.checkpoint + CHECKPOINT_DISTANCE:
                self.checkpoint += CHECKPOINT_DISTANCE
                self.checkpoint_score = self.score
                self.remove_holes_before_checkpoint()

        self.all_sprites.update()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.terrain.draw()
        self.draw_checkpoints()
        self.all_sprites.draw(self.screen)
        self.draw_hud()

    def explode(self):
        self.all_sprites.remove(self.player)
        self.player.dead = True
        explosion = Explosion(self.player.rect[0] - WHEEL_SIZE / 2, self.player.rect[1], self.take_damage)
        self.all_sprites.add(explosion)

    def take_damage(self, explosion):
        self.all_sprites.remove(explosion)
        if self.lives > 0:
            self.goto_checkpoint()
            self.lives -= 1
        else:
            gameover = GameOver(self.screen.get_width() * 0.2, self.screen.get_height() * 0.2,
                                int(self.screen.get_width() * 0.6), int(self.screen.get_height() * 0.6),
                                self.highest_score, self.reset)
            self.all_sprites.add(gameover)

    def player_collide_with_hole(self):
        if not self.player.on_ground:
            return False
        for hole in self.holes:
            player_x = self.player.x_pos + ROVER_SIZE / 2
            hole_x = hole - self.terrain.x_pos
            if hole_x < player_x and player_x - 50 < hole_x + HOLE_WIDTH:
                return True
        return False

    def draw_checkpoints(self):
        next_checkpoint = CHECKPOINT_DISTANCE - self.terrain.x_pos % CHECKPOINT_DISTANCE - 32
        self.screen.blit(self.checkpoint_image, (next_checkpoint, self.screen.get_height() - 100))

    def draw_hud(self):
        padding = 10

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (padding, padding, score_text.get_width(), score_text.get_height()))

        life_width, life_height = self.life_image.get_size()
        for i in range(self.lives):
            x = self.screen.get_width() - (padding + life_width) * (i + 1)
            y = padding
            self.screen.blit(self.life_image, (x, y, life_width, life_height))

    def generate_holes(self):
        end_x_pos = self.terrain.get_end_pos()
        if end_x_pos > self.next_hole:
            self.holes.append(self.next_hole)
            self.next_hole = self.next_hole + random.random() * HOLE_SPACE_VAR + HOLE_SPACE_MIN
            next_checkpoint = self.checkpoint + CHECKPOINT_DISTANCE
            if (self.next_hole + HOLE_WIDTH > next_checkpoint - HOLE_SPACE_MIN
                    and self.next_hole < next_checkpoint + HOLE_SPACE_MIN):
                self.next_hole = next_checkpoint + CHECKPOINT_SAFE_SPACE

    def terrain_point(self, x):
        y = 200
        for i in range(1, 5):
            y += self.simplex.noise2d(x / (10 * i ** 3), i * 100) * 2 ** i * 3
        new_hole = next((hole for hole in self.holes if hole < x < hole + HOLE_WIDTH), None)
        if new_hole:
            x_root = HOLE_WIDTH / 2
            stretch = HOLE_DEPTH / x_root ** 2
            x_offset = x - new_hole - x_root
            y += stretch * (x_offset + x_root) * (x_offset - x_root)
        return y

    def remove_holes_before_checkpoint(self):
        self.holes = [hole for hole in self.holes if hole > self.checkpoint]

    def goto_checkpoint(self):
        self.score = self.checkpoint_score
        self.player.x_pos = START_LOCATION
        self.terrain.goto(self.checkpoint)
        self.all_sprites.add(self.player)
        self.player.dead = False

    def reset(self, gameover):
        self.all_sprites.remove(gameover)
        self.lives = 3
        self.score = 0
        self.highest_score = 0
        self.next_hole = self.screen.get_width() + random.random() * HOLE_SPACE_VAR
        self.holes = []
        self.terrain.goto(0)
        self.player.x_pos = START_LOCATION
        self.all_sprites.add(self.player)
        self.player.dead = False


current_game: Game = None


def get_game() -> Game:
    if current_game:
        return current_game
