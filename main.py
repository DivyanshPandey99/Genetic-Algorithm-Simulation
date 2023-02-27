import pygame
from parameters import *
from food import *
from prey import *
from prey_herd import *
from poison import *
from predator_herd import *

pygame.init()


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Genetic Algorithm")
clock = pygame.time.Clock()


foods = Food()
poisons = Poison()
preys = Preys()
predators = Predators()
run = True
while(run):
    clock.tick(60)
    screen.fill(gray)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    preys.draw(screen)
    predators.draw(screen)
    foods.draw(screen)
    poisons.draw(screen)
    preys.update(foods,poisons,predators)
    predators.update(preys,foods)
    pygame.display.update()

pygame.quit()
