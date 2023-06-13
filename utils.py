import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense

import numpy as np

def create_model(input_shape, fc1, fc2, actions, lr, use_bias=False):
	model = tf.keras.Sequential()
	model.add(Dense(fc1, activation="relu", input_shape=input_shape, use_bias=use_bias))
	model.add(Dense(fc2, activation="relu", input_shape=input_shape, use_bias=use_bias))
	model.add(Dense(actions, activation='softmax', use_bias=use_bias))

	model.compile(loss='mse', optimizer=Adam(learning_rate=lr))
	return model

def sortSnakes(snake_list):
	fitness = {}

	for snake in snake_list:
		fitness[snake] = snake.getFitness()

	sortedSnakes = sorted(fitness.items(), key=lambda kv: kv[1], reverse=True)

	return [snake[0] for snake in sortedSnakes]

def crossover(parent1, parent2, p_crossover):
	weight1 = parent1.get_weights()
	weight2 = parent2.get_weights()

	offspring_weight = []
	for idx, weight in enumerate(weight1):
		for i in range(weight.shape[0]):
			for j in range(weight.shape[1]):
				if np.random.uniform(0, 1) < p_crossover:
					weight[i, j] = weight2[idx][i, j]
		offspring_weight.append(weight)

	return offspring_weight

def mutate(parent, p_mutate):
	weights = parent.get_weights()

	for idx, weight in enumerate(weights):
		for i in range(weight.shape[0]):
			for j in range(weight.shape[1]):
				if np.random.uniform(0, 1) < p_mutate:
					weight[i, j] += np.random.uniform(-0.5, 0.5)

		weights[idx] = weight

	parent.set_weights(weights)
	return parent

# if __name__ == "__main__":
# 	a = {
# 		1: "a",
# 		2: "c",
# 		3: "d"
# 	}

# 	sort = sorted(a.items(), key=lambda kv: kv[1], reverse=True)
# 	ans = [temp[0] for temp in sort]
# 	print("Sort = ", sort)
# 	print("Ans = ", ans)