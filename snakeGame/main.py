# SNAKE GAME 1.0
# Using Object Oriented Programming

# Modules required for this project
import pygame
from pygame.locals import *
import time
import random

# Variables required
size = 40
background_color = (173, 231, 146)
width = 1000
height = 1000

# Creates the able object


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("assets/apple.jpg").convert()
        self.cordinate_x = 120
        self.cordinate_y = 120

    def draw(self):
        self.parent_screen.blit(
            self.image, (self.cordinate_x, self.cordinate_y))
        pygame.display.flip()

    def move(self):
        self.cordinate_x = random.randint(0, 23) * size
        self.cordinate_y = random.randint(0, 23) * size


class Snake:
    # Create snake and move controls

    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("assets/block.jpg").convert()
        self.direction = "down"

        self.length = length
        self.cordinate_x = [40] * length
        self.cordinate_y = [40] * length

    def move_left(self):
        if not self.direction == "right":
            self.direction = "left"

    def move_right(self):
        if not self.direction == "left":
            self.direction = "right"

    def move_up(self):
        if not self.direction == "down":
            self.direction = "up"

    def move_down(self):
        if not self.direction == "up":
            self.direction = "down"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.cordinate_x[i] = self.cordinate_x[i - 1]
            self.cordinate_y[i] = self.cordinate_y[i - 1]

        if self.direction == "left":
            self.cordinate_x[0] -= size

        if self.direction == "right":
            self.cordinate_x[0] += size

        if self.direction == "up":
            self.cordinate_y[0] -= size

        if self.direction == "down":
            self.cordinate_y[0] += size

        self.draw()

    def draw(self):
        # self.parent_screen.fill(background_color)

        for i in range(self.length):
            self.parent_screen.blit(
                self.image, (self.cordinate_x[i], self.cordinate_y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.cordinate_x.append(-1)
        self.cordinate_y.append(-1)


class Game:
    # Opens the game window and keep it running until we choose to close
    # Allows in controling snake using the class Snake

    def __init__(self):
        # automatically initialize the whole module
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.background_music()

        self.surface = pygame.display.set_mode((width, height))

        self.snake = Snake(self.surface, 2)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def background_music(self):
        pygame.mixer.music.load("assets/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)

    def sound_effect(self, sound):
        sound = pygame.mixer.Sound(f"assets/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def is_collision(self, cordinate_x1, cordinate_y1, cordinate_x2, cordinate_y2):
        if cordinate_x1 >= cordinate_x2 and cordinate_x1 < cordinate_x2 + size:
            if cordinate_y1 >= cordinate_y2 and cordinate_y1 < cordinate_y2 + size:
                return True

        if cordinate_x1 > width or cordinate_x1 < 0 or cordinate_y1 > height or cordinate_y1 < 0:
            return True

        return False

    def render_background(self):
        bg = pygame.image.load("assets/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.cordinate_x[0], self.snake.cordinate_y[0], self.apple.cordinate_x, self.apple.cordinate_y):

            # properties position inside self.is_collision must follow from is collision function
            # example is_collision(a, b, c, d) means self.is_collision(a, b, c, d)
            # cannot be self.is_collision(a, c, b, d). Cannot change the position later will get error

            self.sound_effect("Ding-sound-effect")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.cordinate_x[0], self.snake.cordinate_y[0], self.snake.cordinate_x[i], self.snake.cordinate_y[i]):
                self.sound_effect("1_snake_game_resources_crash")
                raise "Collision Occured"

        if self.is_collision(self.snake.cordinate_x[0], self.snake.cordinate_y[0], width, height):
            raise "Collision Occured"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length - 2}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    def game_over(self):

        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        text1 = font.render(
            f"GAME OVER! YOUR SCORE IS {self.snake.length}.", True, (255, 255, 255))
        self.surface.blit(text1, (100, 400))
        text2 = font.render(
            f"HIT 'ENTER' TO PLAY ANOTHER GAME", True, (255, 255, 255))
        self.surface.blit(text2, (100, 500))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # keydown function means when the keyboards are pressed(any keys).
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
