import pygame
import random
from parameters import *
from vector import *
from prey import *
from food import *

class Preys:
    def __init__(self):
        self.preycount = 50 #initial count
        self.preyherd = self.initialiseHerd() #list


    def initialiseHerd(self):
        preyherd = []
        for i in range(self.preycount):
            preyherd.append(Prey(Vector(random.randint(0,width),random.randint(0,height))))

        return preyherd

    def update(self,foods,poisons,predators):
        for i in reversed(range(len(self.preyherd))):
            prey = self.preyherd[i]
            prey.behaviors(foods.foodlist,poisons.poisonlist, predators.predatorherd)

            #prey.eat(poisons.poisonlist)

            clone = prey.clone()
            if(clone!=None):
                self.preyherd.append(clone)

            if(prey.isDead()):
                foods.foodlist.append(Vector(prey.position.x,prey.position.y))
                self.preyherd.pop(i)
                
            
            prey.update()
            

    def draw(self,screen):
        for prey in self.preyherd:
            prey.draw(screen)