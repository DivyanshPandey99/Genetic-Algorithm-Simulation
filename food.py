import pygame
import random
from parameters import *
from vector import *
class Food:
    def __init__(self):
        self.foodcount = 60
        self.foodlist = self.initializeFoods()
        

    def initializeFoods(self):
        foodlist = []
        for i in range(self.foodcount):
            foodlist.append(Vector(random.randint(padding,width-padding),random.randint(padding,height-padding)))
        return foodlist


    def draw(self,screen):
        if(random.random()<0.1):
            self.foodlist.append(Vector(random.randint(padding,width-padding),random.randint(padding,height-padding)))
        for food in self.foodlist:
            pygame.draw.circle(screen,green,food.xy(),2)