import pygame
import random
from parameters import *
from vector import *
class Poison:
    def __init__(self):
        self.poisoncount = 12
        self.poisonlist = self.initializePoisons()
        

    def initializePoisons(self):
        poisonlist = []
        for i in range(self.poisoncount):
            poisonlist.append(Vector(random.randint(padding,width-padding),random.randint(padding,height-padding)))
        return poisonlist


    def draw(self,screen):
        if(random.random()<0.008):
            self.poisonlist.append(Vector(random.randint(padding,width-padding),random.randint(padding,height-padding)))
        for poison in self.poisonlist:
            pygame.draw.circle(screen,red,poison.xy(),2)