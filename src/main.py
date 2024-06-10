import pygame, sys, random
from pygame.math import Vector2
from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    GAME = auto()
    GAME_OVER = auto()

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class OBSTACLE:
    def __init__(self, position):
        self.pos = position

    def draw_obstacle(self):
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (200, 0, 0), obstacle_rect)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load("../Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("../Graphics/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("../Graphics/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("../Graphics/head_right.png").convert_alpha()

        self.tail_up = pygame.image.load("../Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("../Graphics/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("../Graphics/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("../Graphics/tail_right.png").convert_alpha()

        self.body_horizontal = pygame.image.load("../Graphics/body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load("../Graphics/body_vertical.png").convert_alpha()

        self.body_bl = pygame.image.load("../Graphics/body_bl.png").convert_alpha()
        self.body_br = pygame.image.load("../Graphics/body_br.png").convert_alpha()
        self.body_tl = pygame.image.load("../Graphics/body_tl.png").convert_alpha()
        self.body_tr = pygame.image.load("../Graphics/body_tr.png").convert_alpha()
        self.sound = pygame.mixer.Sound("../Sound/crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  # Set an initial direction

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.sound.play()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.obstacles = []
        self.game_state = GameState.MENU
        self.create_obstacles()

    def create_obstacles(self):
        for _ in range(5):  # Create 5 obstacles
            while True:
                obstacle_position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
                if obstacle_position not in self.snake.body and obstacle_position != self.fruit.pos:
                    self.obstacles.append(OBSTACLE(obstacle_position))
                    break

    def update(self):
        if self.game_state == GameState.GAME:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        if self.game_state == GameState.GAME:
            self.draw_grass()
            self.fruit.draw_fruit()
            for obstacle in self.obstacles:
                obstacle.draw_obstacle()
            self.snake.draw_snake()
            self.draw_score()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.MENU:
            self.draw_menu()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_state = GameState.GAME_OVER
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_state = GameState.GAME_OVER
        for obstacle in self.obstacles:
            if self.snake.body[0] == obstacle.pos:
                self.game_state = GameState.GAME_OVER

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_number * cell_size - 60)
        score_y = int(cell_number * cell_size - 60)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (164, 209, 69), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_game_over(self):
        game_over_surface = game_font.render("Game Over", True, (56, 74, 12))
        game_over_rect = game_over_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size / 2 - 50))

        score_text = f"Score: {len(self.snake.body) - 3}"
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2))

        play_again_surface = game_font.render("Play Again? Y/N", True, (56, 74, 12))
        play_again_rect = play_again_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size / 2 + 50))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(play_again_surface, play_again_rect)

    def draw_menu(self):
        menu_surface = game_font.render("Snake Game", True, (56, 74, 12))
        menu_rect = menu_surface.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2 - 50))

        start_surface = game_font.render("Press SPACE to Start", True, (56, 74, 12))
        start_rect = start_surface.get_rect(center=(cell_number * cell_size / 2, cell_number * cell_size / 2))

        screen.blit(menu_surface, menu_rect)
        screen.blit(start_surface, start_rect)

    def reset(self):
        self.snake.reset()
        self.fruit.randomize()
        self.obstacles = []
        self.create_obstacles()
        self.game_state = GameState.GAME

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_size * cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load("../Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font('../Font/Reach-Fill&Outline.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and main_game.game_state == GameState.GAME:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if main_game.game_state == GameState.GAME:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            elif main_game.game_state == GameState.GAME_OVER:
                if event.key == pygame.K_y:
                    main_game.reset()
                if event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
            elif main_game.game_state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    main_game.reset()

    screen.fill((174, 245, 93))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(120)
