import pygame
pygame.init()
import numpy as np
import time
from Snake import Snake
import os
import cv2

from utils import crossover, mutate, sortSnakes

font = pygame.font.SysFont("Comic Sans MS", 24)

DIRECTIONS = {
	0: "RIGHT",
	1: "DOWN",
	2: "LEFT",
	3: "UP"
}

class Environment:
	def __init__(self, width=640, height=480, video_dir="./video"):
		self.win_width = width
		self.win_height = height
		self.video_folder = video_dir

		if not os.path.isdir(self.video_folder):
			os.mkdir(self.video_folder)

		self.N_ACTIONS = 3

		self.win = pygame.display.set_mode((self.win_width, self.win_height))
		pygame.display.set_caption("Snake Game")

		self.bg_color = (0, 0, 0)	# BLACK


	def updateEnvironment(self):
		self.win.fill(self.bg_color)

	def displayScore(self, score):
		text = font.render(f'Score: {score}', True, (255, 255, 255))
		self.win.blit(text, (0, 0))

	def getObservationShape(self):
		return (11,)

	def isCollision(self, points, snake_list, snake_block):

		if points in snake_list:
			return True

		[x, y] = points

		if x < 0 or x > self.win_width-snake_block	\
			or y < 0 or y > self.win_height - snake_block:

			return True

		return False

	def get_state(self, x, y, foodx, foody, direction, snake_list, snake_block):

		point_l = [x-snake_block, y]
		point_u = [x, y-snake_block]
		point_r = [x+snake_block, y]
		point_d = [x, y+snake_block]

		dir_r = direction == 0
		dir_d = direction == 1
		dir_l = direction == 2
		dir_u = direction == 3
		
		state = [
			# if Danger is in straight
			(dir_r and self.isCollision(point_r, snake_list, snake_block)) or
			(dir_d and self.isCollision(point_d, snake_list, snake_block)) or
			(dir_l and self.isCollision(point_l, snake_list, snake_block)) or
			(dir_u and self.isCollision(point_u, snake_list, snake_block)),

			# If danger is in Right
			(dir_r and self.isCollision(point_d, snake_list, snake_block)) or
			(dir_d and self.isCollision(point_l, snake_list, snake_block)) or
			(dir_l and self.isCollision(point_u, snake_list, snake_block)) or
			(dir_u and self.isCollision(point_r, snake_list, snake_block)),

			# If danger is in Left
			(dir_r and self.isCollision(point_u, snake_list, snake_block)) or
			(dir_d and self.isCollision(point_r, snake_list, snake_block)) or
			(dir_l and self.isCollision(point_l, snake_list, snake_block)) or
			(dir_u and self.isCollision(point_l, snake_list, snake_block)),

			dir_r,
			dir_d,
			dir_l,
			dir_u,

			foodx < x, # Food to left
			foodx > x, # Food to Right
			foody < y, # Food to up
			foody > y
		]

		return np.asarray(state, dtype=np.half)

	def step(self, snakes, render=False):
		# Handle Events to prevent lags in pygame window
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		clk_wise = [0, 1, 2, 3]

		done_snakes = []

		for snake in snakes:
			idx = clk_wise.index(snake.direction)
			obs = self.get_state(snake.X, snake.Y, snake.foodx, snake.foody, snake.direction, snake.snake_list, snake.SNAKE_BLOCK)
			action = snake.get_action(obs)

			# Check the direction the snake is willing to move
			if action == 0:	# If snake wants to go in same direction
				new_dir = clk_wise[idx]
			elif action == 1: # If snake wants to turn right
				new_dir = (clk_wise[idx] + 1) % 4
			else:	# If snake wants to turn left
				new_dir = (clk_wise[idx] - 1) % 4

			if snake.direction == new_dir:
				snake.same_direction_cnt += 1
			else:
				snake.same_direction_cnt = 0

			snake.direction = new_dir
			action = new_dir

			# Based on new action change the X or Y co-ordinate
			if action == 0:
				snake.X += snake.vel
			elif action == 1:
				snake.Y += snake.vel
			elif action == 2:
				snake.X -= snake.vel
			else:
				snake.Y -= snake.vel

			# PUNISHMENT 1: IF there is collision then penalize that snake
			if self.isCollision([snake.X, snake.Y], snake.snake_list, snake.SNAKE_BLOCK):
				snake.done = True
				snake.reward -= 200
				done_snakes.append(snake)
				snakes.remove(snake)

			# PUNISHMENT 2: If snake exceeds max frame than punish it
			if snake.frame_cnt > snake.MAX_FRAME:
				snake.done = True
				snake.reward -= 200
				if snake not in done_snakes:
					done_snakes.append(snake)
					snakes.remove(snake)

			# PUNISHMENT 3: If a snake keeps on moving in same direction then punish it
			if snake.same_direction_cnt > 8:
				snake.reward -= 10
				snake.same_direction_cnt = 0

			# If snake ate food then reward it
			if snake.X in range(snake.foodx, snake.foodx+snake.SNAKE_BLOCK) \
			 and snake.Y in range(snake.foody, snake.foody+snake.SNAKE_BLOCK):
				snake.reward += 200
				snake.MAX_FRAME += 100
				snake.food_eaten = True
				snake.snake_len += 1
				snake.score += 1

			snake.snake_list.append([snake.X, snake.Y])

			if len(snake.snake_list) > snake.snake_len:
				del snake.snake_list[0]

			snake.frame_cnt += 1
			snake.updateUI()

		if render:
			rect = pygame.Rect(0, 0, self.win_width, self.win_height)
			ss = self.win.subsurface(rect)
			img = pygame.surfarray.pixels3d(ss)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			img = np.transpose(img, (1, 0, 2))

			self.video.write(img)

		score = 0
		if not snake[0].done:
			score = snake[0].score
		else:
			score = done_snakes[0].score

		text = font.render(f'Score: {score}', True, (255, 255, 255))
		self.win.blit(text, (0, 0))
		pygame.display.flip()
		return done_snakes, snakes

	def setGeneration(self, generation):
		pygame.display.set_caption(f"Generation {generation+1}")

	def createVideoInstance(self, generation):
		filename = self.video_folder + f"/generation_{generation}.avi"
		self.video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 10, (self.win_width, self.win_height))

	def releaseVideoInstance(self):
		self.video.release()
		time.sleep(1)