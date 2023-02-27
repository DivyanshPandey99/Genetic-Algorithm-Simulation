import pygame
import random
from parameters import *
from vector import *


class Prey:
    def __init__(self, position=Vector()):
        self.position = position
        self.health = 1.0
        #self.dna
        self.velocity = Vector(2,2)
        self.acceleration = Vector(0,0)
        self.angle = self.velocity.Heading()
        self.maxspeed = 3
        self.maxforce = 0.2
        self.dna = DNA()


    def update(self):
        self.health -= healthtimer
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
    def behaviors(self,food,poison, predatorherd):
        steerfood = self.eat(food, food_nutrition, self.dna.foodperception)
        steerpoison = self.eat(poison, poison_nutrition, self.dna.poisonperception)
        #Force to be applied iff dna has chasepower
        steerrun = Vector(0,0)
        if(self.dna.chasepower!=0):
            steerrun = self.run(predatorherd,self.dna.predatorperception)
        

        steerfood = Vector.__mul__(steerfood,self.dna.foodforce)
        steerpoison = Vector.__mul__(steerpoison,self.dna.poisonforce)
        steerrun = Vector.__mul__(steerrun,-1)

        self.applyForce(steerfood)
        self.applyForce(steerpoison)
        if(random.random()<0.6):
            self.applyForce(steerrun)

    # returns the force from seek function
    def eat(self,list, nutrition, perception):
        record = 5000 # minimum distance
        closest = -1  # index of minimum distance
        for i in range(len(list)):
            d = Vector.GetDistance(self.position,list[i])
            if(d<record and d<perception):
                record = d
                closest = i
        #Eating
        if(record<5):
            list.pop(closest)
            self.health+=nutrition
            #self.health = min(1,self.health)
        elif(closest>-1):
            return self.seek(list[closest])

        return Vector(0,0)
    

    # Force applied when preadtor is near
    def run(self,list, perception):
        record = 5000 # minimum distance
        closest = -1  # index of minimum distance
        for i in range(len(list)):
            d = Vector.GetDistance(self.position,list[i].position)
            if(d<record and d<perception):
                record = d
                closest = i
        #Eating
        if(record<5):
            return Vector(0,0)
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
        if(random.random()<0.002):
            clone = Prey(self.position)
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
        """
        if(self.position.x<d):
            desired = Vector(self.maxspeed,self.velocity.y)
        elif(self.position.x>width-d):
            desired = Vector(-self.maxspeed,self.velocity.y)

        if(self.position.y<d):
            desired = Vector(self.velocity.x,self.maxspeed)
        elif(self.position.y>height-d):
            desired = Vector(self.velocity.x, - self.maxspeed)
        
        if(desired!=None):
            desired = desired.Scale(self.maxspeed)
            steerforce = Vector.__sub__(desired,self.velocity)
            if(steerforce.Magnitude()>self.maxforce):
                steerforce = steerforce.Scale(self.maxforce)
            self.applyForce(steerforce)
        """
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
            ( self.position + Vector(prey_size//2, 0).Rotate(self.angle) ).xy(),
            ( self.position - Vector(prey_size//2, - prey_size/3).Rotate(self.angle) ).xy(),
            ( self.position - Vector(prey_size//2, + prey_size/3).Rotate(self.angle) ).xy()
        ]
        #color = pygame.Color.lerp(lightblue,blue,self.health)
        #pygame.draw.polygon(screen, white, triangle,prey_size//3)
        pygame.draw.polygon(screen, blue, triangle)




class DNA:
    def __init__(self):
        self.foodforce = random.randint(0,5)
        self.poisonforce = random.randint(-2,3)
        self.foodperception = random.randint(20,150)
        self.poisonperception = random.randint(10,100)
        self.predatorperception = random.randint(20,100)
        self.chasepower = 0
        if(random.random()<0.03):
            self.chasepower = 1
        

