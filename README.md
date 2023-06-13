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




https://github.com/Gruhit13/genetic-algorithm/assets/64111603/f47b07cd-5ef4-479b-837a-8c090b48b813



### Generation 200
Till now snakes were able to understand that the best way to survive longer is by eating more apple as they would get more frame
to work on when they eat more apply.




https://github.com/Gruhit13/genetic-algorithm/assets/64111603/85fc1b87-db4e-418b-a8b9-3f6b57f05092

### Generation 350
By the 300th generation, snakes had figured out what can be the best way to eat apples and its really interesting to watch how they do so



https://github.com/Gruhit13/genetic-algorithm/assets/64111603/b2ccddeb-2b77-475d-83a1-7f669730da49


### Valuable Insights
After 350 generations snakes had learned many things
- not to strike the wall.
- not to keep moving in the same direction unusually.
- not to strike in their own body even if the food is generated there.
- keep eating more apples in order to survive more.
- an optimal way of eating way in a way that their body stays on the edge of the wall so they
  get more area to more freely.
