# Genetic-algorithm
Snake game using genetic algorithm

Genetic algorithm is highly inspired by the evolution of the human race and its development is done so by trial and error, and 
where each human generation has something to pass on to their offspring.

## How it works in this case?
First, we generate a population of snakes and let them explore the environment. Based on their performance we assign them their fitness score,
which indicates the quality of the snake(better the fitness score better the quality of the snake).

Once the lifetime of every snake in a generation ends we perform the following steps
1. Select top snakes from the current generation to act as parents for creating the next generation and qualify for performing in the next generation.
2. Based on top performers create a specific amount of members for the next generation by crossing over those parents.
3. Lastly to fill the generation create new members.
Taking the best performer from each generation and crossing them over is not necessary. As this will not result in innovation.
Thus in order to introduce a slight entropy and also make the performer motivate to explore new actions we mutate some members
of the next generation.
4. Randomly mutate some members of the next generation.

We perform this step for many generations until the desired result is achieved.

Here are some results from my snake generations.

### Generation 50
This generation was totally random yet learnt a lot of things.

<video src='https://github.com/Gruhit13/genetic-algorithm/blob/main/videos/generation_100.mp4' width=180/>
