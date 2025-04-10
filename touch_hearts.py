import pygame
import sys
import random
import math
from pygame import gfxdraw

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clover Moving Like a Fan with Galaxy Effect")

BLACK = (0, 0, 0)
PINK = (255, 105, 180)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
SNOW_COLOR = (255, 255, 255)  # Snowflake color

# --- Galaxy Effect (Stars) ---
class GalaxyEffect:
    def __init__(self):
        self.stars = []
        self.num_stars = 300  # Increase number of stars
        self.create_stars()

    def create_stars(self):
        for _ in range(self.num_stars):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)  # Star size
            opacity = random.randint(100, 255)  # Star opacity
            self.stars.append([x, y, size, opacity])

    def update(self):
        # Move stars slowly to simulate space movement
        for star in self.stars:
            star[1] += 1  # Move stars downwards
            if star[1] > HEIGHT:
                star[1] = 0
            star[0] += random.randint(-1, 1)  # Slight horizontal movement

    def draw(self, surface):
        # Draw Stars with realistic effect
        for star in self.stars:
            pygame.draw.circle(surface, WHITE, (star[0], star[1]), star[2])

# --- Snowflakes ---
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, HEIGHT)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.opacity = random.randint(200, 255)

    def update(self):
        # Snowflake moves downwards
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, SNOW_COLOR, (self.x, self.y), self.size)

# --- Heart Particle Class ---
class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(10, 25)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-3, -1)
        self.gravity = 0.05
        self.opacity = 255
        self.fade_speed = random.randint(3, 6)
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.05, 0.05)
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 255, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 127)
        ]
        self.color = random.choice(self.colors)

    def update(self):
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        self.opacity -= self.fade_speed
        return self.opacity > 0

    def draw(self, surface):
        heart_surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        center_x = heart_surf.get_width() // 2
        center_y = heart_surf.get_height() // 2
        points = []
        for t in range(200):
            t /= 100
            x = 16 * (math.sin(t) ** 3)
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            x *= self.size / 16
            y *= -self.size / 16
            rx = x * math.cos(self.rotation) - y * math.sin(self.rotation)
            ry = x * math.sin(self.rotation) + y * math.cos(self.rotation)
            points.append((center_x + rx, center_y + ry))

        color_with_alpha = (*self.color, max(0, min(255, int(self.opacity))))
        if len(points) > 2:
            gfxdraw.filled_polygon(heart_surf, points, color_with_alpha)
            gfxdraw.aapolygon(heart_surf, points, color_with_alpha)
        surface.blit(heart_surf, (self.x - center_x, self.y - center_y))

# --- Clover + Ribbon with Fan-Like Movement ---
class FanClover:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Initial rotation angle
        self.rotation_speed = 0.05  # Speed of rotation
        self.dx = random.uniform(-0.2, 0.2)  # Slow horizontal movement
        self.dy = random.uniform(-0.2, 0.2)  # Slow vertical movement
        self.leaf_size = 40
        self.offset = 30

        # Load a stylish font for "Rakshyanda"
        self.font = pygame.font.Font("freesansbold.ttf", 48)  # You can change this to any font you prefer
        self.text = self.font.render('Rakshyanda', True, WHITE)

    def move(self):
        # Slow movement of the clover
        self.x += self.dx
        self.y += self.dy

        # Rotation like a fan
        self.angle += self.rotation_speed

        # Bounce the clover within screen boundaries
        if self.x <= 0 or self.x >= WIDTH:
            self.dx = -self.dx
        if self.y <= 0 or self.y >= HEIGHT:
            self.dy = -self.dy

    def draw(self, surface):
        def draw_leaf(cx, cy, angle):
            points = []
            for t in range(200):
                t /= 100
                px = 16 * (math.sin(t) ** 3)
                py = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                px *= self.leaf_size / 16
                py *= -self.leaf_size / 16
                rx = px * math.cos(angle) - py * math.sin(angle)
                ry = px * math.sin(angle) + py * math.cos(angle)
                points.append((cx + rx, cy + ry))
            if len(points) > 2:
                gfxdraw.filled_polygon(surface, points, GREEN)
                gfxdraw.aapolygon(surface, points, GREEN)

        # 4 leaves
        draw_leaf(self.x, self.y - self.offset, self.angle)
        draw_leaf(self.x + self.offset, self.y, self.angle + math.pi / 2)
        draw_leaf(self.x, self.y + self.offset, self.angle + math.pi)
        draw_leaf(self.x - self.offset, self.y, self.angle + 3 * math.pi / 2)

        # Stem
        pygame.draw.line(surface, GREEN, (self.x, self.y + 10), (self.x, self.y + 50), 6)

        # Pink ribbon
        pygame.draw.ellipse(surface, PINK, (self.x - 20, self.y - 10, 40, 20))
        pygame.draw.line(surface, PINK, (self.x - 10, self.y + 15), (self.x - 20, self.y + 30), 4)
        pygame.draw.line(surface, PINK, (self.x + 10, self.y + 15), (self.x + 20, self.y + 30), 4)

        # Draw "Rakshyanda" text on the clover with shadow
        # Shadow effect
        shadow_text = self.font.render('Rakshyanda', True, (0, 0, 0))  # Black shadow
        surface.blit(shadow_text, (self.x - shadow_text.get_width() // 2 + 3, self.y - 80 + 3))  # Position with slight offset
        surface.blit(self.text, (self.x - self.text.get_width() // 2, self.y - 80))  # Draw the actual text

# --- Main ---
def main():
    clock = pygame.time.Clock()
    hearts = []
    clover = FanClover(WIDTH // 2, HEIGHT // 2)
    galaxy = GalaxyEffect()

    snowflakes = [Snowflake() for _ in range(100)]  # Create 100 snowflakes

    font = pygame.font.SysFont(None, 24)
    info_text = font.render("Click or drag to create hearts", True, (255, 255, 255))
    info_rect = info_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for _ in range(random.randint(3, 7)):
                    hearts.append(Heart(x, y))

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if random.random() > 0.5:
                hearts.append(Heart(x, y))

        # Clear the screen
        screen.fill(BLACK)

        galaxy.update()  # Update galaxy stars
        galaxy.draw(screen)  # Draw galaxy effect

        for snowflake in snowflakes:
            snowflake.update()  # Update snowflakes
            snowflake.draw(screen)  # Draw snowflakes

        clover.move()  # Move and rotate the clover like a fan
        clover.draw(screen)

        hearts = [heart for heart in hearts if heart.update()]
        for heart in hearts:
            heart.draw(screen)

        screen.blit(info_text, info_rect)
        pygame.display.flip()
        clock.tick(60)  # Smooth frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
