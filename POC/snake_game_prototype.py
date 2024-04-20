import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
GRID_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)

# Set up the colors
SNAKE_COLOR = (0, 255, 0)
FRUIT_COLOR = (255, 0, 0)

# Set up the directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set up the game variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT
fruit = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Main game loop
while True:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT

    # Move the snake
    head = snake[0]
    new_head = (head[0] + snake_direction[0], head[1] + snake_direction[1])
    snake.insert(0, new_head)

    # Check for collisions with walls
    if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        pygame.quit()
        sys.exit()

    # Check for collisions with the snake itself
    if len(snake) != len(set(snake)):
        pygame.quit()
        sys.exit()

    # Check for collisions with the fruit
    if new_head == fruit:
        fruit = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

    # Draw the fruit
    pygame.draw.rect(screen, FRUIT_COLOR, (fruit[0] * CELL_SIZE, fruit[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(10)
