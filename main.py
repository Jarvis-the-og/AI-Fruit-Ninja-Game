import pygame
from hand_tracking import HandTracker
from fruit import Fruit
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Gesture Fruit Ninja")

tracker = HandTracker()

fruits = []
score = 0

clock = pygame.time.Clock()

while True:

    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get finger position
    x,y = tracker.get_hand_position()

    if x and y:
        pygame.draw.circle(screen,(0,255,0),(x,y),10)

    # Spawn fruits
    if len(fruits) < 5:
        fruits.append(Fruit())

    for fruit in fruits:

        fruit.move()
        fruit.draw(screen)

        if x and y:

            distance = math.sqrt((fruit.x-x)**2 + (fruit.y-y)**2)

            if distance < fruit.radius:

                fruits.remove(fruit)
                score += 1

    # Display score
    font = pygame.font.SysFont(None,40)
    text = font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(text,(10,10))

    pygame.display.update()

    clock.tick(60)