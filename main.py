import pygame
import eventmanager
from game import Game
from menu import Menu
pygame.init()

size = (1400, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moon Patrol")


def goto_menu():
    global current_scene
    current_scene = menu


def goto_game():
    global current_scene
    current_scene = Game(screen)


menu = Menu(screen, goto_game)
current_scene = menu

done = False
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        eventmanager.execute_events(event)

    current_scene.tick()
    current_scene.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
