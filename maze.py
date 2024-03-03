import pygame
import sys
import time

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
COL = (123, 111, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (169, 169, 169)  # Grey color for roads
BALL_RADIUS = 15
FPS = 60

image_path = "logo.jpg"  # Replace with the path to your image
background_image = pygame.image.load(image_path)
start_logo = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map with Roads and Ball")
clock = pygame.time.Clock()

# Load hero image
hero_image = pygame.image.load("hero.png")
HERO_SIZE = (30, 30)  # Adjust the size of the hero image

# Define road areas (x, y, width, height) for each level
levels = [
    [
        (100, 200, 600, 40),
        (300, 100, 40, 400),
        (500, 300, 200, 40),
        (50, 350, 200, 30),
        (400, 50, 30, 200)
    ],
    [
        (10, 600, 60, 40),
        (100, 300, 420, 40),
        (350, 30, 20, 40),
        (510, 30, 100, 30),
        (0, 500, 300, 120)
    ],
    [
        (350, 20, 100, 40),
        (300, 50, 400, 40),
        (550, 30, 100, 400),
        (510, 350, 245, 130),
        (40, 350, 300, 20),
        (100, 30, 100, 30),
        (0, 100, 30, 10)
    ],
    [
        (101, 20, 16, 410),
        (210, 330, 20, 240),
        (333, 333, 210, 430),
        (10, 50, 10, 300),
        (190, 0, 30, 20),
        (333, 0, 210, 270)
    ],
    [
        (121, 60, 10, 40),
        (20, 373, 220, 40),
        (383, 33, 20, 40),
        (70, 550, 100, 30),
        (10, 100, 30, 20),
        (3, 220, 20, 70),
        (421, 60, 10, 40),
        (320, 373, 220, 40),
        (683, 33, 20, 40),
        (370, 550, 100, 30),
        (310, 100, 30, 20),
        (53, 220, 20, 70),
        (333, 520, 20, 70),
        (421, 560, 10, 40),
        (320, 773, 220, 40),
        (383, 333, 200, 400),
        (170, 50, 100, 300),
        (210, 200, 300, 200),
        (761, 460, 40, 100),
        (620, 573, 100, 40),
        (730, 350, 400, 400),
        (620,500,60,60)
    ],
    # Add other levels here
]

# End box position for each level
end_boxes = [
    pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 50)
    # Add end box positions for other levels here
]*len(levels)

# Ball position and velocity
ball_x = 30
ball_y = 30
ball_velocity = 5

# Timer variables
start_time = pygame.time.get_ticks()
display_time = 500  # 5 seconds in milliseconds

# Player status
player_out = False
level_completed = False
end_reached = False  # New variable to track end reached state

# Level index
current_level = 0
start=True
# Main game loop
running = True
display_complete = False
while running:
    font = pygame.font.SysFont(None, 32)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    keys = pygame.key.get_pressed()
    level_time=15*1000
    if start:
        screen.blit(start_logo, (0, 0))
        font_out = pygame.font.SysFont(None, 64)
        out_text = font_out.render("Hold Space to start", True, WHITE)
        screen.blit(out_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(start_logo, (0, 0))
        out_text = font_out.render("", True, WHITE)
        pygame.display.flip()
        time.sleep(.5)
        if keys[pygame.K_SPACE] :
            start=False
            start_time = pygame.time.get_ticks()
            display_complete = False

    # Check if display time is over
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= display_time:
        display_complete = True
        
    if current_time - start_time >= level_time:
        player_out=True

    # Move the ball only when the screen turns black, the player is not out, and the end is not reached
    if display_complete and not player_out and not end_reached and not start:
        if keys[pygame.K_RIGHT] and ball_x + BALL_RADIUS + ball_velocity < WIDTH:
            ball_x += ball_velocity
        elif keys[pygame.K_LEFT] and ball_x - BALL_RADIUS - ball_velocity > 0:
            ball_x -= ball_velocity
        elif keys[pygame.K_DOWN] and ball_y + BALL_RADIUS + ball_velocity < HEIGHT:
            ball_y += ball_velocity
        elif keys[pygame.K_UP] and ball_y - BALL_RADIUS - ball_velocity > 0:
            ball_y -= ball_velocity

    # Check if the ball reaches the end box
    if end_boxes[current_level].collidepoint(ball_x, ball_y) and display_complete:
        level_completed = True
        end_reached = True  # Set end reached to True

    # Check if the ball touches any road
    for road in levels[current_level]:
        road_rect = pygame.Rect(road)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if road_rect.colliderect(ball_rect) and display_complete:
            # Player is out if hits the road
            player_out = True

    # Draw background
    if not start:
        screen.fill(BLACK if display_complete else COL)

    # Draw roads if display time is not over
    if not display_complete and not start:
        for road in levels[current_level]:
            pygame.draw.rect(screen, GREY, road)

    # Draw starting and ending points
    if not start:
        pygame.draw.rect(screen, RED, (10, 10, 100, 50))
        font = pygame.font.SysFont(None, 32)
        start_text = font.render("Start", True, WHITE)
        screen.blit(start_text, (20, 20))

        pygame.draw.rect(screen, RED, end_boxes[current_level])
        end_text = font.render("End", True, WHITE)
        screen.blit(end_text, (WIDTH - 100, HEIGHT - 50))

        pygame.draw.rect(screen, RED, (1,10,100,50))
        end_text = font.render(str("Level "+str(current_level+1)), True, WHITE)
        screen.blit(end_text, (WIDTH - 100,50))

    
        if not level_completed or not player_out:
            pygame.draw.rect(screen, RED, (1,10,100,50))
            end_text = font.render(str("Time Left "+str((current_time-start_time)/1000)), True, WHITE)
            screen.blit(end_text, (WIDTH - 300,50))

    # Draw ball if the player is not out
    if not player_out:
        # Draw the hero image at the ball's position with the adjusted size
        hero_resized = pygame.transform.scale(hero_image, HERO_SIZE)
        hero_rect = hero_resized.get_rect(center=(ball_x, ball_y))
        if not start:
            screen.blit(hero_resized, hero_rect)

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

    # Display "Level Completed" if the ball reaches the end box
    if level_completed:
        font_level = pygame.font.SysFont(None, 64)
        level_text = font_level.render("Level Completed", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - 200, HEIGHT // 2))
        next_level_text = font_level.render("Press N for next level", True, WHITE)
        screen.blit(next_level_text, (WIDTH // 2 - 250, HEIGHT // 2 + 50))

        # Check for next level option
        if keys[pygame.K_n]:
            ball_x = 30
            ball_y = 30
            player_out = False
            level_completed = False
            start_time = pygame.time.get_ticks()
            display_complete = False
            end_reached=False
            current_level = (current_level + 1) % len(levels)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
