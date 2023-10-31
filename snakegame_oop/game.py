import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 500, 400
SNAKE_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directional constants
UP = (0, -SNAKE_SIZE)
DOWN = (0, SNAKE_SIZE)
LEFT = (-SNAKE_SIZE, 0)
RIGHT = (SNAKE_SIZE, 0)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = RIGHT

    def move(self, food):
        head = self.body[0]
        x, y = head
        dx, dy = self.direction
        new_head = ((x + dx) % WIDTH, (y + dy) % HEIGHT)

        # Check if the new head coincides with food
        if new_head == food.position:
            self.body.insert(0, new_head)
            food.randomize_position()  # Randomize new food position
            return True
        else:
            self.body.insert(0, new_head)
            self.body.pop()  # Remove the tail if no food is eaten
            return False

    def change_direction(self, new_direction):
        if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    def check_collision(self):
        return self.body[0] in self.body[1:]

    def check_boundaries(self):
        return (
            self.body[0][0] < 0
            or self.body[0][0] >= WIDTH
            or self.body[0][1] < 0
            or self.body[0][1] >= HEIGHT
        )

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))


class Food:
    def __init__(self):
        self.position = (random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE,
                         random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE)

    def randomize_position(self):
        self.position = (random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE,
                         random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, SNAKE_SIZE, SNAKE_SIZE))


class GameOverScreen:
    def __init__(self, width, height, score):
        self.width = width
        self.height = height
        self.score = score

    def display(self, screen):
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Your Score: {self.score}", True, WHITE)
        press_space_text = font.render("Press Space to Start New Game", True, WHITE)

        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
        score_rect = score_text.get_rect(
            center=(self.width // 2, (self.height // 2) + 50)
        )
        press_space_rect = press_space_text.get_rect(
            center=(self.width // 2, (self.height // 2) + 100)
        )

        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(press_space_text, press_space_rect)
        pygame.display.update()


class SnakeGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        clock = pygame.time.Clock()
        running = True
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)

            if not game_over:
                if self.snake.move(self.food):
                    self.score += 10

                    # Increase speed every 100 points
                    if self.score % 100 == 0:
                        global FPS
                        FPS += 2

                if self.snake.check_collision() or self.snake.check_boundaries():
                    game_over = True
            else:
                game_over_screen = GameOverScreen(self.width, self.height, self.score)
                game_over_screen.display(screen)

                # Wait for space bar to start a new game
                waiting_for_space = True
                while waiting_for_space:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_space = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.__init__()  # Reset the game
                                game_over = False
                                waiting_for_space = False

            screen.fill(BLACK)
            self.snake.draw(screen)
            self.food.draw(screen)
            self.display_score(screen)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()  # Exit the program after the game over

    def display_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
