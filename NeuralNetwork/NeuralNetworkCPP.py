
try:
    from NeuralNetworkPython import NeuralNetwork as NeuralNetworkCPP
    from NeuralNetworkPython import ModificationOptions as ModificationOptionsCPP
except ModuleNotFoundError:
    from NeuralNetwork.NeuralNetworkPython import NeuralNetwork as NeuralNetworkCPP
    from NeuralNetwork.NeuralNetworkPython import ModificationOptions as ModificationOptionsCPP

class MofificationOptions():
    def __init__(self, numChanges, temperature):
        self._modificationOptions = ModificationOptionsCPP(numChanges, temperature)

    def getRaw(self):
        return self._modificationOptions

class NeuralNetwork:
    def __init__(self, nodeLayerSizes: list[int]):
        self._nn = NeuralNetworkCPP(nodeLayerSizes)

    def compute(self, inputValues: list[float]):
        out = self._nn.compute(inputValues)
        return out

    def randomChange(self, modificationOptions: MofificationOptions):
        self._nn.executeRandomChange(modificationOptions.getRaw())

    def save(self, path):
        if not path.endswith(".txt"):
            path += ".txt"

        self._nn.save(path)

    def copy(self):

        newNetwork = NeuralNetwork([0])
        newNetwork._nn = self._nn.copy()
        return newNetwork

if __name__ == "__main__":
    nn = NeuralNetwork([1, 1])
    signals = [0.0]

    newNN = nn.copy()

    mod = MofificationOptions(1, 1)
    nn.randomChange(mod)

    print(nn.compute(signals))
    print(newNN.compute(signals))