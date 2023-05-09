import pygame
import random
import sys
from pygame.locals import *

# Initialize the pygame library
pygame.init()

# Set up the game window
screen_width = 900
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blicky Block")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the square
square_size = 25
square_speed = 5

# Set up the projectiles
projectile_speed = 3
projectile_size = 6

# Set up the font for displaying the round
font = pygame.font.Font(None, 36)

def draw_text(text, pos):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, pos)

def draw_square(pos, size):
    pygame.draw.rect(screen, WHITE, (pos[0], pos[1], size, size))

def draw_projectile(pos, size, color):
    pygame.draw.rect(screen, color, (pos[0], pos[1], size, size))

def spawn_projectile(is_red=False):
    edge = random.randint(0, 3)
    center = [screen_width // 2, screen_height // 2]

    if edge == 0:  # Top edge
        pos = [random.randint(0, screen_width - projectile_size), 0]
    elif edge == 1:  # Right edge
        pos = [screen_width - projectile_size, random.randint(0, screen_height - projectile_size)]
    elif edge == 2:  # Bottom edge
        pos = [random.randint(0, screen_width - projectile_size), screen_height - projectile_size]
    else:  # Left edge
        pos = [0, random.randint(0, screen_height - projectile_size)]

    direction = [center[0] - pos[0], center[1] - pos[1]]
    distance = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
    normalized_direction = [direction[0] / distance, direction[1] / distance]

    speed = [int(normalized_direction[0] * projectile_speed), int(normalized_direction[1] * projectile_speed)]

    if not is_red:
        speed[0] += random.randint(-1, 1)
        speed[1] += random.randint(-1, 1)

    return pos, speed

def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    replay_text = font.render("Press Enter to play again, Esc to quit", True, WHITE)
    replay_rect = replay_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
    screen.blit(replay_text, replay_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    main()


def main():
    global square_size, projectile_speed, projectile_size

    square_size = 25  # Reset square size
    projectile_size = 5  # Reset projectile size

    square_pos = [screen_width // 2 - square_size // 2, screen_height // 2 - square_size // 2]
    projectiles = []
    rounds_survived = 0
    projectiles_to_survive = 10
    projectiles_dodged = 0
    red_ball_spawned = False
    red_ball_threshold = random.randint(1, projectiles_to_survive // 2)
    base_spawn_rate = 0.02

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            square_pos[0] -= square_speed
        if keys[K_RIGHT]:
            square_pos[0] += square_speed
        if keys[K_UP]:
            square_pos[1] -= square_speed
        if keys[K_DOWN]:
            square_pos[1] += square_speed

        # Keep the square within the screen
        square_pos[0] = max(0, min(screen_width - square_size, square_pos[0]))
        square_pos[1] = max(0, min(screen_height - square_size, square_pos[1]))

        draw_square(square_pos, square_size)

        # Update and draw projectiles
        survived_projectiles = []
        for pos, speed, color in projectiles:
            pos[0] += speed[0]
            pos[1] += speed[1]

            draw_projectile(pos, projectile_size, color)

            # Check for collisions
            if (pos[0] + projectile_size > square_pos[0] and pos[0] - projectile_size < square_pos[0] + square_size and
                pos[1] + projectile_size > square_pos[1] and pos[1] - projectile_size < square_pos[1] + square_size):
                if color == RED:
                    square_size //= 1.5
                else:
                    game_over_screen()
            else:
                if 0 <= pos[0] <= screen_width and 0 <= pos[1] <= screen_height:
                    survived_projectiles.append((pos, speed, color))
                else:
                    projectiles_dodged += 1

        projectiles = survived_projectiles

        # Check for round completion
        if projectiles_dodged >= projectiles_to_survive:
            rounds_survived += 1
            projectiles_to_survive = 10 + rounds_survived * 10
            projectiles_dodged = 0
            red_ball_spawned = False
            red_ball_threshold = random.randint(1, projectiles_to_survive // 2)
            square_size *= 2
            projectile_size = int(projectile_size * 1.1)
            projectile_speed += 1
            base_spawn_rate += 0.01  # Increase spawn rate each round

            # Reset the square to the center
            square_pos = [screen_width // 2 - square_size // 2, screen_height // 2 - square_size // 2]

            # Reset the projectiles
            projectiles = []

        # Spawn projectiles
        if random.random() < base_spawn_rate:
            white_balls_spawned = sum(1 for _, _, color in projectiles if color == WHITE)

            if not red_ball_spawned and white_balls_spawned >= red_ball_threshold:
                projectile_color = RED
                pos, speed = spawn_projectile(is_red=True)
                red_ball_spawned = True
            else:
                projectile_color = WHITE
                pos, speed = spawn_projectile()

            projectiles.append((pos, speed, projectile_color))
            
        # Draw the current round on the screen
        draw_text(f"Round: {rounds_survived}", (10, 10))

        pygame.display.flip()
        pygame.time.delay(20)

if __name__ == "__main__":
    main()