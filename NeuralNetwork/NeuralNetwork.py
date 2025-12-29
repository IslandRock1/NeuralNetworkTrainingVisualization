
from time import perf_counter

import numpy as np
from random import random, randint, choice

def tanH(z):
    return np.tanh(z)

def ReLU(z):
    return max(0, z)

def Sigmoid(z):
    if (z < -200): return 0.0
    if (z > 40): return 1.0

    return 1 / (1 + np.exp(-z))

def linear(z):
    return z

class Node:
    def __init__(self, numWeights, scale: float = 1.0):
        
        """
        weights is the weights from each of the nodes from the previous layer.
        """
        
        self.weights = np.random.random([numWeights]) * 2.0 * scale - 1.0 * scale
        self.bias = random() * 2.0 * scale - 1.0 * scale

        self.value = 0
        self.function = choice(self.getLegalFunctions())
    
    def returnActivatedValue(self, value):
        match self.function:
            case 0:
                return tanH(value)
            
            case 1:
                return ReLU(value)
            
            case 2:
                return Sigmoid(value)
            
            case 3:
                return linear(value)

    def executeActivationFunction(self):
        match self.function:
            case 0:
                self.value = tanH(self.value)
            
            case 1:
                self.value = ReLU(self.value)
            
            case 2:
                self.value = Sigmoid(self.value)
            
            case 3:
                self.value = linear(self.value)

    def getLegalFunctions(self):
        return [0, 1, 2, 3]

class Layer:
    def __init__(self, size, sizeIn):
        self.initNodes(size, sizeIn)
        self.numNodes = size

    def initNodes(self, num: int, numIn: int) -> list[Node]:
        self.nodes: list[Node] = []

        for _ in range(num):
            n = Node(numIn)
            self.nodes.append(n)
    
    def setValues(self, values: np.array):
        for node, val in zip(self.nodes, values):
            node.value = val

    def computeLayer(self, inputValues: np.array):
        output = np.array([n.bias for n in self.nodes])
    
        for ix in range(self.numNodes):

            tmp = 0
            for n in range(len(inputValues)):
                tmp += inputValues[n] * self.nodes[ix].weights[n]

            output[ix] += tmp

        for ix in range(self.numNodes):
            output[ix] = self.nodes[ix].returnActivatedValue(output[ix])

        for ix in range(self.numNodes):
            self.nodes[ix].value = output[ix]
            
        return output

class NeuralNetwork:
    def __init__(self, nodeLayerSizes: list[int]):
        self.initLayers(nodeLayerSizes)

    def initLayers(self, nodeLayerSizes: list[int]):
        self.layers: list[Layer] = []

        l = Layer(nodeLayerSizes[0], 0)
        for node in l.nodes:
            node.bias = 0
        self.layers.append(l)

        for ix in range(len(nodeLayerSizes) - 1):
            l = Layer(nodeLayerSizes[ix + 1], nodeLayerSizes[ix])
            self.layers.append(l)

    def compute(self, inputValues: list[float]):
        self.layers[0].setValues(inputValues)
        
        inputValues = np.array(inputValues)

        for layer in self.layers[1:]:
            inputValues = layer.computeLayer(inputValues)
        
        return inputValues

def getFunctionFromString(string):
    match string:
        case "TanH":
            return 0
        case "ReLU":
            return 1
        case "Sigmoid":
            return 2
        case "Linear":
            return 3

def loadNetwork(path: str):
    if not path.endswith(".txt"):
        path += ".txt"
    
    with open(path, "r") as file:
        lines = file.readlines()

    for ix, line in enumerate(lines):
        lines[ix] = line[0:-1]

    sizeLine = lines[0]
    layersNum = list(sizeLine.split(":"))
    layersNum = [int(x) for x in layersNum]
    
    nn = NeuralNetwork(layersNum)

    nn: NeuralNetwork
    for line in lines[1:]:

        values = line.split(":")

        ixL = int(values[0])
        ixN = int(values[1])

        try:
            nn.layers[ixL].nodes[ixN].function = int(values[2])
        except Exception as e:
            nn.layers[ixL].nodes[ixN].function = getFunctionFromString(values[2])

        nn.layers[ixL].nodes[ixN].bias = float(values[3])
        nn.layers[ixL].nodes[ixN].weights = [float(x) for x in values[4:]]

    return nn

def saveNetwork(nn: NeuralNetwork, path: str):
    sizes = [l.numNodes for l in nn.layers]

    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, "w") as file:
        
        for size in sizes[0:-1]:
            file.write(str(size))
            file.write(":")
        file.write(str(sizes[-1]) + "\n")

        for ixL, layer in enumerate(nn.layers):
            for ixN, node in enumerate(layer.nodes):
                file.write(f"{ixL}:{ixN}:{node.function}:{node.bias}")
                for w in node.weights:
                    file.write(f":{w}")
                
                file.write("\n")

def getRandomNodePosition(nn: NeuralNetwork):
    
    numNodes = sum([l.numNodes for l in nn.layers[1:]])
    randNum = random()

    nodeCount = 0

    layerPos = -1
    for ix, l in enumerate(nn.layers[1:]):
        nodeCount += l.numNodes

        if randNum < (nodeCount / numNodes):
            layerPos = ix + 1
            break

    if layerPos == -1:
        layerPos = len(nn.layers) - 1

    nodesInLayer = nn.layers[layerPos].numNodes
    nodePos = randint(0, nodesInLayer - 1)

    return layerPos, nodePos

def randomChange(nn: NeuralNetwork, hyperParams):
    """
    Should probably be made such that the chances are based on
    number of weights and such
    """

    randNum = random()
    layerPos, nodePos = getRandomNodePosition(nn)

    scale = hyperParams.SCALE_VALUE_FOR_CHANGES_TO_BIAS_AND_WEIGHT
    randChange = random() * 2.0 - 1.0 #Random number between -1 and 1
    randChange *= scale

    functionChance = float(hyperParams.PERCENTAGE_CHANCE_TO_CHANGE_ACTIVATION_FUNCTION) / 100.0
    weightChance = functionChance + float(hyperParams.PERCENTAGE_CHANCE_TO_CHANGE_ONE_WEIGHT) / 100.0
    biasChance = weightChance + float(hyperParams.PERCENTAGE_CHANCE_TO_CHANGE_BIAS) / 100.0

    if abs(biasChance - 1.0) > 0.001: 
        print(f"HYPERPARAMS does not sum to 100%, instead it is {biasChance}")

    if randNum < functionChance:
        # Change function
        nn.layers[layerPos].nodes[nodePos].function = choice(nn.layers[layerPos].nodes[nodePos].getLegalFunctions())

    elif randNum < weightChance:
        # Change weight
        numWeights = len(nn.layers[layerPos].nodes[nodePos].weights)
        w = randint(0, numWeights - 1)

        nn.layers[layerPos].nodes[nodePos].weights[w] += randChange

    elif randNum < biasChance:
        # Change bias
        nn.layers[layerPos].nodes[nodePos].bias += randChange

    else:
        ...
    
    return nn


def main():
    nn = NeuralNetwork([1, 1])
    inputValues = [0.0]

    newNN = nn.co

if __name__ == "__main__": main()