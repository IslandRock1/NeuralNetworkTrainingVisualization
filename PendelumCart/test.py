
from math import sin, cos
from random import random

from .PendelSimulation import PendelSimulation

class testControlAlgorithm:
    def __init__(self, initOptions = None):
        self.system = PendelSimulation()

        if (initOptions is not None):
            # print(f"Using options: {initOptions}")
            self.system.rotationPos = initOptions[0]
            self.system.rotationVel = initOptions[1]

            self.system.cartPos = initOptions[2]
            self.system.cartVel = initOptions[3]
        else:
            self.system.rotationPos = random() * 2 * 3.1415926
            self.system.rotationVel = (random() * 2.0 - 1.0) / 10

            self.system.cartPos = (random() * 2.0 - 1.0)
            self.system.cartVel = (random() * 2.0 - 1.0) / 10

        self.dt = 1.0 / 60.0

        self.runningCount = 0
        self._sumTime = 0
        self._sumReward = 0

        self.cartPosIntegral = 0
        self.iterationCount = 1
        self.maxTime = 20
    
    def getInfo(self):
        rotPos = self.system.rotationPos
        rotVel = self.system.rotationVel
        carPos = self.system.cartPos
        carVel = self.system.cartVel

        rotX = sin(rotPos)
        rotY = cos(rotPos)

        carVel = max(min(10, carVel), -10)
        carVel /= 10

        return [rotX, rotY, rotVel, carPos, carVel]

    def update(self, inputSignal, constValues: list[float] = []):
        
        force = inputSignal[0]
        force = min(1, force)
        force = max(-1, force)

        self._sumTime += self.dt

        self.system.update(self.dt, force)

        finished = self._sumTime > self.maxTime
        reward = self.rewardFunction(constValues)

        progress = self._sumTime / self.maxTime

        return finished, reward, progress

    def rewardFunction(self, constValues: list[float] = []):
        error = abs(self.system.rotationPos)

        overTreshold = error <= (3.1415926 / 4)
        self.runningCount = (self.runningCount + 1.0 / 1_000.0) * int(overTreshold)
        heightTerm = self.runningCount * (overTreshold)

        rotVel = self.system.rotationVel
        positionTerm = abs(self.system.cartPos) * abs(self.system.cartPos)
        velocityTerm = abs(self.system.cartVel) * abs(self.system.cartVel)

        if (len(constValues) != 0):
            result = constValues[0] * heightTerm + constValues[1] * rotVel + constValues[2] * positionTerm + constValues[3] * velocityTerm
        else: result = heightTerm - rotVel - positionTerm - velocityTerm
        self._sumReward += result

        return self._sumReward