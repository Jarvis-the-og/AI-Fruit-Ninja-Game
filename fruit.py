import pygame
import random


class Fruit:
    # Fruit types available
    FRUIT_TYPES = ['apple', 'banana', 'watermelon', 'kiwi', 'pineapple']

    def __init__(self, is_bomb=False):
        self.is_bomb = is_bomb
        self.sliced = False

        if self.is_bomb:
            self.fruit_type = 'bomb'
            try:
                self.image = pygame.image.load('assets/bomb.png')
                self.image = pygame.transform.scale(self.image, (60, 60))
            except:
                # Fallback: draw a black circle if no bomb image
                self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.circle(self.image, (20, 20, 20), (30, 30), 30)
                pygame.draw.circle(self.image, (80, 80, 80), (30, 30), 30, 3)
                font = pygame.font.SysFont(None, 28)
                txt = font.render("💣", True, (255, 255, 255))
                self.image.blit(txt, (10, 10))
        else:
            self.fruit_type = random.choice(self.FRUIT_TYPES)
            self.image = pygame.image.load(f'assets/{self.fruit_type}.png')
            self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.radius = 35  # collision radius

        # Spawn from bottom at random x
        self.x = float(random.randint(80, 720))
        self.y = float(650)

        # Upward velocity + slight horizontal drift
        self.vel_y = -random.uniform(10, 15)
        self.vel_x = random.uniform(-2, 2)
        self.gravity = 0.25

        self.rect.center = (int(self.x), int(self.y))

    def move(self):
        """Apply gravity arc movement"""
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (int(self.x), int(self.y))

    def is_off_screen(self):
        return self.y > 680

    def draw(self, screen):
        screen.blit(self.image, self.rect)