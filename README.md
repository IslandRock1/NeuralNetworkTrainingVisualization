
# Neural Network Project

## Installing required libraries

This project has a few dependencies, all of witch can be installed using pip with the following command in a terminal.

```sh
pip install numpy pygame tqdm
```

## Setting up pygame screensize

This is my first time giving someone else my GUI/pygame code, so its fully possible it isnt working as intended. I did find one flaw when testing the code on another students machine, and it has to do with the scaling of the screen.

Especially laptops usually has the screen setting "scale" set to 150% or even 200%. This will make it look like only half or a quarter of the pygamw window is showing. This can be solved by either changing the scale setting on the computer to 100%, or by modifying the initial screen size in my program.

For `testAndVisuNetwork.py` this is done on line 195, and for `trainNeuralNetwork.py` this is done on line 44 and 45.

## Training your own network

To train your own network you first need to choose wether you want to train the network for the inverted pendelum, or for the logic gates.

### Logic Gates

Training a network for the logic gates is the reccomended method. This does not take too much time, but will still give a sense of how the code works.

Start by making sure you have selected the right value for `testPendelum` on line 17 of `trainNeuralNetwork.py`. Once this is done you can choose wether to train the network for 2, 3, or 4 gates by changing the operations in `LogicGates/test.py/generateTestAndAnswer()` function. The final step is to update the hyperparams in `LogicGates/HYPERPARAMS.py` to your liking. The most important changes are the number of output nodes, witch should be the same as the number of gates.

Once this is done you can run the `trainNeuralNetwork.py` file and watch your network learn.

### Inverted pendelum

To train the network for the inverted pendelum start by making sure you have selected the right value for `testPendelum` on line 17 of `trainNeuralNetwork.py`. After this update the hyperparams in `PendelumCart/HYPERPARAMS.py` to your liking. You can also change physical parameters in the `PendelumCart/PendelSimulation.py` file. Then you can modify the `PendelumCart/test.py/rewardFunction()` function to your liking.

Lastly, it is reccomended to take a backup of the pre-trained networks in the `PendelumCart/models` folder. Training a network to solve the inverted pendelum takes a long time, so for visualizaion it is reccomended to use the pre-trained ones.

Once this is done you can run the `trainNeuralNetwork.py` file and watch your network learn.

## Testing the network

Currently the visualization and testing of the network only works for the inverted pendelum. If you do not want to train your own network there are some provided already. Network 61 is a pretty decent solution.

In line 201 of `testAndVisuNetwork.py` you can choose what network you want to visualize. When training, the network saves the best network from each generation, this means that a higher number is often better.

To play yourself you can use the `p` key to change the player from the network to the player, this also works the other way. To take a screenshot the key `s` can be used. When controlling the pendelum manually the left and right arrowkeys are used.