import pygame
import random
from parameters import *
from vector import *


class Predator:
    def __init__(self, position=Vector()):
        self.position = position
        self.health = 1.0
        self.predatorsize = random.randint(8,13)
        self.velocity = Vector(1,1)
        self.acceleration = Vector(0,0)
        self.angle = self.velocity.Heading()
        self.maxspeed = 15/self.predatorsize
        self.maxforce = 0.2
        self.dna = DNA()


    def update(self):
        self.health -= predatorhealthtimer
        self.velocity = Vector.__add__(self.velocity,self.acceleration)
        if(self.velocity.Magnitude()>self.maxspeed):
            self.velocity = self.velocity.Scale(self.maxspeed)
        self.position = Vector.__add__(self.position,self.velocity)
        self.boundaries()
        # Reset Acceleration
        self.acceleration = Vector(0,0)
        # Update angle
        self.angle = self.velocity.Heading()

    # Applies the force returned from eat function
    def behaviors(self,preyherd):
        steerfood = self.eat(preyherd, self.dna.huntperception)

        steerfood = Vector.__mul__(steerfood,self.dna.huntforce)

        self.applyForce(steerfood)

    # returns the force from seek function
    def eat(self,list, perception):
        record = 5000 # minimum distance
        closest = -1  # index of minimum distance
        for i in range(len(list)):
            d = Vector.GetDistance(self.position,list[i].position)
            if(d<record and d<perception):
                record = d
                closest = i
        #Eating
        if(record<5):

            #If prey is small, not able to eat most of the time
            if(1.5*self.predatorsize<prey_size):
                # Predator can't eat 95% of time if its size is small
                if(random.random()<0.9):
                    return Vector(0,0)
            else:
                #Predator can't eat preys 60% of the time
                if(random.random()<0.5):
                    return Vector(0,0)    
            # Health changes by a factor of absorption power present in predator's DNA
            self.health += (list[closest].health/self.dna.absorption)

            list.pop(closest)
            
            #self.health = min(1,self.health)
        elif(closest>-1):
            return self.seek(list[closest].position)

        return Vector(0,0)


    # returns force to reach particular target
    def seek(self, target):
        # Desired velocity
        desired = Vector.__sub__(target,self.position)
        desired = desired.Scale(self.maxspeed)

        # Steering Force
        steer = Vector.__sub__(desired,self.velocity)
        if(steer.Magnitude()>self.maxforce):
            steer = steer.Scale(self.maxforce)
        
        
        return steer



    def applyForce(self,force):
        self.acceleration = Vector.__add__(self.acceleration,force)
        if(self.acceleration.Magnitude()>self.maxforce):
            self.acceleration = self.acceleration.Scale(self.maxforce)

    def clone(self):
        if(random.random()<0.0012):
            clone = Predator(self.position)
            clone.health = 1
            clone.dna = self.dna
            clone.velocity = Vector.__mul__(self.velocity,-1)
            return clone

    #def mutate(self):


    def isDead(self):
        return self.health<=0

    def boundaries(self):
        d = padding
        desired = None
        
        if(self.position.x<d):
            self.velocity = Vector(abs(self.velocity.x),self.velocity.y)
        elif(self.position.x>width-d):
            self.velocity = Vector(-abs(self.velocity.x),self.velocity.y)

        if(self.position.y<d):
            self.velocity = Vector(self.velocity.x,abs(self.velocity.y))
        elif(self.position.y>height-d):
            self.velocity = Vector(self.velocity.x, -abs(self.velocity.y))
    


    def draw(self,screen):
        #pygame.draw.circle(screen,blue,self.position.xy(),6)
        # initialize triangle point
        # rotate point based on the angle
        triangle = [
            ( self.position + Vector(self.predatorsize//2, 0).Rotate(self.angle) ).xy(),
            ( self.position - Vector(self.predatorsize//2, - self.predatorsize/3).Rotate(self.angle) ).xy(),
            ( self.position - Vector(self.predatorsize//2, + self.predatorsize/3).Rotate(self.angle) ).xy()
        ]
        #color = pygame.Color.lerp(lightblue,blue,self.health)
        #pygame.draw.polygon(screen, white, triangle,self.predatorsize//3)
        #pygame.draw.polygon(screen, red, triangle)
        pygame.draw.circle(screen,darkred,self.position.xy(),self.predatorsize)
        pygame.draw.circle(screen,lightred,self.position.xy(),self.predatorsize,2)


class DNA:
    def __init__(self):
        self.huntforce = random.randint(0,5)
        self.huntperception = random.randint(20,150)
        self.absorption = random.randint(2,4)

