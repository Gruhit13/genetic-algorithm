from Environment import Environment
import pygame
pygame.init()
import numpy as np
import time
from Snake import Snake
import os

from utils import crossover, mutate, sortSnakes
DIRECTIONS = {
	0: "RIGHT",
	1: "DOWN",
	2: "LEFT",
	3: "UP"
}

if __name__ == "__main__":
	env = Environment()
	NAME = "Snake_"

	N_GENERATIONS = 2
	POPULATION = 50

	P_CROSSOBER = 0.5
	P_MUTATE = 0.2
	TOP_N_PARENTS = 2

	snakes = []
	for i in range(POPULATION):
		snakes.append(Snake(env, NAME+str(i+1)))
		snakes[-1].reset()

	for i in range(N_GENERATIONS):
		done_snakes = []

		print("\nGeneration: ", i+1)
		env.createVideoInstance(i+1)

		# print("Total Snakes: ", len(snakes))
		while len(snakes) != 0:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			env.updateEnvironment()
			env.displayScore(snake.score)

			d_snake, snakes = env.step(snakes, render=False)
			# time.sleep(0.1)
			for snake in d_snake:
				done_snakes.append(snake)

		env.releaseVideoInstance()

		# Sort the snakes with best fitness values
		sortedSnakes = sortSnakes(done_snakes)

		# Save the best snake
		sortedSnakes[0].save_brain(i+1)

		print("Top 5 Candidate")
		# Print top - 5 candiate
		for i in range(5):
			sortedSnakes[i].printData()

		snakes = []

		# Take TOP_N_PARENTS as it is
		for k in range(TOP_N_PARENTS):
			snake = sortedSnakes[k]
			snake.rename(NAME+str(k))
			snakes.append(snake)

		# Create other population from TOP_N_PARENTS
		for k in range(TOP_N_PARENTS, POPULATION // 2):
			child = Snake(env, NAME+str(TOP_N_PARENTS+k))

			idx1 = np.random.randint(0, TOP_N_PARENTS)
			idx2 = np.random.randint(0, TOP_N_PARENTS)

			child_weight = crossover(snakes[idx1], snakes[idx2], P_CROSSOBER)
			child.set_weights(child_weight)
			snakes.append(child)

		# Create new snakes to fill rest of population
		for k in range(len(snakes), POPULATION):
			snakes.append(Snake(env, NAME+str(k+1)))

		# Perform mutation randomly over population
		for j in range(len(snakes)):
			if np.random.uniform(0, 1) < P_MUTATE:
				snake = mutate(snakes[j], P_MUTATE)
				snakes[j] = snake

			snakes[j].reset()
			snakes[j].rename(NAME+str(j+1))