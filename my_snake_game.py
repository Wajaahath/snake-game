import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # Each square in the grid
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]  # Starting position
        self.direction = (GRID_SIZE, 0)  # Moving right

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)  # Add new head
        self.body.pop()  # Remove the last segment (unless eating food)

    def grow(self):
        self.body.append(self.body[-1])  # Adds a new segment at the tail

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:]  # Collision with itself
            or head[0] < 0 or head[0] >= WIDTH  # Collision with walls
            or head[1] < 0 or head[1] >= HEIGHT
        )

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def respawn(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


def main():
    running = True
    snake = Snake()
    food = Food()

    while running:
        screen.fill(BLACK)  # Clear screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))

        # Move snake
        snake.move()

        # Check for collisions
        if snake.check_collision():
            running = False  # End game if collision occurs

        # Check if food is eaten
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()

        # Draw snake and food
        snake.draw(screen)
        food.draw(screen)

        # Refresh screen
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
