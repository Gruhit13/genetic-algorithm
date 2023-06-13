import pygame
pygame.init()
from Environment import Environment
from Snake import Snake
import time
import os

def test():
	env = Environment()
	snake = Snake(env, "Test Snake")

	GEN = 391
	Snake_n = 64
	filename = f"./Brains/gen_{GEN}_Snake_{Snake_n}.h5"
	snake.load_brain(filename)
	snake.reset()

	while not snake.done:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		env.updateEnvironment()
		done_snake, snakes = env.step([snake], render=False)
		time.sleep(0.1)

		if len(done_snake) > 0:
			snake = done_snake[0]
		else:
			snake = snakes[0]

	snake.printData()

test()