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

prev_x = None
prev_y = None

while True:

    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get finger position
    x,y = tracker.get_hand_position()
    prev_x, prev_y = None, None

    # Get finger position
    x, y = tracker.get_hand_position()

    if x is not None and y is not None:
        pygame.draw.circle(screen,(0,255,0),(x,y),10)

        if prev_x is not None and prev_y is not None:
            pygame.draw.line(screen,(255,255,255),(prev_x,prev_y),(x,y),12)

        prev_x = x
        prev_y = y

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