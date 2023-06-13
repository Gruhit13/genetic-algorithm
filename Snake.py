import tensorflow as tf
import numpy as np
import pygame
import os

from utils import create_model

class Snake:
	def __init__(self, env, name, win_width=640, win_height=480, chkpt_dir="./Brains"):
		
		self.name = name
		self.env = env
		
		self.win_width = win_width
		self.win_height = win_height
		self.checkpoint_dir = chkpt_dir

		if not os.path.isdir(self.checkpoint_dir):
			os.mkdir(self.checkpoint_dir)		 

		self.SNAKE_BLOCK = 20
		self.X = self.win_width // 2
		self.Y = self.win_height // 2

		self.foodx = np.random.randint(0, (self.win_width-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK
		self.foody = np.random.randint(0, (self.win_height-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK

		self.snake_list = [[self.X, self.Y]]
		self.snake_len = 1

		self.direction = 0
		self.vel = self.SNAKE_BLOCK
		self.score = 0

		self.green = (0, 244, 0)
		self.blue = (0, 100, 255)
		self.food_color = (205, 0, 0)

		self.MAX_FRAME = 300
		self.frame_cnt = 0

		self.done = False
		self.reward = 0

		self.same_direction_cnt = 0
		self.food_eaten = False

		self.brain = create_model(self.env.getObservationShape(), 11, 64, self.env.N_ACTIONS, 0.001)

	def reset(self):
		self.X = self.win_width // 2
		self.Y = self.win_height // 2
		self.snake_list = [[self.X, self.Y]]
		self.snake_len = 1
		self.score = 0
		self.direction = 0
		
		self.frame_cnt = 0
		self.MAX_FRAME = 300
		self.done = False
		self.reward = 0

		self.same_direction_cnt = 0

		self.foodx = np.random.randint(0, (self.win_width-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK
		self.foody = np.random.randint(0, (self.win_height-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK
		self.food_eaten = False

		self.updateUI()


	def __drawSnake(self):
		for pos in self.snake_list:
			pygame.draw.rect(self.env.win, self.green, (pos[0], pos[1], self.SNAKE_BLOCK, self.SNAKE_BLOCK))
			pygame.draw.rect(self.env.win, self.blue, (pos[0]+4, pos[1]+4, self.SNAKE_BLOCK-8, self.SNAKE_BLOCK-8))

	def __drawFood(self):
		pygame.draw.rect(self.env.win, self.food_color, (self.foodx, self.foody, self.SNAKE_BLOCK, self.SNAKE_BLOCK))

	def updateUI(self):
		self.__drawSnake()

		if self.food_eaten:
			self.food_eaten = False
			self.foodx = np.random.randint(0, (self.win_width-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK
			self.foody = np.random.randint(0, (self.win_height-self.SNAKE_BLOCK) // self.SNAKE_BLOCK) * self.SNAKE_BLOCK

		self.__drawFood()

	def get_action(self, observation):
		obs = tf.convert_to_tensor([observation], dtype=tf.float32)
		action = self.brain(obs).numpy().argmax(axis=-1)
		return action

	def save_brain(self, generation):
		self.brain.save_weights(self.checkpoint_dir+f"/gen_{generation}_{self.name}.h5")

	def load_brain(self, filename):
		# self.brain = tf.keras.models.load_model(filename)
		self.brain.load_weights(filename)
		print(f"\nBranin loaded from {filename}")

	def rename(self, new_name):
		self.name = new_name

	def getFitness(self):
		return self.reward

	def printData(self):
		print(f"{self.name} | Frame: {self.frame_cnt} | Score: {self.score} | Fitness: {self.getFitness()}")

	def set_weights(self, weights):
		self.brain.set_weights(weights)

	def get_weights(self):
		return self.brain.get_weights()