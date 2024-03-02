import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
COL = (123, 111, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)  # Grey color for roads
BALL_RADIUS = 10
FPS = 60

# Assuming you have loaded the hero image
hero_image = pygame.image.load("hero.png")
# Load wall image
wall_image = pygame.image.load("wall.png")
BALL_RADIUS = 15
HERO_SIZE = (30, 30)  # Adjust the size of the hero image

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map with Roads and Ball")
clock = pygame.time.Clock()

# Define road areas (x, y, width, height)
original_roads = [
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

# Timer variables
start_time = pygame.time.get_ticks()
display_time = 5000  # 5 seconds in milliseconds

# Player status
player_out = False

# Main game loop
running = True
display_complete = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Check if display time is over
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= display_time:
        display_complete = True

    # Move the ball only when the screen turns black and the player is not out
    if display_complete and not player_out:
        if keys[pygame.K_RIGHT]:
            ball_x += ball_velocity
        elif keys[pygame.K_LEFT]:
            ball_x -= ball_velocity
        elif keys[pygame.K_DOWN]:
            ball_y += ball_velocity
        elif keys[pygame.K_UP]:
            ball_y -= ball_velocity

    # Check if the ball touches any road
    for road in original_roads:
        road_rect = pygame.Rect(road)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if road_rect.colliderect(ball_rect) and display_complete:
            # Player is out if hits the road
            player_out = True

    # Draw background
    screen.fill(BLACK if display_complete else COL)

    # Draw roads if display time is not over
    if not display_complete:

        for road in original_roads:
            pygame.draw.rect(screen, GREY, road)

        # Draw starting and ending points
        pygame.draw.rect(screen, RED, (10, 10, 100, 50))
        font = pygame.font.SysFont(None, 32)
        start_text = font.render("Start", True, WHITE)
        screen.blit(start_text, (20, 20))

        pygame.draw.rect(screen, RED, (WIDTH - 110, HEIGHT - 60, 100, 50))
        end_text = font.render("End", True, WHITE)
        screen.blit(end_text, (WIDTH - 100, HEIGHT - 50))


    


    # Draw ball if the player is not out
    if not player_out:
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
            # Draw the hero image at the ball's position with the adjusted size
        hero_resized = pygame.transform.scale(hero_image, HERO_SIZE)
        screen.blit(hero_resized, (ball_x - BALL_RADIUS, ball_y - BALL_RADIUS))

    # Display "Player is out" if the player hits a grey road
    if player_out:
        font_out = pygame.font.SysFont(None, 64)
        out_text = font_out.render("Player is out", True, WHITE)
        screen.blit(out_text, (WIDTH // 2 - 200, HEIGHT // 2))
        ball_x = 30
        ball_y = 30
        restart_text = font_out.render("Press R to restart", True, WHITE)


        screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 50))

        # Check for restart option
        if keys[pygame.K_r]:
            player_out = False
            start_time = pygame.time.get_ticks()
            display_complete = False


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
