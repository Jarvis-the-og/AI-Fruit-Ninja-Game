import pygame
import random

class Fruit:

    def __init__(self):

        self.x = random.randint(100,700)
        self.y = 0
        self.speed = random.randint(3,7)
        self.radius = 30

    def move(self):
        self.y += self.speed

    def draw(self,screen):
        pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.radius)