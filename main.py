import pygame
import math
import random
import sys
from hand_tracking import HandTracker
from fruit import Fruit

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Fruit Ninja")

clock = pygame.time.Clock()

# ── Colours ───────────────────────────────────────────────────────────────────
BG_COLOR = (30, 30, 30)
WHITE    = (255, 255, 255)
RED      = (220, 50,  50)
GREEN    = (50,  220, 50)
YELLOW   = (255, 220, 0)
ORANGE   = (255, 140, 0)

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_large  = pygame.font.SysFont("Arial", 64, bold=True)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_small  = pygame.font.SysFont("Arial", 28)

# ── Sound helpers ─────────────────────────────────────────────────────────────
def make_beep(freq=440, duration=120, volume=0.3):
    import numpy as np
    sample_rate = 44100
    n = int(sample_rate * duration / 1000)
    t = np.linspace(0, duration / 1000, n, endpoint=False)
    wave = (np.sin(2 * np.pi * freq * t) * 32767 * volume).astype(np.int16)
    stereo = np.column_stack([wave, wave])  # stereo required by pygame
    return pygame.sndarray.make_sound(stereo)

try:
    slice_sound    = make_beep(880, 80,  0.3)
    bomb_sound     = make_beep(200, 300, 0.5)
    gameover_sound = make_beep(150, 600, 0.4)
    print("[OK] Sounds loaded")
except Exception as e:
    print(f"[WARN] Sound disabled: {e}")
    slice_sound = bomb_sound = gameover_sound = None

def play(sound):
    if sound:
        try: sound.play()
        except: pass

# ── Particle system ───────────────────────────────────────────────────────────
FRUIT_COLORS = {
    'apple':      [(220, 50,  50),  (255, 100, 100)],
    'banana':     [(255, 220, 0),   (255, 180, 30)],
    'watermelon': [(50,  200, 80),  (220, 50,  50)],
    'kiwi':       [(80,  160, 50),  (200, 180, 100)],
    'pineapple':  [(255, 200, 0),   (180, 220, 60)],
    'bomb':       [(80,  80,  80),  (40,  40,  40)],
}

class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 9)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(18, 35)
        self.max_life = self.life
        self.radius = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1

    def draw(self, surface):
        r = max(1, int(self.radius * self.life / self.max_life))
        alpha = int(255 * self.life / self.max_life)
        col = (*self.color[:3], alpha)
        surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, col, (r, r), r)
        surface.blit(surf, (int(self.x) - r, int(self.y) - r))

def spawn_particles(x, y, fruit_type, count=20):
    colors = FRUIT_COLORS.get(fruit_type, [(255, 255, 255)])
    return [Particle(x, y, random.choice(colors)) for _ in range(count)]

# ── Trail ─────────────────────────────────────────────────────────────────────
TRAIL_LEN = 12

class Trail:
    def __init__(self):
        self.points = []

    def update(self, x, y):
        if x is not None and y is not None:
            self.points.append((x, y))
            if len(self.points) > TRAIL_LEN:
                self.points.pop(0)
        else:
            self.points.clear()

    def draw(self, surface):
        n = len(self.points)
        for i in range(1, n):
            width = max(1, int(10 * i / n))
            col   = (255, 255, int(200 * i / n))
            pygame.draw.line(surface, col, self.points[i-1], self.points[i], width)

# ── Difficulty ────────────────────────────────────────────────────────────────
def get_difficulty(score):
    if score < 10:
        return 4, 0.10, "Easy",   GREEN
    elif score < 25:
        return 5, 0.18, "Medium", YELLOW
    elif score < 45:
        return 6, 0.25, "Hard",   ORANGE
    else:
        return 7, 0.33, "Insane", RED

# ── Lives display ─────────────────────────────────────────────────────────────
def draw_lives(surface, lives):
    for i in range(lives):
        txt = font_medium.render("♥", True, RED)
        surface.blit(txt, (WIDTH - 45 - i * 38, 10))

# ── Game Over screen ──────────────────────────────────────────────────────────
def game_over_screen(surface, score):
    play(gameover_sound)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title = font_large.render("GAME OVER", True, RED)
    surface.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))

    sc = font_medium.render(f"Final Score: {score}", True, WHITE)
    surface.blit(sc, sc.get_rect(center=(WIDTH//2, HEIGHT//2)))

    hint = font_small.render("Press  R  to Restart   |   ESC to Quit", True, (180, 180, 180))
    surface.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # restart
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

# ── Main game function ────────────────────────────────────────────────────────
def run_game(tracker):
    trail     = Trail()
    fruits    = []
    particles = []
    score     = 0
    lives     = 3

    while True:
        screen.fill(BG_COLOR)

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tracker.release()
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tracker.release()
                    pygame.quit(); sys.exit()

        # ── Hand tracking ──────────────────────────────────────────────────────
        x, y = tracker.get_hand_position()
        trail.update(x, y)
        trail.draw(screen)

        if x is not None and y is not None:
            pygame.draw.circle(screen, GREEN, (x, y), 10)

        # ── Difficulty & spawning ──────────────────────────────────────────────
        max_fruits, bomb_chance, diff_label, diff_color = get_difficulty(score)

        if len(fruits) < max_fruits:
            is_bomb = random.random() < bomb_chance
            fruits.append(Fruit(is_bomb=is_bomb))

        # ── Update fruits ──────────────────────────────────────────────────────
        for fruit in fruits[:]:
            fruit.move()
            fruit.draw(screen)

            # Falls off bottom → just remove, no life penalty
            if fruit.is_off_screen():
                fruits.remove(fruit)

            # Collision with finger tip
            elif x is not None and y is not None:
                dist = math.sqrt((fruit.x - x)**2 + (fruit.y - y)**2)
                if dist < fruit.radius + 10:
                    fruits.remove(fruit)
                    particles += spawn_particles(fruit.x, fruit.y, fruit.fruit_type)

                    if fruit.is_bomb:
                        play(bomb_sound)
                        lives -= 1
                        # Red flash
                        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        flash.fill((200, 0, 0, 80))
                        screen.blit(flash, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(120)
                    else:
                        play(slice_sound)
                        score += 1

        # ── Particles ─────────────────────────────────────────────────────────
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        # ── HUD ───────────────────────────────────────────────────────────────
        score_txt = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_txt, (10, 10))

        diff_txt = font_small.render(f"● {diff_label}", True, diff_color)
        screen.blit(diff_txt, (10, 55))

        draw_lives(surface=screen, lives=lives)

        pygame.display.update()
        clock.tick(60)

        # ── Game over check ────────────────────────────────────────────────────
        if lives <= 0:
            pygame.display.update()
            game_over_screen(screen, score)
            return  # restart from main loop

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tracker = HandTracker()   # create camera ONCE — reused across restarts
    while True:
        run_game(tracker)