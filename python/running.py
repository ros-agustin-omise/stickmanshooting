import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Stickman")
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-3, -1)
        self.gravity = 0.1
        self.lifetime = 20

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class StickmanTarget:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.active = True
        self.hit_radius = 50
        self.animation_frame = 0
        self.running_speed = 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.particles = []

    def update(self):
        if self.active:
            # Move the stickman
            self.x += self.direction_x * self.running_speed
            self.y += self.direction_y * self.running_speed
            
            # Bounce off walls
            if self.x <= 50 or self.x >= WIDTH - 50:
                self.direction_x *= -1
            if self.y <= 50 or self.y >= HEIGHT - 50:
                self.direction_y *= -1
                
            # Keep within bounds
            self.x = max(50, min(WIDTH - 50, self.x))
            self.y = max(50, min(HEIGHT - 50, self.y))
            
            # Update animation
            self.animation_frame += 0.2
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]

    def hit(self):
        if self.active:
            self.active = False
            # Create hit particles
            for _ in range(20):
                particle = Particle(self.x, self.y, (255, 0, 0))
                self.particles.append(particle)
            # Respawn after 3 seconds
            pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    def respawn(self):
        self.active = True
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def draw(self):
        # Draw particles first
        for particle in self.particles:
            particle.draw(screen)
            
        if self.active:
            # Calculate leg positions for running animation
            leg_offset = math.sin(self.animation_frame * 3) * 10
            
            # Body (vertical line)
            pygame.draw.line(screen, BLACK, (self.x, self.y - 20), (self.x, self.y + 10), 3)
            
            # Head (circle)
            pygame.draw.circle(screen, BLACK, (self.x, self.y - 30), 8, 2)
            
            # Arms
            arm_swing = math.sin(self.animation_frame * 3) * 15
            pygame.draw.line(screen, BLACK, (self.x, self.y - 10), (self.x - 15 + arm_swing, self.y), 2)
            pygame.draw.line(screen, BLACK, (self.x, self.y - 10), (self.x + 15 - arm_swing, self.y), 2)
            
            # Legs (animated for running)
            pygame.draw.line(screen, BLACK, (self.x, self.y + 10), (self.x - 10 + leg_offset, self.y + 30), 3)
            pygame.draw.line(screen, BLACK, (self.x, self.y + 10), (self.x + 10 - leg_offset, self.y + 30), 3)

# Create the stickman target
target = StickmanTarget()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = ((mouse_x - target.x)**2 + (mouse_y - target.y)**2)**0.5
            if distance < target.hit_radius and target.active:
                target.hit()
        if event.type == pygame.USEREVENT + 1:
            target.respawn()

    screen.fill(WHITE)

    target.update()
    target.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()