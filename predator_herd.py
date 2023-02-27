import pygame
import random
from parameters import *
from vector import *
from predator import *
from food import *

class Predators:
    def __init__(self):
        self.predatorcount = 50 #initial count
        self.predatorherd = self.initialiseHerd() #list


    def initialiseHerd(self):
        predatorherd = []
        for i in range(self.predatorcount):
            predatorherd.append(Predator(Vector(random.randint(0,width),random.randint(0,height))))

        return predatorherd

    def update(self,preys,foods):
        for i in reversed(range(len(self.predatorherd))):
            predator = self.predatorherd[i]
            predator.behaviors(preys.preyherd)

            #prey.eat(poisons.poisonlist)

            clone = predator.clone()
            if(clone!=None):
                self.predatorherd.append(clone)

            if(predator.isDead()):
                foods.foodlist.append(Vector(predator.position.x,predator.position.y))
                self.predatorherd.pop(i)
                
            
            predator.update()
            

    def draw(self,screen):
        for predator in self.predatorherd:
            predator.draw(screen)