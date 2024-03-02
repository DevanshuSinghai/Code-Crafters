import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)  # Grey color for roads
BALL_RADIUS = 10
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map with Roads and Ball")
clock = pygame.time.Clock()

# Define road areas (x, y, width, height)
roads = [
    (100, 200, 600, 40),
    (300, 100, 40, 400),
    (500, 300, 200, 40),
    (50, 350, 200, 30),
    (400, 50, 30, 200)
]

# Ball position and velocity
ball_x = 30
ball_y = 30
ball_velocity = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move the ball
    if keys[pygame.K_RIGHT]:
        ball_x += ball_velocity
    elif keys[pygame.K_LEFT]:
        ball_x -= ball_velocity
    elif keys[pygame.K_DOWN]:
        ball_y += ball_velocity
    elif keys[pygame.K_UP]:
        ball_y -= ball_velocity

    # Check if the ball touches any road
    for road in roads:
        road_rect = pygame.Rect(road)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if road_rect.colliderect(ball_rect):
            # Reset ball position to start
            ball_x = 30
            ball_y = 30

    # Draw background
    screen.fill(BLACK)

    # Draw roads
    for road in roads:
        pygame.draw.rect(screen, GREY, road)

    # Draw starting and ending points
    pygame.draw.rect(screen, RED, (10, 10, 100, 50))
    font = pygame.font.SysFont(None, 32)
    start_text = font.render("Start", True, WHITE)
    screen.blit(start_text, (20, 20))

    pygame.draw.rect(screen, RED, (WIDTH - 110, HEIGHT - 60, 100, 50))
    end_text = font.render("End", True, WHITE)
    screen.blit(end_text, (WIDTH - 100, HEIGHT - 50))

    # Draw ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()