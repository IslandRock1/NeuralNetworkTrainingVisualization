from math import sin, cos, pi

class PendelSimulation():
    def __init__(self):
        self.pendelumLength = 2.0
        self.massCart = 1
        self.massPendelum = 0.2

        self.simulationSteps = 1

        self.rotationPos = 0.0
        self.rotationVel = 0.0
        
        self.cartPos = 0
        self.cartVel = 0

        self.numHits = 0
        self.didHitLeft = False
        self.didHitRight = False
    
    def update(self, dt: float, externalForce: float = 0):
        
        g = 9.81
        dt /= self.simulationSteps
        externalForce *= 10.0
        
        for _ in range(self.simulationSteps):
            sinTheta = sin(self.rotationPos + pi)
            cosTheta = cos(self.rotationPos + pi)

            t0 = self.massPendelum * self.pendelumLength * self.rotationVel * self.rotationVel * sinTheta
            t1 = self.massPendelum * g * sinTheta * cosTheta
            t2 = externalForce
            n = self.massCart + self.massPendelum * sinTheta * sinTheta

            positionAcc = (t0 + t1 + t2) / (n)

            t0 = -self.massPendelum * self.pendelumLength * self.rotationVel * self.rotationVel * sinTheta * cosTheta
            t1 = -(self.massPendelum + self.massCart) * g * sinTheta
            t2 = -externalForce * cosTheta
            n = self.pendelumLength * (self.massCart + self.massPendelum * sinTheta * sinTheta)

            rotationAcc = (t0 + t1 + t2) / (n)

            self.rotationVel *= 0.99999
            self.rotationVel += rotationAcc * dt
            self.rotationPos += self.rotationVel * dt

            self.cartVel *= 0.99999
            self.cartVel += positionAcc * dt
            self.cartPos += self.cartVel * dt

            two_pi = 2 * pi
            self.rotationPos = self.rotationPos % two_pi

            if self.rotationPos > pi:
                self.rotationPos -= two_pi
            elif self.rotationPos < -pi:
                self.rotationPos += two_pi
